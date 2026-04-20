"""Deterministic runner for echo-agent. Pure function, no side effects."""

from __future__ import annotations


class EchoRunner:
    def run(self, input_text: str) -> str:
        return input_text[::-1]
