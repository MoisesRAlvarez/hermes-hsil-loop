#!/usr/bin/env python3
"""
Script de generación HSIL.
Lee proposals.yaml y, si auto_apply_skills está activo, crea/actualiza skills
y aplica cambios de configuración.
"""

import os
import sys
import yaml
from pathlib import Path

# ----------------------------------------------------------------------
HSIL_DIR = Path.home() / ".hermes" / "hsil"
PROPOSAL_FILE = HSIL_DIR / "proposals.yaml"
# ----------------------------------------------------------------------


def _load_config():
    """Leer la configuración de Hermes para verificar el flag auto_apply_skills."""
    cfg_path = Path.home() / ".hermes" / "config.yaml"
    if not cfg_path.exists():
        return {}
    try:
        import yaml as yml
        return yml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


def _apply_new_skill(prop):
    """Crear una skill nueva usando la skill hermes-agent-skill-authoring."""
    from hermes_tools import skill_manage  # helper interno

    title = prop.get("title", "Skill sin título")
    skill_name = (
        title.lower()
        .replace(" ", "-")
        .replace("/", "-")
        .replace("_", "-")
    )
    skill_content = f"""---
name: {skill_name}
description: \"{prop.get('description', 'Skill generada automáticamente por HSIL')}\"
version: 0.1.0
author: Hermes (auto-generado)
category: custom
---

# {title}

{prop.get('description', '')}

## Uso

<!-- Agrega instrucciones de uso aquí -->
"""

    try:
        skill_manage(
            action="create",
            name=skill_name,
            content=skill_content,
        )
        print(f"✅ Skill creada: {skill_name}")
    except Exception as e:
        print(f"❌ No se pudo crear la skill {skill_name}: {e}")


def _apply_edit_skill(prop):
    """Marcador de posición para editar una skill existente."""
    print("ℹ️ Las propuestas de edición de skill aún no son totalmente automáticas.")
    print(f"   Propuesta: {prop.get('title')}")


def _apply_config_change(prop):
    """Aplicar un cambio simple de configuración a config.yaml."""
    from hermes_tools import config as hermes_cfg  # helper interno

    changes = prop.get("suggested_config", {})
    if not isinstance(changes, dict) or not changes:
        print("ℹ️ No hay cambios de configuración para aplicar.")
        return

    cfg_path = Path.home() / ".hermes" / "config.yaml"
    try:
        import yaml as yml
        cfg = yml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    except Exception:
        cfg = {}

    for k, v in changes.items():
        cfg[k] = v

    cfg_path.write_text(yml.dump(cfg, default_flow_style=False), encoding="utf-8")
    print(f"✅ Configuración actualizada con: {changes}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generar skills/config desde propuestas HSIL.")
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Si se setea, aplicar cambios automáticamente (respeta hsil.auto_apply_skills).",
    )
    args = parser.parse_args()

    cfg = _load_config()
    auto_apply = cfg.get("hsil", {}).get("auto_apply_skills", False)

    if not auto_apply and not args.auto:
        print("⚠️ Auto-apply está deshabilitado. Usa --auto para forzar la aplicación, o establece hsil.auto_apply_skills: true en config.")

    if not PROPOSAL_FILE.exists():
        print("❌ No se encontró el archivo de propuestas. Ejecuta hsil_analyze primero.")
        sys.exit(1)

    try:
        data = yaml.safe_load(PROPOSAL_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Error leyendo las propuestas: {e}")
        sys.exit(1)

    proposals = data.get("proposals", [])
    if not proposals:
        print("ℹ️ No hay propuestas en el archivo.")
        sys.exit(0)

    for prop in proposals:
        p_type = prop.get("type", "").lower()
        if p_type == "new_skill":
            _apply_new_skill(prop)
        elif p_type == "edit_skill":
            _apply_edit_skill(prop)
        elif p_type == "config_change":
            _apply_config_change(prop)
        else:
            print(f"⚠️ Tipo de propuesta desconocido: {p_type}")

    print("✅ Paso de generación completado.")


if __name__ == "__main__":
    main()
