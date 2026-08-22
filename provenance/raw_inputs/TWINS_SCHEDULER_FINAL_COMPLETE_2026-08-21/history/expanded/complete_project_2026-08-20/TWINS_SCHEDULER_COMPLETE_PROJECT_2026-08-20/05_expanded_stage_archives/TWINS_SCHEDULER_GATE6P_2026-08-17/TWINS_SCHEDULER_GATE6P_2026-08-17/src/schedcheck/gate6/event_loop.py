from __future__ import annotations

"""Independent Python model of the Gate 6' fuller consensus event loop.

The model intentionally does not import the Gate 4'/5' kernels.  It mirrors the
small Go fixture at the semantic boundary needed by the paper:

* two rounds and two conflicting values;
* proposal -> prevote -> POLKA -> precommit -> COMMIT;
* stable logical vote keys;
* persistent lock update in the baseline;
* one controlled missing-lock mutation;
* three scheduler policies for the same B -> pivot edge in round zero.

FIFO is used for Go/Python conformance.  Seeded random and LIFO queue selection
are used only for bounded event-order sensitivity; all choices preserve causal
generation because an event can be selected only after it has been enqueued.
"""

from dataclasses import asdict, dataclass, field
from random import Random
from typing import Literal

Phase = Literal["PROPOSAL", "PREVOTE", "POLKA", "PRECOMMIT", "COMMIT"]
Grammar = Literal[
    "G_T_TYPE_SPECIFIC",
    "G_D_ROUND0_EDGE_OFF",
    "G_D_ROUND0_EDGE_ON",
]
Mutation = Literal["BASELINE", "MISSING_LOCK_UPDATE"]
Strategy = Literal["fifo", "lifo", "random"]

GRAMMARS: tuple[Grammar, ...] = (
    "G_T_TYPE_SPECIFIC",
    "G_D_ROUND0_EDGE_OFF",
    "G_D_ROUND0_EDGE_ON",
)
MUTATIONS: tuple[Mutation, ...] = ("BASELINE", "MISSING_LOCK_UPDATE")


@dataclass(frozen=True, slots=True)
class Message:
    from_: str
    to: str
    round: int
    value: int
    phase: Phase

    def json(self) -> dict[str, object]:
        return {
            "from": self.from_,
            "to": self.to,
            "round": self.round,
            "value": self.value,
            "phase": self.phase,
        }


@dataclass(slots=True)
class Replica:
    name: str
    locked: bool = False
    locked_value: int = 0
    locked_round: int = -1
    decided: bool = False
    decision: int = -1


VoteKey = tuple[str, int, int, Phase]


@dataclass(slots=True)
class LeaderRound:
    prevotes: set[VoteKey] = field(default_factory=set)
    precommits: set[VoteKey] = field(default_factory=set)
    polka_emitted: bool = False
    commit_emitted: bool = False


class EventLoop:
    def __init__(
        self,
        grammar: Grammar,
        mutation: Mutation,
        *,
        strategy: Strategy = "fifo",
        seed: int = 0,
    ) -> None:
        if grammar not in GRAMMARS:
            raise ValueError(f"unsupported grammar: {grammar}")
        if mutation not in MUTATIONS:
            raise ValueError(f"unsupported mutation: {mutation}")
        if strategy not in ("fifo", "lifo", "random"):
            raise ValueError(f"unsupported queue strategy: {strategy}")
        self.grammar = grammar
        self.mutation = mutation
        self.strategy = strategy
        self.quorum = 3
        self.queue: list[Message] = []
        self.replicas = {
            name: Replica(name=name) for name in ("H1", "P", "H3")
        }
        self.leader: dict[int, LeaderRound] = {}
        self.log: list[dict[str, object]] = []
        self.rng = Random(seed)

    def _record(
        self, action: str, message: Message | None, detail: str
    ) -> None:
        row: dict[str, object] = {
            "index": len(self.log),
            "action": action,
            "detail": detail,
        }
        if message is not None:
            row["message"] = message.json()
        self.log.append(row)

    def _allow(self, message: Message) -> bool:
        if (
            message.round != 0
            or message.from_ != "B"
            or message.to != "P"
        ):
            return True
        if self.grammar == "G_T_TYPE_SPECIFIC":
            return message.phase != "COMMIT"
        if self.grammar == "G_D_ROUND0_EDGE_OFF":
            return False
        if self.grammar == "G_D_ROUND0_EDGE_ON":
            return True
        raise AssertionError("unreachable grammar")

    def _enqueue(self, message: Message) -> None:
        self.queue.append(message)
        self._record(
            "ENQUEUE", message, "message entered deterministic event loop"
        )

    def _round_state(self, round_: int) -> LeaderRound:
        if round_ not in self.leader:
            self.leader[round_] = LeaderRound()
        return self.leader[round_]

    @staticmethod
    def _can_support(replica: Replica, value: int) -> bool:
        if replica.decided and replica.decision != value:
            return False
        return not replica.locked or replica.locked_value == value

    @staticmethod
    def _proposal_targets(round_: int) -> tuple[str, ...]:
        return ("H1", "P") if round_ == 0 else ("P", "H3")

    def start_round(self, round_: int, value: int) -> None:
        state = self._round_state(round_)
        state.prevotes.add(("B", round_, value, "PREVOTE"))
        self._record("ROUND_START", None, f"round={round_} value={value}")
        for target in self._proposal_targets(round_):
            self._enqueue(
                Message("B", target, round_, value, "PROPOSAL")
            )
        self.drain()

    def _select_queue_index(self) -> int:
        if self.strategy == "fifo":
            return 0
        if self.strategy == "lifo":
            return len(self.queue) - 1
        return self.rng.randrange(len(self.queue))

    def drain(self) -> None:
        while self.queue:
            index = self._select_queue_index()
            message = self.queue.pop(index)
            if not self._allow(message):
                self._record(
                    "DROP", message, "blocked by selected scheduler grammar"
                )
                continue
            self._record(
                "DELIVER", message, f"delivered by {self.strategy} scheduler"
            )
            self._handle(message)

    def _handle(self, message: Message) -> None:
        if message.to == "B":
            self._handle_leader(message)
            return
        try:
            replica = self.replicas[message.to]
        except KeyError as exc:
            raise AssertionError("message addressed to unknown replica") from exc

        if message.phase == "PROPOSAL":
            if not self._can_support(replica, message.value):
                self._record(
                    "REJECT",
                    message,
                    "proposal conflicts with persistent lock or decision",
                )
                return
            self._enqueue(
                Message(
                    replica.name,
                    "B",
                    message.round,
                    message.value,
                    "PREVOTE",
                )
            )
            return

        if message.phase == "POLKA":
            if not self._can_support(replica, message.value):
                self._record(
                    "REJECT",
                    message,
                    "POLKA conflicts with persistent lock or decision",
                )
                return
            if self.mutation == "BASELINE":
                replica.locked = True
                replica.locked_value = message.value
                replica.locked_round = message.round
                self._record(
                    "STATE",
                    None,
                    f"{replica.name} locks value={message.value} "
                    f"round={message.round}",
                )
            else:
                self._record(
                    "MUTATION",
                    None,
                    f"{replica.name} omits persistent lock update",
                )
            self._enqueue(
                Message(
                    replica.name,
                    "B",
                    message.round,
                    message.value,
                    "PRECOMMIT",
                )
            )
            return

        if message.phase == "COMMIT":
            if replica.decided and replica.decision != message.value:
                self._record(
                    "REJECT",
                    message,
                    "terminal evidence conflicts with irreversible decision",
                )
                return
            if not replica.decided:
                replica.decided = True
                replica.decision = message.value
                self._record(
                    "STATE",
                    None,
                    f"{replica.name} decides value={message.value} "
                    f"round={message.round}",
                )
            return

        raise AssertionError(f"replica received unexpected phase {message.phase}")

    def _add_unique(self, target: set[VoteKey], message: Message) -> bool:
        key: VoteKey = (
            message.from_,
            message.round,
            message.value,
            message.phase,
        )
        if key in target:
            self._record(
                "DUPLICATE", message, "stable logical vote already counted"
            )
            return False
        target.add(key)
        return True

    @staticmethod
    def _support_count(
        votes: set[VoteKey], round_: int, value: int, phase: Phase
    ) -> int:
        return sum(
            1
            for _, vote_round, vote_value, vote_phase in votes
            if vote_round == round_
            and vote_value == value
            and vote_phase == phase
        )

    def _handle_leader(self, message: Message) -> None:
        state = self._round_state(message.round)
        if message.phase == "PREVOTE":
            self._add_unique(state.prevotes, message)
            count = self._support_count(
                state.prevotes, message.round, message.value, "PREVOTE"
            )
            if not state.polka_emitted and count >= self.quorum:
                state.polka_emitted = True
                state.precommits.add(
                    ("B", message.round, message.value, "PRECOMMIT")
                )
                self._record(
                    "CERTIFICATE",
                    None,
                    f"POLKA formed round={message.round} value={message.value}",
                )
                for target in self._proposal_targets(message.round):
                    self._enqueue(
                        Message(
                            "B", target, message.round, message.value, "POLKA"
                        )
                    )
            return

        if message.phase == "PRECOMMIT":
            self._add_unique(state.precommits, message)
            count = self._support_count(
                state.precommits,
                message.round,
                message.value,
                "PRECOMMIT",
            )
            if not state.commit_emitted and count >= self.quorum:
                state.commit_emitted = True
                self._record(
                    "CERTIFICATE",
                    None,
                    f"COMMIT formed round={message.round} value={message.value}",
                )
                for target in self._proposal_targets(message.round):
                    self._enqueue(
                        Message(
                            "B", target, message.round, message.value, "COMMIT"
                        )
                    )
            return

        raise AssertionError(f"leader received unexpected phase {message.phase}")

    def result(self) -> dict[str, object]:
        decisions = sorted(
            (
                {"replica": name, "value": replica.decision}
                for name, replica in self.replicas.items()
                if replica.decided
            ),
            key=lambda row: str(row["replica"]),
        )
        values = {int(row["value"]) for row in decisions}
        locks = {
            name: (
                f"{replica.locked_value}@{replica.locked_round}"
                if replica.locked
                else "none"
            )
            for name, replica in self.replicas.items()
        }
        polkas = sorted(
            round_
            for round_, state in self.leader.items()
            if state.polka_emitted
        )
        commits = sorted(
            round_
            for round_, state in self.leader.items()
            if state.commit_emitted
        )
        return {
            "grammar": self.grammar,
            "mutation": self.mutation,
            "unsafe": len(values) > 1,
            "decisions": decisions,
            "locks": locks,
            "polka_rounds": polkas,
            "commit_rounds": commits,
            "log": self.log,
        }


def execute_case(
    grammar: Grammar,
    mutation: Mutation,
    *,
    strategy: Strategy = "fifo",
    seed: int = 0,
) -> dict[str, object]:
    loop = EventLoop(grammar, mutation, strategy=strategy, seed=seed)
    loop.start_round(0, 0)
    loop.start_round(1, 1)
    return loop.result()


def _classification(cases: list[dict[str, object]]) -> dict[str, bool]:
    by_key = {
        f"{case['grammar']}/{case['mutation']}": bool(case["unsafe"])
        for case in cases
    }
    return {
        "all_baselines_safe": all(
            not by_key[f"{grammar}/BASELINE"] for grammar in GRAMMARS
        ),
        "type_specific_mutant_unsafe": by_key[
            "G_T_TYPE_SPECIFIC/MISSING_LOCK_UPDATE"
        ],
        "directed_edge_off_mutant_safe": not by_key[
            "G_D_ROUND0_EDGE_OFF/MISSING_LOCK_UPDATE"
        ],
        "directed_edge_on_mutant_safe": not by_key[
            "G_D_ROUND0_EDGE_ON/MISSING_LOCK_UPDATE"
        ],
    }


def evaluate_suite(
    *, strategy: Strategy = "fifo", seed: int = 0
) -> dict[str, object]:
    cases = [
        execute_case(grammar, mutation, strategy=strategy, seed=seed)
        for mutation in MUTATIONS
        for grammar in GRAMMARS
    ]
    checks = _classification(cases)
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "strategy": strategy,
        "seed": seed,
        "cases": cases,
        "checks": checks,
    }


def canonical_case(case: dict[str, object]) -> dict[str, object]:
    """Fields that must agree across independent implementations."""

    return {
        "grammar": case["grammar"],
        "mutation": case["mutation"],
        "unsafe": case["unsafe"],
        "decisions": case["decisions"],
        "locks": case["locks"],
        "polka_rounds": case["polka_rounds"],
        "commit_rounds": case["commit_rounds"],
    }


def compare_suites(
    left: dict[str, object], right: dict[str, object]
) -> dict[str, object]:
    left_cases = {
        (str(case["grammar"]), str(case["mutation"])): canonical_case(case)
        for case in left["cases"]  # type: ignore[index]
    }
    right_cases = {
        (str(case["grammar"]), str(case["mutation"])): canonical_case(case)
        for case in right["cases"]  # type: ignore[index]
    }
    keys_equal = set(left_cases) == set(right_cases)
    mismatches: list[dict[str, object]] = []
    for key in sorted(set(left_cases) | set(right_cases)):
        if left_cases.get(key) != right_cases.get(key):
            mismatches.append(
                {
                    "grammar": key[0],
                    "mutation": key[1],
                    "left": left_cases.get(key),
                    "right": right_cases.get(key),
                }
            )
    return {
        "status": "PASS" if keys_equal and not mismatches else "FAIL",
        "keys_equal": keys_equal,
        "cases_checked": len(left_cases) if keys_equal else 0,
        "mismatches": mismatches,
    }


def order_sensitivity(
    *, random_seeds: int = 256, first_seed: int = 0
) -> dict[str, object]:
    if random_seeds < 0:
        raise ValueError("random_seeds must be non-negative")
    failures: list[dict[str, object]] = []
    signatures: dict[str, set[str]] = {
        f"{grammar}/{mutation}": set()
        for mutation in MUTATIONS
        for grammar in GRAMMARS
    }

    runs: list[tuple[Strategy, int]] = [("fifo", 0), ("lifo", 0)]
    runs.extend(("random", first_seed + offset) for offset in range(random_seeds))
    for strategy, seed in runs:
        suite = evaluate_suite(strategy=strategy, seed=seed)
        if suite["status"] != "PASS":
            failures.append(
                {"strategy": strategy, "seed": seed, "checks": suite["checks"]}
            )
        for case in suite["cases"]:  # type: ignore[index]
            key = f"{case['grammar']}/{case['mutation']}"
            signature = repr(
                (
                    case["unsafe"],
                    case["decisions"],
                    case["locks"],
                    case["polka_rounds"],
                    case["commit_rounds"],
                )
            )
            signatures[key].add(signature)

    return {
        "status": "PASS" if not failures else "FAIL",
        "queue_strategies": ["fifo", "lifo", "seeded_random"],
        "random_seed_range": (
            [first_seed, first_seed + random_seeds - 1]
            if random_seeds
            else []
        ),
        "runs_checked": len(runs),
        "case_runs_checked": len(runs) * len(GRAMMARS) * len(MUTATIONS),
        "classification_failures": failures,
        "distinct_terminal_signatures_per_case": {
            key: len(values) for key, values in sorted(signatures.items())
        },
        "scope": (
            "bounded causal event-order sensitivity within the supplied two-round "
            "fixture; not a partial-synchrony or liveness result"
        ),
    }
