# hermes-hsil-loop 🚀

> **Self-Improving Loop: no es solo ejecutar, es aprender de cada interacción.**

Este proyecto nace de mi necesidad como estudiante de IA en ITLA para crear sistemas que no sean estáticos. `hermes-hsil-loop` es el motor que permite a mi ecosistema personal aprender de sus propios aciertos y errores tras cada sesión.

Repositorio: https://github.com/MoisesRAlvarez/hermes-hsil-loop

## 🧠 El concepto

HSIL (Hermes Self-Improving Loop) implementa un ciclo cerrado de retroalimentación:

1. **Capture:** registra victorias, fallos y patrones de comportamiento.
2. **Analyze:** procesa los logs mediante LLMs para detectar áreas de mejora.
3. **Generate:** crea o ajusta nuevas habilidades (skills) de forma autónoma.

## 🛠️ Tecnologías

- **Python 3.11+**
- **JSONL** para logging eficiente
- **Integración opcional con Notion y Obsidian** para persistencia de conocimiento

## 📁 Estructura del repositorio

- `SKILL.md` – definición de la skill.
- `scripts/` – scripts de captura (`capture.py`), análisis (`analyze.py`), generación (`generate.py`) y recuerdo (`recall.py`).
- `tests/` – carpeta opcional para pruebas futuras.
- `CHANGELOG.md` – historial de cambios.
- `LICENSE` – licencia MIT.
- `.gitignore` – archivos y patrones a ignorar.

## 🚀 Instalación

```bash
git clone https://github.com/MoisesRAlvarez/hermes-hsil-loop.git
cd hermes-hsil-loop
```

### Dependencias

El núcleo de HSIL usa la biblioteca estándar de Python, por lo que no es necesario un `requirements.txt` para la funcionalidad básica.

Si llegas a usar integraciones adicionales con Notion u Obsidian, instala los paquetes requeridos según tu configuración.

## 🔧 Uso básico

1. Instala la skill en tu entorno Hermes.
2. Configura `~/.hermes/config.yaml` con la sección `hsil`.
3. Ejecuta manualmente o deja que las tareas automáticas hagan su trabajo:

```bash
hermes run hsil_capture
hermes run hsil_analyze
hermes run hsil_generate
hermes run hsil_recall
```

## ⚙️ Configuración sugerida

```yaml
hsil:
  enabled: true
  post_run_hook: true
  analysis_cron: "0 22 * * *"
  max_log_lines: 5000
  recall_count: 5
  auto_apply_skills: true
```

## 📝 Notas

- `capture.py` respalda los datos en `~/.hermes/hsil/log.jsonl` y en una nota diaria de Obsidian.
- `analyze.py` prepara propuestas en `~/.hermes/hsil/proposals.yaml`.
- `generate.py` puede crear skills nuevas y aplicar cambios de configuración.
- `recall.py` imprime los aprendizajes más relevantes para que el agente los use como contexto.
