# Terminal-delay boundary

## Question

Can temporal control replace phase/type control?

## Positive boundary

For phase-coupled witnesses where the message coupled with enabling evidence is
terminal or repair evidence, one-view delay is sufficient under three explicit
conditions:

1. the enabling message is delivered in the original view;
2. the terminal/repair message can remain pending until the conflicting branch
   has completed;
3. delaying it does not suppress another message required by that branch.

Under these conditions, the delayed directed grammar reaches the same unsafe
observation as the phase-specific grammar. Immediate-delivery closure destroys
the witness.

Both locking kernels satisfy this boundary for:

- persistent-lock omission;
- an incorrect justification/valid-round guard.

## Negative boundary

Temporal control does not generally replace phase discrimination. The Gate 4′
timeout-classification defect requires the scheduler to suppress one incoming
quorum-forming phase while admitting another on the same endpoint edge. Delaying
only terminal evidence cannot express that distinction.

## Consequence

Scheduler capabilities form multiple axes rather than one total scale:

- endpoint direction;
- phase/type discrimination;
- message-instance choice;
- cross-view delay;
- replay.

`G_D1` and `G_T` are therefore intentionally incomparable in the formal model.
