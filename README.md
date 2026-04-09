# Proyecto Marca Personal — Onyx

Sistema de estrategia de contenido y marca personal construido sobre Claude Code. Diseñado para acompañar la transición profesional de Lucía Camilletti de AP Lead hacia un rol de automatización de procesos / finance ops.

---

## Qué es esto

Un agente de LinkedIn estratégico llamado **Onyx** que vive dentro de Claude Code. Onyx no genera contenido genérico — trabaja con proof of work real, voz de marca definida y un posicionamiento concreto. Todo lo que produce está anclado en proyectos reales y experiencia genuina.

**Posicionamiento:**
> "Automatizo procesos financieros en AP — reconciliación, comunicación con vendors, intake de datos y reporting — reduciendo tiempo manual y errores operativos."

---

## Estructura del proyecto

```
proyecto_marcapersonal/
├── CLAUDE.md                          # Instrucciones del proyecto para Claude
├── README.md                          # Este archivo
│
├── .claude/
│   ├── agents/onyx.md                 # Definición del agente Onyx
│   └── commands/                      # Slash commands (10 comandos)
│       ├── onyx-post.md
│       ├── onyx-daily.md
│       ├── onyx-strategy.md
│       ├── onyx-profile.md
│       ├── onyx-research.md
│       ├── onyx-calendar.md
│       ├── onyx-review.md
│       ├── onyx-substack.md
│       ├── onyx-reddit-research.md
│       └── onyx-metrics.md
│
├── onyx/
│   ├── context/
│   │   └── user-profile.md            # Perfil completo, roadmap, voz de marca
│   ├── memory/
│   │   ├── persistent-variables.md    # Variables clave siempre activas
│   │   ├── projects/                  # Historias de los 5 proyectos reales
│   │   │   ├── p1-ap-reconciliation-app.md
│   │   │   ├── p2-vendor-email-automation.md
│   │   │   ├── p3-slack-bot-supply.md
│   │   │   ├── p4-invoice-ingestion.md
│   │   │   └── p5-postclose-reporting.md
│   │   ├── posts/                     # Posts publicados
│   │   │   └── post-01-nadie-me-pidio.md
│   │   └── logs/
│   │       └── bitacora-sesiones.md   # Log completo de cada sesión
│   ├── skills/linkedin-strategy/      # 25+ skills modulares
│   └── sync/
│       └── build-notion-workspace.py  # Script sync con Notion
│
├── onyx-bot/                          # Telegram Bot (pendiente deploy)
│   ├── system_prompt.py
│   ├── notion_client.py
│   ├── drive_client.py
│   └── railway.toml
│
└── p1-reconciliation-app/             # App de reconciliación AP (Proyecto 1)
    └── reconciliation-app.html
```

---

## Comandos disponibles

| Comando | Para qué sirve |
|---------|----------------|
| `/onyx-post` | Crear un post estratégico completo para LinkedIn |
| `/onyx-daily` | Convertir trabajo del día en contenido |
| `/onyx-strategy` | Planificación estratégica de posicionamiento |
| `/onyx-profile` | Auditoría y mejora del perfil de LinkedIn |
| `/onyx-research` | Benchmark y análisis de referentes del sector |
| `/onyx-calendar` | Generar o actualizar calendario editorial |
| `/onyx-review` | Revisión semanal/mensual de contenido y métricas |
| `/onyx-substack` | Crear artículo completo para Substack |
| `/onyx-reddit-research` | Investigación de audiencia en Reddit |
| `/onyx-metrics` | Análisis de rendimiento de posts publicados |

---

## Skills disponibles

Las skills están en `onyx/skills/linkedin-strategy/` y son invocadas automáticamente por Onyx según el contexto:

| Skill | Función |
|-------|---------|
| `insight-extractor` | Extrae insights de experiencias reales |
| `content-angle-generator` | Genera ángulos de contenido distintos para el mismo material |
| `narrative-builder` | Construye narrativa profesional coherente |
| `positioning-auditor` | Audita alineación con el posicionamiento objetivo |
| `authority-builder` | Construye autoridad sin inflación ni fluff |
| `anti-cliche-filter` | Elimina genéricos y corporativismo |
| `hook-generator` | Genera hooks fuertes para posts |
| `post-rewriter` | Reescribe posts débiles sin perder la voz |
| `trend-scanner` | Detecta tendencias relevantes al nicho |
| `competitor-analyzer` | Analiza referentes del sector |
| `idea-gap-finder` | Encuentra huecos de contenido sin explotar |
| `comment-strategy` | Estrategia de comentarios para construir red |
| `feedback-loop` | Análisis de rendimiento de posts publicados |
| `posting-strategy-optimizer` | Optimiza frecuencia y momento de publicación |
| `editorial-calendar-system` | Sistema de calendario editorial |
| `project-story-miner` | Extrae historias de proyectos reales |
| `benchmark-mapper` | Mapea referentes y brechas de posicionamiento |
| `profile-gap-analyzer` | Analiza brechas en el perfil de LinkedIn |
| `proof-of-work-packager` | Empaqueta evidencias reales de forma estratégica |
| `weekly-review-engine` | Motor de revisión semanal |
| `skill-orchestrator` | Orquesta múltiples skills en una sola sesión |
| `memory-skill` | Gestión de memoria contextual entre sesiones |
| `reddit-audience-researcher` | Investigación profunda de audiencia en Reddit |
| `substack-writer` | Redacción de artículos para Substack |
| `platform-content-adapter` | Adapta contenido entre plataformas |

---

## Integraciones

### Notion MCP
Sincronización directa con el workspace de Notion. Tres bases de datos activas:
- **Tareas & Roadmap** — 37 tareas distribuidas en las 16 semanas
- **Posts LinkedIn** — copy completo de los 4 posts de Fase 1
- **Artículos Substack** — 3 artículos Fase 1–2

### Zernio (en setup)
API unificada para LinkedIn y 13 redes más. Habilita:
- Métricas de posts directamente desde Claude (impresiones, engagement, clicks)
- Publicación y programación de posts sin salir de Claude Code
- Best time to post basado en datos reales de la audiencia
- Cierra el loop de `/onyx-metrics` con datos reales sin trabajo manual

**Estado:** API key activa, LinkedIn conectado. Pendiente instalar `uv` para activar el MCP local.

```bash
# Para activar Zernio:
curl -LsSf https://astral.sh/uv/install.sh | sh
# Luego reiniciar Claude Code
```

### Onyx Bot (Telegram — pendiente deploy)
Bot de Telegram que permite interactuar con Onyx fuera de Claude Code. Código completo en `onyx-bot/`. Deploy en Railway pendiente.

---

## Los 5 proyectos (proof of work)

| # | Proyecto | Estado | Semanas |
|---|----------|--------|---------|
| P1 | AP Reconciliation App — parsea statements de vendors, cruza contra Bill.com y NetSuite | ✅ Completo | 1–4 |
| P2 | Vendor Email Automation — email semanal a vendors con Make + Gmail | En pipeline | 3–6 |
| P3 | Slack Bot para Supply — intake estructurado + resumen automático lunes | En pipeline | 5–9 |
| P4 | Invoice Ingestion automática — parsea mails de vendors hacia Sheet central | En pipeline | 8–12 |
| P5 | Post-close Reporting Integration — reporte automático con trigger | En pipeline | 11–14 |

Cada proyecto genera: **1 artículo Substack** + **2–3 posts LinkedIn** con ángulos distintos.

---

## Estrategia de contenido

### LinkedIn — descubrimiento
- 2 posts/semana
- 150–250 palabras, hook directo, líneas cortas
- Todo en inglés, 6–8 hashtags del nicho AP
- Nunca resumir — siempre un ángulo concreto

### Substack — autoridad
- Fase 1–2: 1 artículo cada 2 semanas
- Fase 3+: 1 artículo/semana
- 800–1500 palabras, pedagógico, proceso completo

### Reddit research
- 1 sesión cada 2 semanas
- Subreddits: r/Accounting, r/excel, r/nocode, r/automation, r/sysadmin, r/smallbusiness, r/FinancialCareers
- Output: 5 ideas LinkedIn + 2 ideas Substack por sesión

---

## Roadmap — 16 semanas (inicio marzo 2026)

| Fase | Semanas | Foco |
|------|---------|------|
| Fase 1 | 1–4 | Anclar P1, lanzar P2, post #1–4 |
| Fase 2 | 5–8 | Case studies P2 + P3, stack de herramientas |
| Fase 3 | 9–12 | Portfolio completo + job search activo |
| Fase 4 | 13–16 | Cierre: "5 proyectos, 4 meses, 1 transición" |

---

## Principios de Onyx

- No inventar logros, métricas, herramientas ni responsabilidades
- No generar contenido genérico de LinkedIn
- Cada post es una decisión de posicionamiento
- Voz: profesional, clara, práctica, reflexiva — sin inflación, sin tono influencer
- Siempre preguntar si algo no está claro antes de producir
