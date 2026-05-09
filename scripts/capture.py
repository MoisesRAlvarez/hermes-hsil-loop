#!/usr/bin/env python3
"""
Script de captura HSIL.
Se ejecuta al final de una sesión de Hermes para registrar wins, losses, patterns
y una feature_request como una entrada JSONL, y hacer respaldo en Notion y Obsidian.
"""

import os
import sys
import json
import datetime
from pathlib import Path

# ----------------------------------------------------------------------
# Rutas (ajusta si cambias la ubicación en la configuración)
HSIL_DIR = Path.home() / ".hermes" / "hsil"
LOG_FILE = HSIL_DIR / "log.jsonl"
# ----------------------------------------------------------------------


def _backup_to_notion(entry: dict):
    """Intentar respaldar la entrada en una base de datos de Notion."""
    try:
        from hermes_tools import notion  # noqa: F401
        # En una implementación completa harías:
        #   db_id = notion.get_database_id("HSIL Log")
        #   notion.create_page(db_id, properties={...})
        # Por ahora solo dejamos el gancho.
        pass
    except Exception:
        # Ignorar silenciosamente si la skill de Notion no está disponible o no está configurada
        pass


def _backup_to_obsidian(entry: dict):
    """Escribir un archivo markdown diario en la bóveda de Obsidian."""
    obsidian_dir = Path.home() / "obsidian" / "hsil"
    obsidian_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    md_file = obsidian_dir / f"{today}.md"

    with md_file.open("a", encoding="utf-8") as f:
        f.write(f"## Captura HSIL – {datetime.datetime.now().isoformat()}\n\n")
        f.write("*Entrada:*\n```json\n")
        f.write(json.dumps(entry, indent=2, ensure_ascii=False))
        f.write("\n```\n\n")
        f.write("---\n\n")


def main():
    # En un despliegue real Hermes pasaría los datos de sesión por stdin o
    # variables de entorno. Para simplicidad leemos de un archivo JSON que
    # el usuario puede crear manualmente, o usamos una plantilla vacía.
    #
    # Ejemplo de uso:
    #   hermes run hsil_capture --input /tmp/session.json
    #
    import argparse

    parser = argparse.ArgumentParser(description="Capturar aprendizaje HSIL para una sesión.")
    parser.add_argument(
        "--input",
        type=str,
        help="Ruta a un archivo JSON con los datos de la sesión (wins, losses, patterns, feature_request). Si se omite, se usa una plantilla vacía.",
    )
    args = parser.parse_args()

    if args.input:
        try:
            data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Error leyendo el archivo de entrada: {e}")
            sys.exit(1)
    else:
        data = {
            "wins": [],
            "losses": [],
            "patterns": [],
            "feature_request": "",
            "timestamp": datetime.datetime.now().isoformat(),
        }

    for key in ("wins", "losses", "patterns", "feature_request", "timestamp"):
        if key not in data:
            data[key] = [] if key not in ("feature_request", "timestamp") else ""

    HSIL_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

    _backup_to_notion(data)
    _backup_to_obsidian(data)

    print(f"Captura HSIL completada: {LOG_FILE}")


if __name__ == "__main__":
    main()
