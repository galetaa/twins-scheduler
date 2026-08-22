package main

import (
	"encoding/json"
	"fmt"
)

type VoteKey struct {
	Validator string
	Round     int
	Phase     string
	Value     int
}

type UniqueVoteSet struct {
	seen map[VoteKey]struct{}
}

func NewUniqueVoteSet() *UniqueVoteSet {
	return &UniqueVoteSet{seen: make(map[VoteKey]struct{})}
}

// Add mirrors the relevant CometBFT contract: a duplicate logical vote is not
// added and does not increase quorum weight.
func (s *UniqueVoteSet) Add(v VoteKey) bool {
	if _, ok := s.seen[v]; ok {
		return false
	}
	s.seen[v] = struct{}{}
	return true
}

func (s *UniqueVoteSet) HonestCount() int { return len(s.seen) }

type InstanceVoteSet struct {
	count int
}

func (s *InstanceVoteSet) Add(_ VoteKey) bool {
	s.count++
	return true
}

func (s *InstanceVoteSet) HonestCount() int { return s.count }

func HasQuorum(honestReceipts int) bool {
	// One Byzantine proposer contribution plus two honest validator identities.
	return 1+honestReceipts >= 3
}

type Replica struct {
	LockedValue  *int
	LockedRound  int
	Precommitted bool
}

// EnterPrecommitBaseline captures the source-level ordering checked in the
// pinned CometBFT snapshot: establish/update the lock before emitting the
// precommit action.
func EnterPrecommitBaseline(r Replica, value, round int) Replica {
	v := value
	r.LockedValue = &v
	r.LockedRound = round
	r.Precommitted = true
	return r
}

// EnterPrecommitMissingLock is a controlled local mutation used only in this
// fixture. It emits the same abstract precommit but omits persistent lock state.
func EnterPrecommitMissingLock(r Replica, _ int, _ int) Replica {
	r.Precommitted = true
	return r
}

func CanSupport(r Replica, value int) bool {
	return r.LockedValue == nil || *r.LockedValue == value
}

type Result struct {
	UniqueFirstAdded              bool `json:"unique_first_added"`
	UniqueReplayAdded             bool `json:"unique_replay_added"`
	UniqueQuorumAfterReplay       bool `json:"unique_quorum_after_replay"`
	InstanceQuorumAfterReplay     bool `json:"instance_quorum_after_replay"`
	BaselineLockedBeforePrecommit bool `json:"baseline_locked_before_precommit"`
	BaselineRejectsConflict       bool `json:"baseline_rejects_conflict"`
	MutationSupportsConflict      bool `json:"mutation_supports_conflict"`
}

func Evaluate() Result {
	vote := VoteKey{Validator: "H1", Round: 1, Phase: "PREVOTE", Value: 0}
	unique := NewUniqueVoteSet()
	first := unique.Add(vote)
	replay := unique.Add(vote)
	instances := &InstanceVoteSet{}
	instances.Add(vote)
	instances.Add(vote)

	base := EnterPrecommitBaseline(Replica{LockedRound: -1}, 0, 1)
	mutant := EnterPrecommitMissingLock(Replica{LockedRound: -1}, 0, 1)
	return Result{
		UniqueFirstAdded:              first,
		UniqueReplayAdded:             replay,
		UniqueQuorumAfterReplay:       HasQuorum(unique.HonestCount()),
		InstanceQuorumAfterReplay:     HasQuorum(instances.HonestCount()),
		BaselineLockedBeforePrecommit: base.Precommitted && base.LockedValue != nil && *base.LockedValue == 0 && base.LockedRound == 1,
		BaselineRejectsConflict:       !CanSupport(base, 1),
		MutationSupportsConflict:      CanSupport(mutant, 1),
	}
}

func main() {
	encoded, err := json.MarshalIndent(Evaluate(), "", "  ")
	if err != nil {
		panic(err)
	}
	fmt.Println(string(encoded))
}
