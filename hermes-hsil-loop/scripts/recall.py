#!/usr/bin/env python3
"""
Script de recuerdo HSIL.
Carga aprendizajes recientes de log.jsonl, elige los K más relevantes
(usando una coincidencia simple por palabras clave – puede cambiarse por embeddings),
y los imprime como bloque de contexto para el prompt del agente.
"""

import os
import sys
import json
from pathlib import Path

# ----------------------------------------------------------------------
HSIL_DIR = Path.home() / ".hermes" / "hsil"
LOG_FILE = HSIL_DIR / "log.jsonl"
# ----------------------------------------------------------------------


def _load_entries(limit: int = 50):
    """Devuelve las entradas más recientes `limit` del JSONL."""
    if not LOG_FILE.exists():
        return []
    entries = []
    with LOG_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    entries.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return entries[:limit]


def _score_entry(entry, query_terms):
    """
    Puntuación muy básica de relevancia: cuenta cuántos términos de consulta aparecen
    en los campos de texto de la entrada.
    """
    text = " ".join(
        [
            " ".join(entry.get("wins", [])),
            " ".join(entry.get("losses", [])),
            " ".join(entry.get("patterns", [])),
            entry.get("feature_request", ""),
        ]
    ).lower()
    score = sum(1 for term in query_terms if term in text)
    return score


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Recordar aprendizajes HSIL relevantes.")
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Cuántas entradas recientes considerar para el puntaje.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Cuántas entradas principales mostrar como contexto.",
    )
    parser.add_argument(
        "--query",
        type=str,
        default="",
        help="Consulta opcional para sesgar el recuerdo (ej. 'hábito meditación').",
    )
    args = parser.parse_args()

    entries = _load_entries(limit=args.limit)
    if not entries:
        print("# No hay aprendizajes HSIL disponibles todavía.")
        return

    if args.query.strip():
        terms = [t.lower() for t in args.query.split()]
        scored = [(_score_entry(e, terms), e) for e in entries]
        scored.sort(key=lambda x: x[0], reverse=True)
        top_entries = [e for _, e in scored[: args.top]]
    else:
        top_entries = entries[: args.top]

    print("# === Contexto HSIL (aprendizajes más relevantes) ===")
    for i, entry in enumerate(top_entries, start=1):
        print(f"\n## Aprendizaje {i} (timestamp: {entry.get('timestamp')})")
        if entry.get("wins"):
            print("**Wins:**")
            for w in entry["wins"]:
                print(f"- {w}")
        if entry.get("losses"):
            print("**Losses:**")
            for l in entry["losses"]:
                print(f"- {l}")
        if entry.get("patterns"):
            print("**Patterns:**")
            for p in entry["patterns"]:
                print(f"- {p}")
        if entry.get("feature_request"):
            print(f"**Feature Request:** {entry['feature_request']}")
    print("\n# === Fin del contexto HSIL ===")


if __name__ == "__main__":
    main()
