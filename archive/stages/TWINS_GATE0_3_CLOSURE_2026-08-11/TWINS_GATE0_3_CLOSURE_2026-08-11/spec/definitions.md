# Gate 1 — Executable minimum formal model

## 1. Protocol class used by the pilot

A protocol identity has a deterministic local transition function. The diagnostic instance has one faulty leader identity and three correct replicas. A correct leader branch:

1. accepts one explicit input value;
2. emits an authenticated `PROPOSE(value)`;
3. after receiving a matching correct vote, emits `COMMIT(value, vote-reference)`.

A correct replica accepts its first valid proposal, locks/votes the value and decides only after a matching causally valid commit. The quorum is deliberately weak, so two equivocated branches can violate agreement. This is a diagnostic transition system, not a claim of production BFT safety.

## 2. Validity predicate

A message is valid only when:

- its sender identity is authenticated;
- the value belongs to the configured finite domain;
- a commit cites a proposal branch and at least one matching correct vote;
- a correct replica decides only the value it previously locked.

No malformed bytes, forged correct identity or arbitrary internal-state assertion is admitted.

## 3. Fault models

### `AB` — accepted-message Byzantine

The adversary selects any finite set of validator-admissible leader histories and selectively delivers their valid messages. It does not need to execute the leader transition function internally.

### `AE` — dynamic state equivocation

The adversary may copy correct reachable leader states and run every copy with the deterministic transition function. In the bounded instance this is exactly the set of finite subsets of distinct input-value histories.

### `AT_total(k)` — total persistent clone cap

At most `k` distinct correct-code clone histories may exist over the entire execution. In the pilot this permits at most `k` distinct input-value branches.

### `AT_active(k)` — reusable active-slot cap

At most `k` physical slots are simultaneously active, but a slot may stop, restart/replay from genesis or restore a reachable snapshot. With unbounded message delay, `AT_active(1)` can generate all finite branches sequentially.

## 4. Network

- asynchronous;
- arbitrary finite delay and reordering;
- clone-specific delivery;
- emitted messages may remain undelivered;
- no fairness, GST, timeout or real-time deadline;
- physical clone IDs are not protocol observations.

## 5. Observations

For each labeled correct replica:

- `N`: no relevant proposal received;
- `P(v)`: proposal `v` received and locked/voted, but no commit received;
- `D(v)`: a matching commit received and `v` decided.

The primary finite observation is the tuple of these statuses. Agreement is violated when at least two distinct values occur in `D` statuses.

## 6. Exact finite languages

For value domain `V` and adversary `A`, `L_A(V)` is the set of all reachable primary observations. `Unsafe_A(V)` is its agreement-violating subset.

The explicit-state explorer enumerates every reachable protocol state for every allowed branch set. A separately implemented closed-form quotient enumerates the product of `N`, `P(v)` and `D(v)` statuses. Equality of the two languages is asserted for every branch set.

## 7. Resource measures

For an observation `o`:

- `width(o)` is the number of distinct branch values appearing in `P` or `D` statuses;
- `k_min_total(o)=width(o)` in this diagnostic protocol;
- `k_min_active(o)=0` for the empty observation and `1` otherwise under reusable replay.

The split is mandatory. Referring simply to “number of active clones” is insufficient for a theorem.
