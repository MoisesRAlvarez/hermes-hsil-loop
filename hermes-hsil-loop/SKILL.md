name: hsil

description: "Hermes Self‑Improving Loop – captura aprendizajes de sesión, los analiza por la noche, propone actualizaciones de skills y hace respaldo en Notion y Obsidian."

version: 0.2.0

author: Hermes (custom)

category: productivity

metadata:

  hermes:

    tags: [hsil, aprendizaje, auto-mejora, notion, obsidian]

---

# Hermes Self‑Improving Loop (HSIL)

## Propósito

Capturar qué funcionó y qué no en cada sesión de Hermes, ejecutar un análisis nocturno con el LLM, generar o actualizar skills automáticamente y guardar un respaldo duradero en Notion y Obsidian.

## Cómo funciona

1. **Capturar** – al final de cada sesión el script `hsil_capture` escribe una línea JSONL en `~/.hermes/hsil/log.jsonl` con:

   - `wins` – lo que salió bien

   - `losses` – lo que falló o se puede mejorar

   - `patterns` – observaciones recurrentes

   - `feature_request` – una idea concreta para una skill nueva o una automatización

   La misma línea se respalda en una base de datos de Notion (`HSIL Log`) y en una nota diaria de Obsidian (`~/obsidian/hsil/YYYY-MM-DD.md`).

2. **Analizar** – un trabajo cron (por defecto `0 22 * * *`) ejecuta `hsil_analyze`. Lee las últimas N líneas del registro, pregunta al LSM por propuestas de mejora (nueva skill, editar skill existente, ajuste de configuración) y las escribe en `~/.hermes/hsil/proposals.yaml`.

3. **Generar** – si `auto_apply_skills: true` (configurable) el script `hsil_generate` convierte cada propuesta en una skill real (usando la skill `hermes-agent-skill-authoring`) o actualiza la configuración de Hermes. Si está en `false`, revisas las propuestas primero.

4. **Recordar** – al inicio de una nueva sesión `hsil_recall` lee el registro, elige los K aprendizajes más relevantes (comparación simple por palabras clave – puede reemplazarse por embeddings) e imprime un bloque de contexto para que el modelo los tenga “en mente”.

## Instalación

La skill es puro Python; solo necesita la biblioteca estándar (opcional: `owlready2` si quieres razonamiento, no se usa aquí).

bash

No hace falta instalar paquetes extra para el núcleo.

Si quieres que el respaldo opcional a Notion/Obsidian funcione, asegura que las skills de Notion y Obsidian estén instaladas y configuradas.

## Configuración

Agrega lo siguiente a `~/.hermes/config.yaml` (ajusta valores según prefieras):

yaml

hsil:

  enabled: true

  post_run_hook: true          # ejecuta la captura al final de cada sesión Hermes

  analysis_cron: "0 22 * * *"  # análisis nocturno a las 22:00

  max_log_lines: 5000          # rota el registro después de tantas líneas (opcional)

  recall_count: 5              # cuántos aprendizajes inyectar al inicio de sesión

  auto_apply_skills: true      # false si quieres revisar propuestas primero

## Uso

- **Automático** – después de cada chat la captura se ejecuta; cada noche a las 22:00 el análisis se ejecuta y, si `auto_apply_skills` está activo, las nuevas skills o cambios de configuración aparecen automáticamente.

- **Manual** – puedes invocar cualquier script directamente:

bash

  hermes run hsil_capture          # forzar una captura ahora

  hermes run hsil_analyze          # generar propuestas ahora

  hermes run hsil_generate         # aplicar propuestas ahora

  hermes run hsil_recall           # ver qué se inyectaría como contexto

## Ejemplo de línea de registro (JSONL)

json

{

  "timestamp": "2026-05-09T23:12:04.123456",

  "wins": ["Completé 30 min de trabajo profundo", "Inbox cero logrado"],

  "losses": ["No medité", "Pasé 20 min en Instagram"],

  "patterns": ["El uso de pantalla en la noche reduce la calidad del sueño"],

  "feature_request": "Crear un recordatorio automático de 'hora de dormir' que atenúe luces y desactive notificaciones a las 21:30"

}

## Extensiones

- Reemplaza la comparación simple de palabras clave en `recall.py` por una búsqueda de similitud en vector store para contexto más rico.

- Agrega un script `hsil_notify` que envíe un resumen nocturno de las propuestas por Telegram.

- Integra con la skill `ontology` para almacenar aprendizajes como triples RDF y consultarlos semánticamente.
