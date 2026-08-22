from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Iterable, Protocol

from schedcheck.model import Message
from schedcheck.partitions import set_partitions


class StaticPolicy(Protocol):
    grammar: str

    def allows(self, message: Message) -> bool:
        ...

    def schedule_id(self) -> str:
        ...

    def schedule_data(self) -> tuple[tuple[str, str], ...]:
        ...


@dataclass(frozen=True, slots=True)
class PartitionPolicy:
    blocks: tuple[tuple[str, ...], ...]
    grammar: str = "G_P_PARTITION"

    def allows(self, message: Message) -> bool:
        return any(message.sender in block and message.receiver in block for block in self.blocks)

    def schedule_id(self) -> str:
        return "/".join("{" + ",".join(block) + "}" for block in self.blocks)

    def schedule_data(self) -> tuple[tuple[str, str], ...]:
        return (("blocks", self.schedule_id()),)


@dataclass(frozen=True, slots=True)
class DirectedPolicy:
    edges: frozenset[tuple[str, str]]
    grammar: str = "G_D_DIRECTED_VIEW"

    def allows(self, message: Message) -> bool:
        return message.edge in self.edges

    def schedule_id(self) -> str:
        if not self.edges:
            return "EMPTY"
        return ",".join(f"{s}>{r}" for s, r in sorted(self.edges))

    def schedule_data(self) -> tuple[tuple[str, str], ...]:
        return (("edges", self.schedule_id()),)


@dataclass(frozen=True, slots=True)
class TypeSpecificPolicy:
    type_edges: frozenset[tuple[str, str, str]]
    grammar: str = "G_T_TYPE_SPECIFIC"

    def allows(self, message: Message) -> bool:
        return message.type_edge in self.type_edges

    def schedule_id(self) -> str:
        if not self.type_edges:
            return "EMPTY"
        return ",".join(f"{kind}:{s}>{r}" for kind, s, r in sorted(self.type_edges))

    def schedule_data(self) -> tuple[tuple[str, str], ...]:
        return (("type_edges", self.schedule_id()),)


def powerset(items: tuple[tuple[str, str], ...]) -> Iterable[frozenset[tuple[str, str]]]:
    for mask in range(1 << len(items)):
        yield frozenset(items[index] for index in range(len(items)) if mask & (1 << index))


def partition_policies(nodes: tuple[str, ...]) -> tuple[PartitionPolicy, ...]:
    return tuple(PartitionPolicy(blocks) for blocks in set_partitions(nodes))


def directed_policies(edges: tuple[tuple[str, str], ...]) -> Iterable[DirectedPolicy]:
    for edge_set in powerset(edges):
        yield DirectedPolicy(edge_set)


def type_specific_policies(
    message_types: tuple[str, ...],
    edges: tuple[tuple[str, str], ...],
) -> Iterable[TypeSpecificPolicy]:
    atoms = tuple((kind, sender, receiver) for kind, (sender, receiver) in product(message_types, edges))
    for mask in range(1 << len(atoms)):
        yield TypeSpecificPolicy(
            frozenset(atoms[index] for index in range(len(atoms)) if mask & (1 << index))
        )
