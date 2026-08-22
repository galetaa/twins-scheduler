package main

import "testing"

func findCase(t *testing.T, suite SuiteResult, grammar Grammar, mutation Mutation) CaseResult {
	t.Helper()
	for _, result := range suite.Cases {
		if result.Grammar == grammar && result.Mutation == mutation {
			return result
		}
	}
	t.Fatalf("case not found: %s/%s", grammar, mutation)
	return CaseResult{}
}

func TestFullEventLoopBoundary(t *testing.T) {
	suite := EvaluateSuite()
	if suite.Status != "PASS" {
		t.Fatalf("suite failed: %+v", suite.Checks)
	}
	mutantTyped := findCase(t, suite, TypeSpecific, MissingLockUpdate)
	if !mutantTyped.Unsafe {
		t.Fatal("phase-specific controlled mutation must violate agreement")
	}
	if findCase(t, suite, DirectedOff, MissingLockUpdate).Unsafe {
		t.Fatal("directed edge-off branch must remain safe")
	}
	if findCase(t, suite, DirectedOn, MissingLockUpdate).Unsafe {
		t.Fatal("directed edge-on branch must remain safe after terminal repair")
	}
}

func TestBaselineSafetyAndMechanism(t *testing.T) {
	suite := EvaluateSuite()
	for _, grammar := range []Grammar{TypeSpecific, DirectedOff, DirectedOn} {
		if findCase(t, suite, grammar, Baseline).Unsafe {
			t.Fatalf("baseline unsafe under %s", grammar)
		}
	}
	typed := findCase(t, suite, TypeSpecific, MissingLockUpdate)
	if typed.Locks["P"] != "none" {
		t.Fatalf("controlled mutation should omit pivot lock, got %s", typed.Locks["P"])
	}
	on := findCase(t, suite, DirectedOn, MissingLockUpdate)
	foundPivotDecision := false
	for _, decision := range on.Decisions {
		if decision.Replica == "P" && decision.Value == 0 {
			foundPivotDecision = true
		}
	}
	if !foundPivotDecision {
		t.Fatal("directed edge-on closure must deliver round-0 terminal evidence to pivot")
	}
}
