package main

import (
	"encoding/json"
	"fmt"
	"sort"
)

type Phase string

const (
	Proposal  Phase = "PROPOSAL"
	Prevote   Phase = "PREVOTE"
	Polka     Phase = "POLKA"
	Precommit Phase = "PRECOMMIT"
	Commit    Phase = "COMMIT"
)

type Grammar string

const (
	TypeSpecific Grammar = "G_T_TYPE_SPECIFIC"
	DirectedOff  Grammar = "G_D_ROUND0_EDGE_OFF"
	DirectedOn   Grammar = "G_D_ROUND0_EDGE_ON"
)

type Mutation string

const (
	Baseline          Mutation = "BASELINE"
	MissingLockUpdate Mutation = "MISSING_LOCK_UPDATE"
)

type Message struct {
	From  string `json:"from"`
	To    string `json:"to"`
	Round int    `json:"round"`
	Value int    `json:"value"`
	Phase Phase  `json:"phase"`
}

type Replica struct {
	Name        string `json:"name"`
	Locked      bool   `json:"locked"`
	LockedValue int    `json:"locked_value"`
	LockedRound int    `json:"locked_round"`
	Decided     bool   `json:"decided"`
	Decision    int    `json:"decision"`
}

type VoteKey struct {
	Validator string
	Round     int
	Value     int
	Phase     Phase
}

type LeaderRound struct {
	Prevotes      map[VoteKey]struct{}
	Precommits    map[VoteKey]struct{}
	PolkaEmitted  bool
	CommitEmitted bool
}

type LogEntry struct {
	Index   int      `json:"index"`
	Action  string   `json:"action"`
	Message *Message `json:"message,omitempty"`
	Detail  string   `json:"detail"`
}

type EventLoop struct {
	Grammar  Grammar
	Mutation Mutation
	Quorum   int
	Queue    []Message
	Replicas map[string]*Replica
	Leader   map[int]*LeaderRound
	Log      []LogEntry
}

func NewEventLoop(grammar Grammar, mutation Mutation) *EventLoop {
	replicas := map[string]*Replica{
		"H1": {Name: "H1", LockedRound: -1, Decision: -1},
		"P":  {Name: "P", LockedRound: -1, Decision: -1},
		"H3": {Name: "H3", LockedRound: -1, Decision: -1},
	}
	return &EventLoop{
		Grammar:  grammar,
		Mutation: mutation,
		Quorum:   3,
		Replicas: replicas,
		Leader:   map[int]*LeaderRound{},
	}
}

func (e *EventLoop) record(action string, msg *Message, detail string) {
	var copyMsg *Message
	if msg != nil {
		m := *msg
		copyMsg = &m
	}
	e.Log = append(e.Log, LogEntry{Index: len(e.Log), Action: action, Message: copyMsg, Detail: detail})
}

func (e *EventLoop) allow(msg Message) bool {
	// Gate 6' studies one view-local endpoint edge: Byzantine leader B -> pivot P
	// in round 0. Other edges are deliberately left open.
	if msg.Round != 0 || msg.From != "B" || msg.To != "P" {
		return true
	}
	switch e.Grammar {
	case TypeSpecific:
		// Phase-specific policy passes enabling proposal/POLKA but withholds the
		// later terminal repair/commit on the same endpoint edge.
		return msg.Phase != Commit
	case DirectedOff:
		// One type-uniform directed graph per round: the edge is absent for all
		// phases on B -> P.
		return false
	case DirectedOn:
		// The same edge is present for all phases, including terminal repair.
		return true
	default:
		panic("unknown grammar")
	}
}

func (e *EventLoop) enqueue(msg Message) {
	e.Queue = append(e.Queue, msg)
	e.record("ENQUEUE", &msg, "message entered deterministic FIFO event loop")
}

func (e *EventLoop) roundState(round int) *LeaderRound {
	state, ok := e.Leader[round]
	if !ok {
		state = &LeaderRound{
			Prevotes:   make(map[VoteKey]struct{}),
			Precommits: make(map[VoteKey]struct{}),
		}
		e.Leader[round] = state
	}
	return state
}

func (e *EventLoop) canSupport(replica *Replica, value int) bool {
	if replica.Decided && replica.Decision != value {
		return false
	}
	return !replica.Locked || replica.LockedValue == value
}

func (e *EventLoop) proposalTargets(round int) []string {
	if round == 0 {
		return []string{"H1", "P"}
	}
	return []string{"P", "H3"}
}

func (e *EventLoop) startRound(round, value int) {
	state := e.roundState(round)
	// Byzantine leader contributes exactly one logical prevote for this round
	// and value. Replay cannot create additional voting power.
	state.Prevotes[VoteKey{Validator: "B", Round: round, Value: value, Phase: Prevote}] = struct{}{}
	e.record("ROUND_START", nil, fmt.Sprintf("round=%d value=%d", round, value))
	for _, target := range e.proposalTargets(round) {
		e.enqueue(Message{From: "B", To: target, Round: round, Value: value, Phase: Proposal})
	}
	e.drain()
}

func (e *EventLoop) drain() {
	for len(e.Queue) > 0 {
		msg := e.Queue[0]
		e.Queue = e.Queue[1:]
		if !e.allow(msg) {
			e.record("DROP", &msg, "blocked by selected scheduler grammar")
			continue
		}
		e.record("DELIVER", &msg, "delivered by deterministic FIFO scheduler")
		e.handle(msg)
	}
}

func (e *EventLoop) handle(msg Message) {
	if msg.To == "B" {
		e.handleLeader(msg)
		return
	}
	replica := e.Replicas[msg.To]
	if replica == nil {
		panic("message addressed to unknown replica")
	}
	switch msg.Phase {
	case Proposal:
		if !e.canSupport(replica, msg.Value) {
			e.record("REJECT", &msg, "proposal conflicts with persistent lock or decision")
			return
		}
		e.enqueue(Message{From: replica.Name, To: "B", Round: msg.Round, Value: msg.Value, Phase: Prevote})
	case Polka:
		if !e.canSupport(replica, msg.Value) {
			e.record("REJECT", &msg, "POLKA conflicts with persistent lock or decision")
			return
		}
		if e.Mutation == Baseline {
			replica.Locked = true
			replica.LockedValue = msg.Value
			replica.LockedRound = msg.Round
			e.record("STATE", nil, fmt.Sprintf("%s locks value=%d round=%d", replica.Name, msg.Value, msg.Round))
		} else {
			e.record("MUTATION", nil, fmt.Sprintf("%s omits persistent lock update", replica.Name))
		}
		e.enqueue(Message{From: replica.Name, To: "B", Round: msg.Round, Value: msg.Value, Phase: Precommit})
	case Commit:
		if replica.Decided && replica.Decision != msg.Value {
			e.record("REJECT", &msg, "terminal evidence conflicts with irreversible decision")
			return
		}
		if !replica.Decided {
			replica.Decided = true
			replica.Decision = msg.Value
			e.record("STATE", nil, fmt.Sprintf("%s decides value=%d round=%d", replica.Name, msg.Value, msg.Round))
		}
	default:
		panic(fmt.Sprintf("replica received unexpected phase %s", msg.Phase))
	}
}

func (e *EventLoop) addUnique(target map[VoteKey]struct{}, msg Message) bool {
	key := VoteKey{Validator: msg.From, Round: msg.Round, Value: msg.Value, Phase: msg.Phase}
	if _, exists := target[key]; exists {
		e.record("DUPLICATE", &msg, "stable logical vote already counted")
		return false
	}
	target[key] = struct{}{}
	return true
}

func (e *EventLoop) supportCount(votes map[VoteKey]struct{}, round, value int, phase Phase) int {
	count := 0
	for key := range votes {
		if key.Round == round && key.Value == value && key.Phase == phase {
			count++
		}
	}
	return count
}

func (e *EventLoop) handleLeader(msg Message) {
	state := e.roundState(msg.Round)
	switch msg.Phase {
	case Prevote:
		e.addUnique(state.Prevotes, msg)
		if !state.PolkaEmitted && e.supportCount(state.Prevotes, msg.Round, msg.Value, Prevote) >= e.Quorum {
			state.PolkaEmitted = true
			// Byzantine leader contributes one logical precommit once the POLKA is formed.
			state.Precommits[VoteKey{Validator: "B", Round: msg.Round, Value: msg.Value, Phase: Precommit}] = struct{}{}
			e.record("CERTIFICATE", nil, fmt.Sprintf("POLKA formed round=%d value=%d", msg.Round, msg.Value))
			for _, target := range e.proposalTargets(msg.Round) {
				e.enqueue(Message{From: "B", To: target, Round: msg.Round, Value: msg.Value, Phase: Polka})
			}
		}
	case Precommit:
		e.addUnique(state.Precommits, msg)
		if !state.CommitEmitted && e.supportCount(state.Precommits, msg.Round, msg.Value, Precommit) >= e.Quorum {
			state.CommitEmitted = true
			e.record("CERTIFICATE", nil, fmt.Sprintf("COMMIT formed round=%d value=%d", msg.Round, msg.Value))
			for _, target := range e.proposalTargets(msg.Round) {
				e.enqueue(Message{From: "B", To: target, Round: msg.Round, Value: msg.Value, Phase: Commit})
			}
		}
	default:
		panic(fmt.Sprintf("leader received unexpected phase %s", msg.Phase))
	}
}

type Decision struct {
	Replica string `json:"replica"`
	Value   int    `json:"value"`
}

type CaseResult struct {
	Grammar      Grammar           `json:"grammar"`
	Mutation     Mutation          `json:"mutation"`
	Unsafe       bool              `json:"unsafe"`
	Decisions    []Decision        `json:"decisions"`
	Locks        map[string]string `json:"locks"`
	PolkaRounds  []int             `json:"polka_rounds"`
	CommitRounds []int             `json:"commit_rounds"`
	Log          []LogEntry        `json:"log"`
}

func ExecuteCase(grammar Grammar, mutation Mutation) CaseResult {
	loop := NewEventLoop(grammar, mutation)
	loop.startRound(0, 0)
	loop.startRound(1, 1)

	decisions := make([]Decision, 0)
	locks := make(map[string]string)
	for name, replica := range loop.Replicas {
		if replica.Decided {
			decisions = append(decisions, Decision{Replica: name, Value: replica.Decision})
		}
		if replica.Locked {
			locks[name] = fmt.Sprintf("%d@%d", replica.LockedValue, replica.LockedRound)
		} else {
			locks[name] = "none"
		}
	}
	sort.Slice(decisions, func(i, j int) bool { return decisions[i].Replica < decisions[j].Replica })
	values := make(map[int]struct{})
	for _, decision := range decisions {
		values[decision.Value] = struct{}{}
	}
	polkas := make([]int, 0)
	commits := make([]int, 0)
	for round, state := range loop.Leader {
		if state.PolkaEmitted {
			polkas = append(polkas, round)
		}
		if state.CommitEmitted {
			commits = append(commits, round)
		}
	}
	sort.Ints(polkas)
	sort.Ints(commits)
	return CaseResult{
		Grammar:      grammar,
		Mutation:     mutation,
		Unsafe:       len(values) > 1,
		Decisions:    decisions,
		Locks:        locks,
		PolkaRounds:  polkas,
		CommitRounds: commits,
		Log:          loop.Log,
	}
}

type SuiteResult struct {
	Status string          `json:"status"`
	Cases  []CaseResult    `json:"cases"`
	Checks map[string]bool `json:"checks"`
}

func EvaluateSuite() SuiteResult {
	cases := []CaseResult{
		ExecuteCase(TypeSpecific, Baseline),
		ExecuteCase(DirectedOff, Baseline),
		ExecuteCase(DirectedOn, Baseline),
		ExecuteCase(TypeSpecific, MissingLockUpdate),
		ExecuteCase(DirectedOff, MissingLockUpdate),
		ExecuteCase(DirectedOn, MissingLockUpdate),
	}
	byKey := make(map[string]CaseResult)
	for _, result := range cases {
		byKey[string(result.Grammar)+"/"+string(result.Mutation)] = result
	}
	checks := map[string]bool{
		"all_baselines_safe": !byKey[string(TypeSpecific)+"/"+string(Baseline)].Unsafe &&
			!byKey[string(DirectedOff)+"/"+string(Baseline)].Unsafe &&
			!byKey[string(DirectedOn)+"/"+string(Baseline)].Unsafe,
		"type_specific_mutant_unsafe":   byKey[string(TypeSpecific)+"/"+string(MissingLockUpdate)].Unsafe,
		"directed_edge_off_mutant_safe": !byKey[string(DirectedOff)+"/"+string(MissingLockUpdate)].Unsafe,
		"directed_edge_on_mutant_safe":  !byKey[string(DirectedOn)+"/"+string(MissingLockUpdate)].Unsafe,
	}
	status := "PASS"
	for _, value := range checks {
		if !value {
			status = "FAIL"
		}
	}
	return SuiteResult{Status: status, Cases: cases, Checks: checks}
}

func main() {
	encoded, err := json.MarshalIndent(EvaluateSuite(), "", "  ")
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
