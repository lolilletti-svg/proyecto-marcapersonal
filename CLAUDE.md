# Proyecto Marca Personal — Onyx v3

## COMPORTAMIENTO AUTOMÁTICO AL CIERRE DE SESIÓN

**Trigger:** Cada vez que Lucía señale que se va o termina la sesión — frases como "me voy", "hasta acá", "chau", "listo por ahora", "me estoy por ir", "cerramos", "terminamos", "nos vemos", "dejo hasta acá", "hasta luego" — ejecutar automáticamente el siguiente protocolo SIN que Lucía lo pida:

### Protocolo de cierre (en orden):

1. **Actualizar memoria del sistema** (`/Users/luciacamilletti/.claude/projects/.../memory/`)
   - Actualizar `project_marca_personal.md` con el estado actual y próximos pasos
   - Crear o actualizar cualquier memoria de proyecto relevante (ej. `project_zernio_setup.md`)
   - Actualizar `MEMORY.md` si se agregaron archivos nuevos

2. **Agregar entrada en bitácora** (`onyx/memory/logs/bitacora-sesiones.md`)
   - Fecha de la sesión
   - Qué se hizo (concreto, no genérico)
   - Estado al cerrar
   - Próximos pasos

3. **Actualizar README.md** (raíz del proyecto)
   - Si no existe, crearlo
   - Si existe, actualizarlo con cualquier cambio relevante de la sesión (integraciones nuevas, comandos nuevos, estado de proyectos, etc.)

4. **Git commit y push a GitHub**
   - `git add -A`
   - `git commit -m "Session [fecha]: [resumen breve de lo hecho]"`
   - `git push origin main`
   - Si el repo no está inicializado o no tiene remote, avisar a Lucía y dar los comandos exactos para configurarlo

### Importante:
- Ejecutar el protocolo completo sin preguntar si hacerlo — es automático
- No omitir ningún paso aunque la sesión haya sido corta
- Si no hay nada nuevo que agregar, igual registrar en bitácora que la sesión fue breve y qué se revisó

## MEMPALACE — MEMORIA SEMÁNTICA GLOBAL

MemPalace es un plugin de memoria instalado a nivel usuario. Se instala una sola vez:

```bash
claude plugin marketplace add milla-jovovich/mempalace
claude plugin install --scope user mempalace
```

Una vez instalado, inicializar en cada proyecto nuevo con:
```
/mempalace:init
```

MemPalace corre en segundo plano automáticamente — no requiere comandos manuales para guardar.

---

## ENTORNO VIRTUAL — CREACIÓN AUTOMÁTICA

En cada proyecto nuevo que se cree o trabaje en este workspace, crear automáticamente un entorno virtual de Python sin preguntar:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

- Crear el `.venv` en la raíz del proyecto
- Agregar `.venv/` al `.gitignore` si no está ya
- No preguntar si crear el entorno — siempre hacerlo directamente

Este proyecto usa Onyx, estratega personal de LinkedIn de Lucía.

## Cómo usar Onyx

Onyx está disponible como subagente en `.claude/agents/onyx.md`.

Los comandos disponibles son:
- `/onyx-post` — crea un post estratégico completo
- `/onyx-daily` — convierte trabajo del día en contenido
- `/onyx-strategy` — planificación estratégica de posicionamiento
- `/onyx-profile` — auditoría y mejora del perfil
- `/onyx-research` — benchmark y análisis de referentes
- `/onyx-calendar` — calendario editorial
- `/onyx-review` — revisión semanal/mensual

## Estructura del plugin

```
.claude/
  agents/onyx.md          ← definición del agente
  commands/               ← slash commands
onyx/
  context/user-profile.md ← perfil de Lucía
  memory/                 ← variables persistentes, proyectos, logs
  skills/linkedin-strategy/ ← 20+ skills de estrategia
```

## Skills disponibles

Las skills están en `onyx/skills/linkedin-strategy/`:

- `insight-extractor` — extrae insights de experiencias reales
- `content-angle-generator` — genera ángulos de contenido
- `narrative-builder` — construye narrativa profesional
- `positioning-auditor` — audita alineación con posicionamiento
- `authority-builder` — construye autoridad sin inflación
- `anti-cliche-filter` — elimina genéricos y corporativismo
- `hook-generator` — genera hooks para posts
- `post-rewriter` — reescribe posts débiles
- `trend-scanner` — detecta tendencias relevantes
- `competitor-analyzer` — analiza referentes del sector
- `idea-gap-finder` — encuentra huecos de contenido
- `comment-strategy` — estrategia de comentarios
- `feedback-loop` — análisis de rendimiento
- `posting-strategy-optimizer` — optimiza frecuencia y momento
- `editorial-calendar-system` — sistema de calendario editorial
- `project-story-miner` — extrae historias de proyectos reales
- `benchmark-mapper` — mapea referentes y brechas
- `profile-gap-analyzer` — analiza brechas en el perfil
- `proof-of-work-packager` — empaqueta evidencias reales
- `weekly-review-engine` — motor de revisión semanal
- `skill-orchestrator` — orquesta múltiples skills
- `memory-skill` — gestión de memoria contextual

## Contexto de Lucía

Ver `onyx/context/user-profile.md` para perfil completo, voz de marca, y non-negotiables.

## Memoria

- `onyx/memory/persistent-variables.md` — variables a rellenar y mantener actualizadas
- `onyx/memory/projects/` — historias de proyectos reales
- `onyx/memory/logs/` — log de contenido publicado
