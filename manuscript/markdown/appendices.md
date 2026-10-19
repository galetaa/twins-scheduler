# Complexity of coarse witness reachability

In the unweighted independent-pivot schema, the decision problem of whether a coarse unsafe execution exists is NP-complete when the number of pivots is unbounded and the finite opportunity order is represented explicitly by its events and precedence or cover edges. A certificate consists of an open set, a reusable set and a topological event order; checking admission, ordering and quorum support takes polynomial time.

For hardness, take an undirected graph on $k$ vertices and an independent-set target $t$. Introduce repairs $R_i$ and second-vote opportunities $V_i$. For every undirected edge $\{i,j\}$ impose $R_i\prec V_j$ and $R_j\prec V_i$. These constraints are acyclic: they point from the repair layer to the vote layer. The fixed prefix and certificate collectors can be added before and after those layers. The resulting repair graph is the symmetric orientation of the original graph. Its induced set is acyclic exactly when it is independent, since each undirected edge creates a directed two-cycle.

Set $d_0=k,d_1=t$. Theorem 3 gives coarse unsafe reachability exactly when $\alpha(H)\ge t$, which is the independent-set question. This uses the classical relation between node cover, feedback node sets, and symmetrized graphs \cite{karp1972reducibility}. It is a complexity statement about the declared opportunity schema. It neither establishes a complexity bound for the fixed four-validator trace nor claims that every constructed order is realizable by a production consensus implementation.

# Supporting replay and diagnostic results

## Replay erasure with outputs

Let $\pi:S\to S_{\mathrm{rel}}$ project relevant state, including processed message keys. For every retained message $m$, require **state congruence** and **output congruence**:

$$
\pi(s)=\pi(t)\Rightarrow
\pi(\delta(s,m))=\pi(\delta(t,m)),
\qquad
\pi(s)=\pi(t)\Rightarrow \mathsf{out}(s,m)=\mathsf{out}(t,m).
$$

For an exact marked duplicate whose key was already processed, require projected stutter $\pi(\delta(s,m))=\pi(s)$ and output silence $\mathsf{out}(s,m)=\epsilon$.

**Supporting proposition (replay erasure).** Deleting all marked duplicates preserves the terminal relevant projection and the complete relevant output trace under these conditions.

**Proof.** Maintain equality of the two current projections and accumulated outputs. A duplicate changes neither on the unerased side. At a retained message, the two congruences preserve the invariant. Induction gives the terminal claim. $\square$

Projected silence alone is insufficient: in a trace $X,X,Y$, the duplicate can change a hidden bit that the later $Y$ copies into relevant state or output. The artifact retains these negative controls. This proposition is standard congruence reasoning; it supports the distinction between internal state and persistent outputs without constituting the revised paper's main contribution.

## The earlier seven-flag diagnostic

For Boolean flags $S_1,S_2,R_q,D,T,E_d,X$, the earlier operational abstraction uses

$$
U(e,r)=(\neg S_1\lor e)\land
[\neg S_2\lor((\neg R_q\lor e)\land\neg(r\land D\land T))].
$$

Here the shortage flags describe the two bases; $R_q$ makes second participation enabling-dependent; $D$ gives repair efficacy; $T$ means repair precedes the **second-vote opportunity**; $E_d$ couples the endpoint key; and $X$ permits phase distinction. Direct substitution yields

$$
X\land E_d\land U(1,0)\land\neg U(0,0)\land\neg U(1,1)
\quad\Longleftrightarrow\quad
S_2\land D\land T\land E_d\land X\land(S_1\lor R_q).
$$

Exactly three of the 128 assignments satisfy this expression. This is a diagnostic of that Boolean machine. The old atomic opportunity interpretation combined vote and certificate formation; it must not be reused to infer that repair merely before a later collector suffices. The revised frontier model separates these events and makes initially ready pivots the primary multi-pivot case.
