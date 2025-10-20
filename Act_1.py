#!/usr/bin/env python3
"""
Simplified Agent Dialogue: KQML-style messages with KIF-like tuples

Goal:
- Alice (procurement) asks Bob (warehouse) about:
  1) available stock of 50-inch TVs
  2) number of HDMI slots

Design choices (for clarity):
- KQML message is a small dataclass.
- KIF "content" is represented as a Python tuple (predicate, subject, variable).
- No complex parsing. Very explicit, readable methods.
- Transcript prints a KQML-looking block for your e-portfolio evidence.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, Union, List
import json
from pathlib import Path

KIF = Tuple[str, str, str]  # (predicate, subject, variable), e.g. ("available-stock", "tv-50-inch", "?qty")

@dataclass
class KQMLMessage:
    performative: str                   # "ask-one" | "tell"
    sender: str
    receiver: str
    language: str = "KIF"
    ontology: str = "warehouse-onto"
    content: Union[KIF, Tuple[str, str, Union[int, str]]] = None  # For tell, we use form: ("=", "?var", value)
    reply_with: Optional[str] = None
    in_reply_to: Optional[str] = None

    def pretty(self) -> str:
        """Human-friendly KQML-like block (for transcripts)."""
        def content_str(c):
            if isinstance(c, tuple):
                if c and c[0] == "=":
                    # ("=", "?qty", 42) --> (= ?qty 42)
                    return f"(= {c[1]} {c[2]})"
                # ("available-stock","tv-50-inch","?qty") --> (available-stock (tv-50-inch) ?qty)
                pred, subj, var = c
                return f"({pred} ({subj}) {var})"
            return str(c)

        lines = [
            "(kqmlmsg",
            f"  :performative {self.performative}",
            f"  :sender {self.sender}",
            f"  :receiver {self.receiver}",
            f"  :language {self.language}",
            f"  :ontology {self.ontology}",
            f"  :content {content_str(self.content)}",
        ]
        if self.reply_with:
            lines.append(f"  :reply-with {self.reply_with}")
        if self.in_reply_to:
            lines.append(f"  :in-reply-to {self.in_reply_to}")
        lines.append(")")
        return "\n".join(lines)

# --- Simple Warehouse "KB" for Bob ---
class WarehouseKB:
    def __init__(self) -> None:
        # Facts keyed by (predicate, subject) --> value
        self.facts: Dict[Tuple[str, str], int] = {
            ("available-stock", "tv-50-inch"): 42,
            ("hdmi-slots", "tv-50-inch"): 3,
        }

    def lookup(self, predicate: str, subject: str) -> Optional[int]:
        return self.facts.get((predicate, subject))

# --- Bob (answers ask-one with tell) ---
class Bob:
    def __init__(self, kb: WarehouseKB) -> None:
        self.name = "Bob"
        self.kb = kb

    def handle(self, msg: KQMLMessage) -> KQMLMessage:
        assert msg.performative == "ask-one", "Bob only supports ask-one in this demo"
        pred, subj, var = msg.content  # type: ignore

        value = self.kb.lookup(pred, subj)
        if value is None:
            # Could also return an error performative in richer systems
            content = ("=", var, "unknown")
        else:
            content = ("=", var, value)

        return KQMLMessage(
            performative="tell",
            sender=self.name,
            receiver=msg.sender,
            content=content,
            ontology=msg.ontology,
            language=msg.language,
            in_reply_to=msg.reply_with,
        )

# --- Alice (asks and records replies) ---
class Alice:
    def __init__(self) -> None:
        self.name = "Alice"
        self.bindings: Dict[str, Union[int, str]] = {}

    def ask(self, receiver: str, ontology: str, content: KIF, tag: str) -> KQMLMessage:
        return KQMLMessage(
            performative="ask-one",
            sender=self.name,
            receiver=receiver,
            content=content,
            ontology=ontology,
            reply_with=tag,
        )

    def handle_reply(self, msg: KQMLMessage) -> None:
        # Expect content like ("=", "?qty", 42)
        op, var, value = msg.content  # type: ignore
        assert op == "=", "Unexpected reply form"
        self.bindings[var] = value

# --- Demo runner ---
def run_demo() -> Dict[str, any]:
    kb = WarehouseKB()
    bob = Bob(kb)
    alice = Alice()
    ontology = "warehouse-onto"

    # 1) Ask stock for 50-inch TVs
    q1 = alice.ask("Bob", ontology, ("available-stock", "tv-50-inch", "?qty"), tag="q1")
    r1 = bob.handle(q1)
    alice.handle_reply(r1)

    # 2) Ask number of HDMI slots
    q2 = alice.ask("Bob", ontology, ("hdmi-slots", "tv-50-inch", "?n"), tag="q2")
    r2 = bob.handle(q2)
    alice.handle_reply(r2)

    transcript = [q1.pretty(), r1.pretty(), q2.pretty(), r2.pretty()]
    return {"bindings": alice.bindings, "transcript": transcript}

def main() -> None:
    result = run_demo()

    # Save artefacts for your e-portfolio evidence
    out = Path("artefacts_simple")
    out.mkdir(exist_ok=True)
    (out / "transcript.txt").write_text("\n\n".join(result["transcript"]), encoding="utf-8")
    (out / "bindings.json").write_text(json.dumps(result["bindings"], indent=2), encoding="utf-8")

    print("=== Dialogue Transcript ===")
    print("\n\n".join(result["transcript"]))
    print("\n=== Extracted Bindings ===")
    for var, val in result["bindings"].items():
        print(f"{var} = {val}")
    print(f"\nSaved artefacts to: {out.resolve()}")

if __name__ == "__main__":
    main()
