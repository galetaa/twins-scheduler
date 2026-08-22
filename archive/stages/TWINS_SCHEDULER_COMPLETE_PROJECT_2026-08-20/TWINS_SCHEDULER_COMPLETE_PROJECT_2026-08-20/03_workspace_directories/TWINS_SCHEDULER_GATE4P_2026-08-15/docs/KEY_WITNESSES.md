# Key minimized Gate 4′ witnesses

All policies below are exact outputs of the bounded explorer. Full message tokens
are in `witnesses.jsonl`.

## Lock update omitted — type-specific

Observation: `H1=0 | H2=1 | H3=-`  
Delivered messages: 18

```text
view 1:
  PROPOSAL, PREVOTE, PRECOMMIT_QC, PRECOMMIT → {H1,H2}
  COMMIT_QC                                  → {H1}
view 2:
  PROPOSAL, PREVOTE, PRECOMMIT_QC, PRECOMMIT → {H2,H3}
  COMMIT_QC                                  → {H2}
```

`H2` supports both conflicting certificates because the mutant omits the lock,
but terminal evidence is delivered to a different member of each quorum.

## Lock update omitted — one-view delayed commit evidence

Observation: `H1=0 | H2=0 | H3=1`  
Delivered messages: 19

```text
view 1: out/in {H1,H2}; defer COMMIT_QC to H1
view 2: out/in {H1,H3}; deliver view-1 deferred certificate after view 2
```

The same pattern also exposes `WRONG_QC_GUARD`.

## Timeout certificate misclassified

Observation: `H1=0 | H2=1 | H3=-`  
Delivered messages: 14

```text
view 1:
  PROPOSAL, TIMEOUT_QC, PRECOMMIT → {H1,H2}
  PREVOTE                         → {}
  COMMIT_QC                       → {H1}
view 2:
  PROPOSAL, TIMEOUT_QC, PRECOMMIT → {H2,H3}
  PREVOTE                         → {}
  COMMIT_QC                       → {H2}
```

Suppressing `PREVOTE` is essential: otherwise normal `PRECOMMIT_QC` evidence
locks the voters. This is why terminal delay alone does not expose the mutant.

## Duplicate signer counting — replay

Observation: `H1=0 | H2=1 | H3=-`  
Delivered messages: 14

In each view one proposal reaches one honest replica. Its one `PREVOTE` and one
`PRECOMMIT` are each delivered twice. The mutant counts two message instances
as two honest voters; together with the Byzantine leader's logical vote, this
forms a false quorum of three.

## Validation omission positive control

Observation: `H1=1 | H2=1 | H3=0`  
Delivered messages: 13

```text
view 1 partition: leader T0 connected only to H3
  H3 accepts a forged one-signer COMMIT_QC for 0
view 2 partition: leader T1 connected to H1,H2
  H1 and H2 form and receive a valid certificate for 1
```

This bug is visible in the weakest grammar and demonstrates that scheduler
expressiveness is not used as a universal explanation for every violation.
