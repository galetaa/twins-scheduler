# relab/hotstuff source verification for Gate 4′

**Verification date:** 2026-08-15  
**Repository:** `relab/hotstuff`  
**Pinned commit:** `3179c6e62929294961acbfd9bf8445769716a121`  
**Branch status at verification:** the official `main` history still identified
this commit as the latest visible commit.

## Pinned files

| File | Local SHA-256 |
|---|---|
| `network.go` | `4419845a04729c23ba31cd2fb37daf792e1c1a10fba32f29163f60c6506f3c55` |
| `scenario.go` | `8eea5dcc18e499920eaafd8b8f3ca62c81adf57387e283b30ff8621fdbdaf72d` |
| `sender.go` | `961cc8bd8bc0ff0c11751b8086a7c07d96dca570c8dc48ec254d69343edb3ce8` |
| `generator.go` | `6049de543e1d683d40ba2932cfb877397e3e26ea48ab87c599d8c9db8ce41b61` |
| `twins.md` | `9ae2fb3c05cc2749a82cef4b6c5f59e3e06812c9f9c335d089a6537bf762545c` |

The files are stored under `inputs/hotstuff_snapshot/`. The upstream license is
stored beside them.

## Extracted operational facts

1. `shouldDrop` indexes the scenario by the **sender's effective view**.
2. Views below one bypass filtering.
3. Messages from a view beyond the configured scenario are dropped.
4. Within a configured view, sender and receiver in one partition bypass the
   drop-type test.
5. Across partitions, only configured runtime message types are dropped.
6. An admitted message retains its sender view in `pendingMessages`.
7. `tick` delivers pending messages whose view is not greater than `globalView`.
8. `globalView` advances only when a tick delivers no pending message.

## Comment/code discrepancy

`scenario.go` says timeout and new-view messages are permitted, but the actual
`NewPartitionedNetwork` call includes `NewViewMsg` and `TimeoutMsg` among the
controlled types. Gate 4′ treats executable code as authoritative.

## Executable conformance scope

`conformance/go_harness/main.go` is a dependency-free extraction of items 1–8.
It was compared extensionally with `conformance/python_harness.py` on six fixed
edge cases and 128 seeded random cases. The check does **not** execute consensus
node event loops, proposal formation, voting logic, or commit checking. It
therefore supports only the mapping of network admission and pending-queue
semantics.
