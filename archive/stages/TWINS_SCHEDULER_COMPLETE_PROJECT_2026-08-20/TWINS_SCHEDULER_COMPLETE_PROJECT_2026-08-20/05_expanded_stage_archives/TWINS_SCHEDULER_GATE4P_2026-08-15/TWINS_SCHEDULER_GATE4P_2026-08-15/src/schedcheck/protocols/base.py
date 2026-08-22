from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Hashable, Iterable

from schedcheck.model import Message, Observation


class FiniteProtocol(ABC):
    """Deterministic phase-bounded protocol interface used by the exact checker."""

    name: str
    nodes: tuple[str, ...]
    observed_nodes: tuple[str, ...]
    message_types: tuple[str, ...]
    phase_count: int

    @abstractmethod
    def initial_state(self) -> Hashable:
        raise NotImplementedError

    @abstractmethod
    def emit(self, state: Hashable, phase: int) -> tuple[Message, ...]:
        raise NotImplementedError

    @abstractmethod
    def deliver(self, state: Hashable, message: Message) -> Hashable:
        raise NotImplementedError

    @abstractmethod
    def barrier(self, state: Hashable, phase: int) -> Hashable:
        raise NotImplementedError

    @abstractmethod
    def observation(self, state: Hashable) -> Observation:
        raise NotImplementedError

    def edge_universe(self) -> tuple[tuple[str, str], ...]:
        return tuple(
            (sender, receiver)
            for sender in self.nodes
            for receiver in self.nodes
            if sender != receiver
        )

    def validate_messages(self, messages: Iterable[Message], phase: int) -> None:
        seen: set[str] = set()
        for message in messages:
            if message.uid in seen:
                raise ValueError(f"duplicate message uid: {message.uid}")
            seen.add(message.uid)
            if message.phase != phase:
                raise ValueError("message phase does not match emit phase")
            if message.sender not in self.nodes or message.receiver not in self.nodes:
                raise ValueError("message endpoint not in protocol node set")
            if message.kind not in self.message_types:
                raise ValueError("message kind not declared by protocol")
