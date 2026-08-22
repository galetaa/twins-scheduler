package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
)

type Variant string
type Grammar string

const (
	Baseline      Variant = "BASELINE"
	MissingLock   Variant = "MISSING_LOCK_UPDATE"
	PhaseSpecific Grammar = "G_T_PHASE_SPECIFIC"
	DirectedOff   Grammar = "G_D_EDGE_OFF"
	DirectedOn    Grammar = "G_D_EDGE_ON"
)

type Result struct {
	F                  int     `json:"f"`
	N                  int     `json:"n"`
	Q                  int     `json:"q"`
	Variant            Variant `json:"variant"`
	Grammar            Grammar `json:"grammar"`
	EDelivered         bool    `json:"E_delivered"`
	RDelivered         bool    `json:"R_delivered"`
	Certificate0       bool    `json:"certificate0"`
	Certificate1       bool    `json:"certificate1"`
	LeftDecision       *int    `json:"left_decision"`
	RightDecision      *int    `json:"right_decision"`
	PivotLockedValue   *int    `json:"pivot_locked_value"`
	PivotDecidedValue  *int    `json:"pivot_decided_value"`
	AgreementViolation bool    `json:"agreement_violation"`
}

func ptr(v int) *int { return &v }
func admissions(g Grammar) (bool, bool) {
	switch g {
	case PhaseSpecific:
		return true, false
	case DirectedOff:
		return false, false
	case DirectedOn:
		return true, true
	default:
		panic("unknown grammar")
	}
}

func execute(f int, variant Variant, grammar Grammar) Result {
	if f < 1 {
		panic("f must be positive")
	}
	n, q := 3*f+1, 2*f+1
	base0, base1 := 2*f, 2*f
	e, r := admissions(grammar)
	height := 1
	locked := false
	decided := false
	emitted0 := false
	if e {
		emitted0 = true
		if variant == Baseline {
			locked = true
		}
	}
	cert0 := base0+boolInt(emitted0) >= q
	var d0 *int
	if cert0 {
		d0 = ptr(0)
	}
	if r && e {
		decided = true
		height = 2
	}
	available1 := height == 1 && !decided && !locked
	cert1 := base1+boolInt(available1) >= q
	var d1 *int
	if cert1 {
		d1 = ptr(1)
	}
	var lockedVal, decidedVal *int
	if locked {
		lockedVal = ptr(0)
	}
	if decided {
		decidedVal = ptr(0)
	}
	return Result{f, n, q, variant, grammar, e, r, cert0, cert1, d0, d1, lockedVal, decidedVal, cert0 && cert1}
}
func boolInt(b bool) int {
	if b {
		return 1
	}
	return 0
}

func repositoryRoot() string {
	current, err := os.Getwd()
	if err != nil {
		panic(err)
	}
	for {
		if _, err := os.Stat(filepath.Join(current, "go.mod")); err == nil {
			return current
		}
		parent := filepath.Dir(current)
		if parent == current {
			panic("could not locate repository root containing go.mod")
		}
		current = parent
	}
}

func main() {
	variants := []Variant{Baseline, MissingLock}
	grammars := []Grammar{PhaseSpecific, DirectedOff, DirectedOn}
	rows := make([]Result, 0, 64*6)
	for f := 1; f <= 64; f++ {
		local := map[string]Result{}
		for _, v := range variants {
			for _, g := range grammars {
				x := execute(f, v, g)
				rows = append(rows, x)
				local[string(v)+"/"+string(g)] = x
			}
		}
		for _, g := range grammars {
			if local[string(Baseline)+"/"+string(g)].AgreementViolation {
				panic("baseline unsafe")
			}
		}
		if !local[string(MissingLock)+"/"+string(PhaseSpecific)].AgreementViolation {
			panic("missing separation")
		}
		if local[string(MissingLock)+"/"+string(DirectedOff)].AgreementViolation || local[string(MissingLock)+"/"+string(DirectedOn)].AgreementViolation {
			panic("directed unsafe")
		}
	}
	root := repositoryRoot()
	if configured := os.Getenv("TWINS_OUTPUT_ROOT"); configured != "" {
		root = configured
	}
	out := filepath.Join(root, "results", "generated")
	if err := os.MkdirAll(out, 0o755); err != nil {
		panic(err)
	}
	blob, _ := json.MarshalIndent(rows, "", "  ")
	if err := os.WriteFile(filepath.Join(out, "cometbft_refinement_results_go.json"), append(blob, '\n'), 0o644); err != nil {
		panic(err)
	}
	fmt.Println("COMETBFT_GO_REFINEMENT PASS")
	fmt.Printf("cases=%d f=1..64\n", len(rows))
}
