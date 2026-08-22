package main

import "testing"

func TestReplayIdempotenceBoundary(t *testing.T) {
	result := Evaluate()
	if !result.UniqueFirstAdded {
		t.Fatal("first logical vote must be added")
	}
	if result.UniqueReplayAdded {
		t.Fatal("duplicate logical vote must be rejected")
	}
	if result.UniqueQuorumAfterReplay {
		t.Fatal("deduplicated vote set must not reach quorum")
	}
	if !result.InstanceQuorumAfterReplay {
		t.Fatal("instance-counting mutation should reach a spurious quorum")
	}
}

func TestLockBeforePrecommitBoundary(t *testing.T) {
	result := Evaluate()
	if !result.BaselineLockedBeforePrecommit {
		t.Fatal("baseline must establish the lock before the precommit action")
	}
	if !result.BaselineRejectsConflict {
		t.Fatal("baseline lock must suppress a conflicting later action")
	}
	if !result.MutationSupportsConflict {
		t.Fatal("controlled lock-omission mutation must leave the conflict enabled")
	}
}
