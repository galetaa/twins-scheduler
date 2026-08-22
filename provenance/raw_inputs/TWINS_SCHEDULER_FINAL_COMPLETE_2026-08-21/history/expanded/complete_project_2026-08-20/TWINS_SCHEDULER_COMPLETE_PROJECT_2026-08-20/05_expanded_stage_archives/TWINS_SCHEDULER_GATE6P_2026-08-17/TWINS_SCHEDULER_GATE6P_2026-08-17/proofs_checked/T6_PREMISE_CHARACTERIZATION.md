# T6 — Exact premise characterization for the supplied Boolean construction

Seven binary flags encode whether the two-branch quorum-pivot construction has
particular structural properties. All `2^7=128` assignments were evaluated
exactly.

In field order

1. first base short by one;
2. second base short by one;
3. second pivot requires enabling evidence;
4. repair disables pivot;
5. repair precedes the second quorum opportunity;
6. enabling and repair share one endpoint edge;
7. the phase-specific grammar can split enabling and repair;

the only strict-separation patterns are:

```text
0111111
1101111
1111111
```

Equivalently, strict separation holds exactly when

```text
second_base_short_by_one
AND repair_disables_pivot
AND repair_precedes_second_quorum_opportunity
AND enabling_and_repair_share_endpoint_edge
AND phase_specific_grammar_can_split_E_and_R
AND (first_base_short_by_one
     OR second_pivot_requires_enabling_evidence)
```

Thus five premises are globally necessary inside this Boolean model. Neither
`first_base_short_by_one` nor
`second_pivot_requires_enabling_evidence` is individually necessary, but at
least one of them is.

This result must not be generalized to all BFT protocols. It characterizes the
small construction used to expose the scheduler-closure mechanism and supplies
a precise target for future protocol-class generalization.
