# Independent proof audit — reconstructed from the conversation

**Date represented in the user-provided report:** 19 August 2026  
**Provenance:** reconstructed from the full report pasted into the conversation. The separately referenced original Markdown file, Python script, script output, and checksum file were not present in the active runtime when this bundle was built.

## Verdict

**CONDITIONAL PASS / REVISION REQUIRED.** No counterexample to the central result was found, but four formal revisions were required before unconditional sign-off.

## T2 — relational closure lifting

The independent derivation confirmed the prefix-induction argument under four premises:

1. initial relation;
2. inserted actions are relation-increasing;
3. retained actions satisfy forward simulation;
4. unsafety is upward-closed.

The reported exhaustive two-state check found 264 premise-satisfying cases with an unsafe original terminal state and zero counterexamples. Removing any one premise produced a counterexample.

## T3 — quorum-pivot separation

The quorum arithmetic was confirmed:

\[
|Q_0|=|Q_1|=f+f+1=2f+1=q,
\qquad
Q_0\cap Q_1=B\cup\{p\}.
\]

Without the honest pivot, either branch has only \(2f=q-1\) participants. The independently reconstructed operational order was:

\[
E < \text{first certificate opportunity} < R < \text{second certificate opportunity}.
\]

The audit required the paper and formal model to state explicitly that:

- \(E\) and \(R\) use the same endpoint and the same view;
- when the directed edge is enabled, \(R\) is processed before the second certificate opportunity;
- the bounded \(G_D\) domain is exhausted by the two edge-bit choices;
- conflicting certificates transition to two distinct decisions by correct replicas.

## T6 — seven-premise boundary

The audit independently reconstructed the operational Boolean outcome:

\[
U(e,r)=
(\neg S_1\lor e)
\land
\left[
\neg S_2
\lor
\left(
(\neg R_q\lor e)
\land
\neg(r\land D\land T)
\right)
\right].
\]

Strict separation was defined as:

\[
X\land E_d\land U(1,0)\land\neg U(0,0)\land\neg U(1,1),
\]

which simplifies to:

\[
S_2\land D\land T\land E_d\land X\land(S_1\lor R_q).
\]

The complete 128-assignment enumeration produced exactly:

```text
0111111
1101111
1111111
```

## T1 — replay erasure

The audit identified a missing future-noninterference condition. A duplicate can leave the immediately relevant projection unchanged while modifying hidden state later read by another message. The counterexample used traces `X, X, Y` and `X, Y`.

A sufficient repair was to define a relevant-state projection \(\pi:S\to S_{rel}\), including processed stable keys, and require projection congruence:

\[
\pi(s)=\pi(t)
\Longrightarrow
\pi(\delta(s,m))=\pi(\delta(t,m)),
\]

plus duplicate stuttering for an already processed key:

\[
\pi(\delta(s,m))=\pi(s)
\]

with no protocol-relevant output.

## Required revisions recorded by the audit

1. Add the explicit phase-ordered transition system for T3.
2. Replace the informal T1 future-behavior premise with projection congruence/noninterference.
3. Include the operational equations for T6 in the manuscript.
4. Separately check the authors' SMT, Lean, and executable artifacts.
