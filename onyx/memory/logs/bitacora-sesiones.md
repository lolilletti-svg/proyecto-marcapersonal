# Bitácora de sesiones

---

## Sesión 2026-04-15 — Loom guion + Hook PreCompact

**Qué se hizo:**

1. **Mini guion Loom guardado en Notion:**
   - Guion de 90s para demo de AP Reconciliation App (P1)
   - Guardado en Notion DB Tareas: "Mini guion Loom — AP Reconciliation App (P1)"
   - Etiquetado como Para Post #4 (22 abr), Proyecto P1, Tipo Contenido

2. **Hook PreCompact configurado:**
   - Creado `/Users/luciacamilletti/.claude/hooks/pre-compact-checkpoint.sh`
   - Agregado `PreCompact` hook en `~/.claude/settings.json`
   - El hook guarda checkpoint completo automáticamente antes de que Claude compacte el contexto
   - Previene pérdida de contexto mid-session

3. **Sistema dual de memoria clarificado (Opción B):**
   - MemPalace = memoria semántica, largo plazo, searchable
   - checkpoint .md = contexto operacional de sesión, se lee al arrancar
   - No hay conflicto real — conviven sin pisarse

**Estado al cerrar:**
- Pre-compact hook: ✅ activo
- Loom guion: ✅ guardado en Notion (ID: 3436e7364ef781ba97e4d5e54a1c4490)
- Post #3: programado Zernio viernes 17 abr 8:30am ART

**Próximos pasos:**
1. Grabar el Loom (guion en Notion)
2. Screenshot de la app P1 para Post #4 (22 abr)
3. Verificar Post #3 publicado el viernes 17 abr
4. Publicar Artículo Substack #1 el 24 abr

---

## Sesión 2026-04-08 — Integración Zernio MCP

**Qué se hizo:**

1. **Investigación de Zernio:**
   - Zernio es una API unificada para 14+ redes sociales (LinkedIn incluido) con MCP para Claude
   - 280+ herramientas: publicar, programar, analytics, inbox, ads, webhooks
   - Free tier: 20 posts/mes, 2 perfiles — sin tarjeta de crédito
   - Analytics add-on: $10/mes (métricas profundas: impresiones, engagement, best time to post)

2. **Configuración del MCP:**
   - API key de Lucía guardada en `settings.json` global
   - Formato SSE (`url` + `headers`) agregado al bloque `mcpServers`
   - Las herramientas del MCP **no cargaron** — posiblemente el formato `url` no es compatible con Claude Code CLI
   - Próximo intento: usar `uvx` (instalación local) — requiere instalar `uv` primero

3. **Estado al cerrar:**
   - `settings.json` tiene la config de Zernio (SSE format — no funciona todavía)
   - LinkedIn conectado en el dashboard de Zernio
   - API key activa: `sk_fddbcfa9a97272c2f2061645daa998e58791abfede7344dd18a6202983468441`

**Próximos pasos:**
1. Correr `curl -LsSf https://astral.sh/uv/install.sh | sh` en terminal
2. Actualizar `settings.json` a formato `uvx` para Zernio
3. Reiniciar Claude Code y verificar que los tools de Zernio cargan
4. Tirar métricas de los 2 posts publicados en LinkedIn

---

## Sesión 2026-03-27 (continuación)

**Qué se hizo:**

1. **Fix leading zeros en matching de Bills:**
   - Problema: statement tenía `019197`, Bills tenía `19197` → marcaba NOT FOUND
   - Fix: construir `billsNorm` (lookup normalizado, strips leading zeros + lowercase) antes del loop de matching
   - Lógica: intenta exact match primero, si falla intenta normalized match
   - Archivo: `reconciliation-app.html` — función `runReconciliation()`, líneas del loop de matching

2. **Intento migración a OpenAI (revertido):**
   - Se migró a `gpt-4o-mini` + pdf.js para extracción de PDF
   - Lucía pidió revertir a Anthropic — quedó con Anthropic API (Tier 1 activo)
   - El código de OpenAI no quedó en el archivo

**Estado al cerrar sesión:**
- App P1: ✅ funciona con Anthropic Tier 1 + fix leading zeros
- Skills métricas + `/onyx-metrics`: ✅ operativos
- Bot Telegram: próxima tarea — agregar LLM para lenguaje natural + transcripción de audios

**Próximos pasos:**
- Agregar LLM al bot de Telegram (texto libre + audios en lenguaje natural)
- Publicar Post #2 (30 mar)

---

## Sesión 2026-03-27

**Qué se hizo:**

1. **Skills de métricas creadas (8 archivos nuevos):**
   - `metrics-orchestrator.md` — orquestador central con flujo, output structure, ritual semanal y criterios de decisión
   - `linkedin-metrics-reader.md` — detector de patrones (incluye modo early-stage)
   - `substack-metrics-reader.md` — estratega de newsletter (incluye modo pre-lanzamiento)
   - `reddit-signal-scanner.md` — analista de audiencia con subreddits específicos de Lucía
   - `content-strategist.md` — estratega editorial con postura obligatoria
   - `content-generator.md` — copywriter con voz y reglas de formato de Lucía
   - `experiment-designer.md` — diseñador de tests con estructura completa
   - `community-manager-advisor.md` — advisor de comunidad con estrategia de respuesta
   - `SKILL.md` actualizado con la nueva sección "Metrics & strategy skills"

2. **Slash command `/onyx-metrics` creado:**
   - Activa el flujo completo: readers → strategist → generator + experiments + community
   - Maneja early-stage automáticamente
   - Output en estructura estándar definida en metrics-orchestrator

3. **App P1 migrada de Anthropic API → OpenAI API:**
   - Modelo: `gpt-4o-mini` (reemplaza `claude-haiku-4-5-20251001`)
   - PDF: pdf.js extrae texto del PDF → se envía como texto a OpenAI (reemplaza document type de Claude)
   - Headers: `Authorization: Bearer sk-...` (reemplaza `x-api-key` + `anthropic-version`)
   - Endpoint: `https://api.openai.com/v1/chat/completions`
   - Response parsing: `data.choices[0].message.content` (reemplaza `data.content[0].text`)
   - UI: label y placeholder actualizados a OpenAI
   - API key: ahora acepta `sk-` (antes requería `sk-ant`)
   - Causa del cambio: rate limits persistentes en cuenta Anthropic — OpenAI como alternativa

4. **Diagnóstico de API usage:**
   - App hace 1 request por archivo de statement
   - Consume ~4,000–12,000 tokens por run
   - Con Tier 1 Anthropic: 50 RPM / 50K TPM — no debería volver a tener rate limits
   - Con OpenAI gpt-4o-mini: sin limitaciones prácticas para este uso

**Estado al cerrar sesión:**
- Skills de métricas: ✅ 8 skills + 1 slash command operativos
- App P1: ✅ migrada a OpenAI — pendiente probar con API key de OpenAI
- Rate limit Anthropic: resuelto (Tier 1 activo + migración a OpenAI)

**Próximos pasos:**
- Probar la app con API key de OpenAI (platform.openai.com/api-keys)
- Publicar Post #2 en LinkedIn (30 mar)
- Deploy bot Telegram (Railway desde terminal de Lucía)

---

## Sesión 2026-03-26 (continuación — tarde)

**Qué se hizo:**

1. **App P1 iterada y mejorada:**
   - Bug fix: credits se limpiaban antes de usarse → nunca matcheaban. Fix: remover `creditsData = []; creditsLookup = {};` de `runReconciliation()`
   - Bug fix: errores en `readBills` eran silenciosos → wrapped en try/catch
   - Bug fix: model ID incorrecto → corregido a `claude-haiku-4-5-20251001`
   - Feature: selector de vendor para credits (igual al de NS Open Items, tema amber)
   - Feature: demo mode con datos hardcodeados de Worldwide Produce (para screenshots sin API)
   - Launcher `.command` creado: doble clic → levanta servidor en background sin dejar Terminal abierta

2. **GitHub:**
   - Repo creado: `github.com/lolilletti-svg/ap-reconciliation-app`
   - README escrito y pusheado
   - Archivo: `p1-reconciliation-app/README.md`

3. **Post #1 publicado en LinkedIn** ✅
   - Cierre actualizado en Notion: "Hay más por venir — y estoy contenta de compartirlo."
   - Decisión tomada: todos los posts de LinkedIn van en inglés (versión larga)
   - Versión corta en español también finalizada para Post #1

4. **Formato LinkedIn definido para todos los posts:**
   - Hook directo que frena el scroll (nombra el proceso específico, nunca "this process")
   - Líneas cortas para móvil
   - Ritmo: tensión → resolución
   - Cierre abierto sin anunciar nada
   - Copy original preservado — solo se aplica formato, no se reescribe

5. **Versiones en inglés agregadas a los 4 posts en Notion:**
   - Cada post tiene sección "Versión — English" al final
   - Hashtags definidos (6-8 por post, centrados en AP niche + herramientas)

6. **Hashtags por post:**
   - #1/#2: `#AccountsPayable #ProcessAutomation #FinanceOps #NoCode #Automation #Documentation #VendorManagement #ClaudeAI`
   - #3: `#AccountsPayable #ProcessAutomation #FinanceOps #Operations #Automation #WorkflowAutomation #NoCode #ClaudeAI`
   - #4: `#AccountsPayable #ProcessAutomation #FinanceOps #NoCode #Automation #ClaudeAI #VendorManagement #OpenSource`

**Estado al cerrar sesión:**
- Post #1: ✅ PUBLICADO EN LINKEDIN
- Posts #2, #3, #4: listos en Notion con versión en inglés + hashtags
- App P1: ✅ funciona, repo en GitHub con README
- Rate limit API: necesita comprar $5 en console.anthropic.com para desbloquear Tier 1
- Bot Telegram: pendiente deploy desde terminal de Lucía (ver sesión anterior)

**Próximos pasos (próxima sesión):**
- Agregar skills de métricas de LinkedIn a Onyx (Lucía lo confirmó)
- Publicar Post #2 (30 mar)
- Comprar créditos en console.anthropic.com para desbloquear la app
- Deploy bot Telegram (Railway desde terminal de Lucía)

---

## Sesión 2026-03-26

**Qué se hizo:**

1. **Notion poblado completo (3 bases de datos):**
   - 📋 Tareas & Roadmap: 37 tareas distribuidas en 4 fases (semanas 1–16) con fecha, tipo, proyecto y estado
   - ✍️ Posts LinkedIn: 4 posts de P1 con copy completo, versión corta, y respuestas a comentarios esperados (generados con /onyx-post)
   - 📰 Artículos Substack: 3 artículos Fase 1–2 con estructura completa y companion posts LinkedIn (generados con /onyx-substack)

2. **Posts LinkedIn generados con /onyx-post (skill correcto):**
   - Post #1: "Nadie me pidió que mejorara este proceso" → LISTO (26 mar)
   - Post #2: "Lo que encontré cuando documenté mi proceso" → LISTO (30 mar)
   - Post #3: "Por qué saber procesos vale más que saber código" → LISTO (2 abr)
   - Post #4: Demo visual app → BORRADOR (6 abr, falta screenshot + GitHub)

3. **Artículos Substack generados con /onyx-substack (skill correcto):**
   - #1: "Cómo construí una app de reconciliación sin saber programar" → borrador listo para pulir (8 abr)
   - #2: "El stack mínimo viable para automatizar AP en 2026" → borrador con [COMPLETAR tras P2] (29 abr)
   - #3: "Documentar antes de automatizar: el paso que todos saltan" → borrador con [COMPLETAR tras P3] (13 may)

4. **Onyx Telegram Bot — diseñado y código completo:**
   - Decisión: Python + Railway (hosting gratuito) + python-telegram-bot + Anthropic SDK
   - Funciones: /post, /substack, /roadmap, /save + modo conversacional con historial por sesión
   - Guardado automático en Google Drive (/Onyx/LinkedIn/ y /Onyx/Substack/) + sync Notion
   - Código en: `onyx-bot/` (bot.py, system_prompt.py, notion_client.py, drive_client.py)
   - Tests OK: Claude API responde, Telegram bot creado (@onyx_lucia_bot)
   - Bloqueado en deploy: Railway guarda credenciales en Keychain de Mac — los comandos desde Claude Code no tienen acceso al Keychain

5. **Feedback guardado en memoria:**
   - Siempre usar /onyx-post para posts LinkedIn y /onyx-substack para artículos Substack sin que Lucía lo pida

**Estado al cerrar sesión:**
- Notion: ✅ roadmap completo + 4 posts + 3 artículos
- Bot código: ✅ completo en `onyx-bot/`
- Bot deploy: ⏳ BLOQUEADO — falta correr desde terminal de Lucía
- Post #1: listo para publicar desde hace 2 días

**Próximos pasos al retomar — EXACTO PUNTO DE CORTE:**

### Deploy del bot (hacer primero — 10 minutos):
Los comandos deben correrse desde la **terminal de Lucía** (no desde Claude Code — Railway usa el Keychain de Mac):

```bash
# 1. Ir a la carpeta
cd /Users/luciacamilletti/Documents/claude_code/proyecto_marcapersonal/onyx-bot

# 2. Login Railway (si no persiste de la sesión anterior)
/opt/homebrew/bin/railway login --browserless
# → abrí railway.com/activate → ingresá el código → autorizá

# 3. Crear proyecto en Railway
/opt/homebrew/bin/railway init
# → nombre: onyx-bot

# 4. Configurar variables de entorno
/opt/homebrew/bin/railway variables set TELEGRAM_TOKEN=$TELEGRAM_TOKEN
/opt/homebrew/bin/railway variables set ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
/opt/homebrew/bin/railway variables set NOTION_TOKEN=$NOTION_TOKEN

# 5. Deploy
/opt/homebrew/bin/railway up --detach

# 6. Verificar logs
/opt/homebrew/bin/railway logs
```

### Después del deploy:
- Abrir Telegram → @onyx_lucia_bot → /start → verificar que responde
- Publicar Post #1 en LinkedIn
- Configurar Google Drive (service account) → habilita guardado en Drive desde el bot

---

## Sesión 2026-03-25

**Qué se hizo:**

1. **3 skills nuevas creadas:**
   - `reddit-audience-researcher.md` — investigación de audiencia en Reddit (r/Accounting, r/excel, r/nocode, r/automation, r/sysadmin, r/smallbusiness, r/FinancialCareers), mapeo a oportunidades de contenido
   - `substack-writer.md` — producción de artículos de Substack con formato editorial propio, distinto al LinkedIn
   - `platform-content-adapter.md` — toma un insight y genera las dos versiones (LinkedIn discovery + Substack authority)

2. **2 comandos nuevos creados:**
   - `/onyx-substack` — genera artículo completo de Substack con companion LinkedIn post
   - `/onyx-reddit-research` — corre investigación de audiencia en subreddits clave, output: 5 ideas LinkedIn + 2 ideas Substack

3. **Sistema expandido a dos canales:**
   - LinkedIn: 2x/semana (descubrimiento y visibilidad)
   - Substack: 1x/2 semanas Fase 1–2, 1x/semana Fase 3+
   - Reddit research: cada 2 semanas como actividad recurrente

4. **Roadmap v2 documentado** en `user-profile.md` — 4 fases con LinkedIn + Substack + Reddit research integrados

5. **Ideas de contenido documentadas** — 8 posts LinkedIn + 3 artículos Substack para Fase 1–2

6. **`persistent-variables.md` actualizado** — canales, cadencias, relación entre ellos

7. **`onyx.md` y `SKILL.md` actualizados** — las 3 skills nuevas registradas

**Estado al cerrar sesión:**
- Post #1: listo, no publicado
- 3 skills nuevas: operativas
- 2 comandos nuevos: operativos
- Roadmap v2: documentado en user-profile y persistent-variables
- P1–P5: sin cambios

**Próximos pasos al retomar:**
1. Publicar post #1 en LinkedIn
2. Correr `/onyx-reddit-research` para baseline de audiencia (Fase 1)
3. Documentar P1 + subir a GitHub
4. Arrancar primer artículo Substack sobre P1 con `/onyx-substack`

---

## Sesión 2026-03-23

**Qué se hizo:**

1. **Roadmap 16 semanas definido y documentado** — 4 fases, 5 proyectos, frecuencia de posting, timeline de job search (arranca semana 9).

2. **Post #1 mejorado y guardado** — "Nadie me pidió que mejorara este proceso. Lo hice igual." Hook mejorado respecto a versión anterior. Listo para publicar. Archivo: `onyx/memory/posts/post-01-nadie-me-pidio.md`

3. **5 archivos de proyecto creados** (uno por proyecto):
   - `p1-ap-reconciliation-app.md` — COMPLETADO, pendiente docs/demo/GitHub
   - `p2-vendor-email-automation.md`
   - `p3-slack-bot-supply.md`
   - `p4-invoice-ingestion.md`
   - `p5-postclose-reporting.md`

4. **`persistent-variables.md` actualizado** — herramientas reales, objetivo 3–4 meses, posicionamiento final, 5 proyectos.

5. **`user-profile.md` actualizado** — narrativa completa, proyectos, roadmap de 16 semanas, posicionamiento final.

6. **Memoria del sistema actualizada** — `project_marca_personal.md` reescrito con estado actual del proyecto.

**Estado al cerrar sesión:**
- Post #1: listo, no publicado
- P1: app construida, falta documentar + demo + GitHub
- P2–P5: definidos, sin empezar

**Próximos pasos al retomar:**
1. Publicar post #1 en LinkedIn
2. Documentar P1: README, comentarios en el código, grabar demo corto
3. Subir P1 a GitHub
4. Arrancar P2 (email automation con Make)

---

## Sesión 2026-04-14

**Qué se hizo:**

1. **Notion sincronizado via REST API** (Notion MCP no carga — workaround directo):
   - Posts LinkedIn (#5, #6, #7) creados en Notion DB con copy completo, hook, CTA, fecha
   - Cleanup DB: 4 posts duplicados/obsoletos archivados, fechas P1 actualizadas (Post #3 → 17 abr, Post #4 → 22 abr)
   - Substack: 1 artículo archivado, 2 actualizados con título EN y fechas correctas (24 abr, 8 may)

2. **Post #3 programado en Zernio** (MCP bug workaround — usar REST API directamente):
   - Bug: `posts_create` MCP falla con `'Platform5' object has no attribute 'lower'` para LinkedIn
   - Workaround: POST /v1/posts (crea draft) → PUT /v1/posts/{id} con isDraft:false + scheduledFor
   - Resultado: Post #3 scheduled para 17/04/2026 12:00 UTC (= 9am ART)
   - Zernio post ID: `69debc75e13608bd119221f2`

3. **Análisis de métricas — Posts #1 y #2 LinkedIn:**

   **Post #1 — "Nadie me pidió que mejorara este proceso"**
   - Publicado: 26/03/2026 18:30 ART
   - Impresiones: 1,326 | Alcanzados: 877 | Reacciones: 26 | Comentarios: 7 | Guardado: 2 | Compartido: 2
   - Nuevos seguidores: 5 | Engagement rate: 2.79%
   - Audiencia: Internacional (Buenos Aires 19%, Manila 7%, CDMX 3%, Barcelona 3%, NY 2%)
   - Sectores top: Contabilidad 22%, Servicios financieros 13%, TI/consultoría 8%
   - Empresas viendo: EY, ExxonMobil, Air Liquide, Genpact, NetSuite

   **Post #2 — "Lo que encontré cuando documenté mi proceso"**
   - Publicado: 31/03/2026 20:30 ART
   - Impresiones: 290 | Alcanzados: 179 | Reacciones: 5 | Comentarios: 0 | Guardado: 0 | Compartido: 1
   - Nuevos seguidores: 0 | Engagement rate: 2.07%
   - Audiencia: Local (Buenos Aires 32%)
   - Sectores top: Contabilidad 16%, Servicios financieros 12%, Software 8%

   **Conclusiones estratégicas:**
   - **Horario**: 18:30 ART >> 20:30 ART. Evitar postear después de las 19:00.
   - **Tema**: Narrativa personal/provocadora (Post #1) supera a la documental (Post #2) en 4.6x impresiones
   - **Alcance internacional**: Post #1 llegó a audiencia AP global (BPO Asia, Latam, Europa)
   - **Audiencia ideal**: AP specialists + finance ops (con experiencia 40-43%), enterprise (10k+ empleados)
   - **Acción inmediata**: Reprogramar Post #3 de 9am → 18:30 ART (21:30 UTC)

**Estado al cerrar sesión:**
- Notion: ✅ 7 LinkedIn posts + 2 Substack limpios y con fechas correctas
- Zernio Post #3: ✅ scheduled 17 abr 12:00 UTC (pendiente evaluar cambio a 18:30 ART)
- Métricas Posts 1+2: ✅ analizadas y guardadas
- Pendiente: análisis no estaba siendo guardado automáticamente → protocolo identificado para corrección

**Próximos pasos:**
- Decidir si reprogramar Post #3 a 18:30 ART
- Activar protocolo de guardado automático post-/onyx-metrics
- Publicar Post #3 jueves 17 abr
