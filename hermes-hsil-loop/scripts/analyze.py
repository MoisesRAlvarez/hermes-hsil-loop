#!/usr/bin/env python3
"""
Script de análisis HSIL.
Lee las últimas N líneas de log.jsonl, pide al LLM propuestas de mejora,
y las escribe en proposals.yaml.
"""

import os
import sys
import json
import datetime
from pathlib import Path

# ----------------------------------------------------------------------
HSIL_DIR = Path.home() / ".hermes" / "hsil"
LOG_FILE = HSIL_DIR / "log.jsonl"
PROPOSAL_FILE = HSIL_DIR / "proposals.yaml"
# ----------------------------------------------------------------------


def _load_recent_entries(limit: int = 20):
    """Devuelve las últimas `limit` entradas JSONL como lista de diccionarios."""
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


def _call_llm_for_proposals(entries):
    """
    Construye un prompt para el LLM y le pide que proponga mejoras.
    En un entorno Hermes real usaríamos el LLM interno del agente.
    Aquí simulamos la estructura que luego consumirá generate.py.
    """
    return {
        "generated_at": datetime.datetime.now().isoformat(),
        "source_entries": entries,
        "proposals": [
            {
                "type": "new_skill",
                "title": "<Título de la skill propuesta>",
                "description": "<Qué hace la skill>",
                "suggested_config": {},
                "reason": "<Por qué esta propuesta ayuda basándose en las entradas>",
            }
        ],
    }


def main():
    import argparse
    import yaml

    parser = argparse.ArgumentParser(description="Ejecutar el análisis nocturno HSIL.")
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Número de entradas recientes del registro a considerar.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(PROPOSAL_FILE),
        help="Archivo donde escribir las propuestas (YAML).",
    )
    args = parser.parse_args()

    entries = _load_recent_entries(limit=args.limit)
    if not entries:
        print("No se encontraron entradas de registro HSIL: nada que analizar.")
        sys.exit(0)

    data = _call_llm_for_proposals(entries)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with Path(args.output).open("w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow=False, sort_keys=False, allow_unicode=True)

    print(f"Análisis completo – propuestas escritas en {Path(args.output).resolve()}")


if __name__ == "__main__":
    main()
