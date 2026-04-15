---
last_updated: 2026-04-15T16:00:00Z
project: proyecto_marcapersonal
---

## 🎯 Objetivo actual
Publicar contenido estratégico en LinkedIn (2x/semana) y Substack (1x/2 semanas) para posicionar a Lucía como especialista en automatización de procesos AP. Post #3 sale el viernes 17 abr a las 8:30am ART vía Zernio. Próximo: grabar Loom demo P1 para Post #4 (22 abr).

## 🧠 Contexto funcional
- Lucía transiciona de AP Lead → automation/finance ops en ~3-4 meses
- Dos proyectos completados con proof of work real: P1 (AP Reconciliation App) y P2 (Vendor Statement Automation con Google Apps Script)
- Notion MCP no carga → workaround: REST API directo con token del settings.json
- Zernio MCP tiene bug en posts_create → workaround: POST /v1/posts (draft) + PUT /v1/posts/{id} con isDraft:false
- Horario óptimo de posteo: **8:30am ART** (basado en /onyx-metrics — NO 18:30, ese fue un error corregido)
- Posts en inglés, con emojis en bullets + 👉 para insight + 💭 para CTA (patrón de Post #1 publicado)
- Sistema dual de memoria: MemPalace (semántica/largo plazo) + checkpoint .md (operacional/sesión) — conviven sin conflicto (Opción B elegida)

## ✅ Decisiones tomadas
- Idioma LinkedIn: inglés siempre
- Horario: 8:30am ART (martes y jueves, o según calendario)
- Emojis: sí, siguiendo patrón Post #1
- Imagen: adjuntar cuando hay visual relevante
- Copy: nunca reescribir sin aprobación
- Sistema de memoria: Opción B — MemPalace + checkpoint .md coexisten sin pisarse
- Hook PreCompact: activo en settings.json (guarda checkpoint antes de compactar automáticamente)

## 📊 Análisis y estrategia
**Métricas Posts #1 y #2:**
- Post #1 (26 mar, 18:30 ART): 1,326 imp | 877 alc | 26 react | 7 com | 2.79% eng | 5 followers
- Post #2 (31 mar, 20:30 ART): 290 imp | 179 alc | 5 react | 0 com | 2.07% eng | 0 followers

**Insights clave:**
1. Hook personal + vulnerabilidad es el multiplicador de alcance
2. Horario óptimo: 8:30am ART — más temprano > más tarde
3. Audiencia enterprise ya apareció: EY, ExxonMobil, Genpact, NetSuite
4. Manila 7% = BPO/shared services AP global — inglés + terminología hace viajar el contenido
5. Responder comentarios en primeras 2 horas (alarma post-publicación)

## 📁 Archivos y rutas clave
- Posts: `onyx/memory/posts/post-01 a post-07.md`
- Substack: `onyx/memory/substack/substack-01 y 02.md`
- Calendario: `onyx/memory/logs/calendario-editorial.md`
- Bitácora: `onyx/memory/logs/bitacora-sesiones.md`
- Persistent vars: `onyx/memory/persistent-variables.md`
- Notion DB Posts LinkedIn: `32e6e736-4ef7-81d3-8666-c3c54b5ba19e`
- Notion DB Substack: `32e6e736-4ef7-8118-a183-cc34da56f593`
- Notion DB Tareas: `32e6e736-4ef7-8112-a599-e5094206098b`
- Notion Loom guion P1: `3436e7364ef781ba97e4d5e54a1c4490` (Para Post #4)
- Zernio LinkedIn account ID: `69d6a5e27dea335c2bc875a4`
- Zernio Post #3 ID: `69debc75e13608bd119221f2` (scheduled 2026-04-17T11:30:00Z = 8:30am ART)
- Notion token: en `~/.claude/settings.json` → mcpServers.notion.env.OPENAPI_MCP_HEADERS
- Zernio API key: en `~/.claude/settings.json` → mcpServers.zernio.env.ZERNIO_API_KEY
- Pre-compact hook: `~/.claude/hooks/pre-compact-checkpoint.sh` + configurado en settings.json

## ⚠️ Riesgos y dudas abiertas
- Post #4 (22 abr): necesita screenshot de la app P1 y el Loom grabado — Lucía tiene que proveerlos
- Substack #1 (24 abr): borrador listo, hay que publicarlo manualmente en Substack.com
- Notion token expuesto en un commit intermedio (luego reescrito) — considerar rotar en notion.so
- Zernio media temp storage: auto-delete después de 7 días → imagen de Post #3 subida el 15 abr, válida hasta ~22 abr

## ➡️ Próximos pasos exactos
1. Grabar Loom demo P1 (guion en Notion ID: 3436e7364ef781ba97e4d5e54a1c4490)
2. Verificar Post #3 publicado viernes 17 abr 8:30am ART
3. Screenshot app P1 para Post #4 (22 abr) — Lucía debe proveerla
4. Programar Post #4 en Zernio (22 abr 8:30am ART) con screenshot + Loom
5. Publicar Substack #1 el 24 abr en Substack.com
6. Empezar P3 (Slack Bot para Supply) — semanas 5-9

## 🔁 Instrucción de rehidratación
Al iniciar nueva sesión: leer este archivo primero. Estado al 2026-04-15: Post #3 programado Zernio viernes 17 abr 8:30am, hook PreCompact activo, Loom guion guardado en Notion para Post #4, sistema dual de memoria (MemPalace + checkpoint .md) confirmado como Opción B.
