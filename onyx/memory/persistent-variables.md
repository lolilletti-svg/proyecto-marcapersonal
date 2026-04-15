# Persistent variables

- current_role: Accounts Payable Lead
- desired_positioning: automatización de procesos financieros — reconciliación, comunicación con vendors, intake de datos y reporting — reduciendo tiempo manual y errores operativos
- target_audience: recruiters de ops/finanzas, hiring managers de finance ops y automation, managers de procesos, profesionales en transición de roles operativos
- target_transition: de AP Lead a roles de automatización de procesos / finance ops (objetivo: 3–4 meses)
- content_pillars: automatización de procesos manuales, eficiencia operativa, lecciones desde AP, herramientas prácticas, pensamiento de procesos transferible
- no_go_topics: política, empresas empleadoras por nombre, métricas inventadas, vida personal
- voice_preferences: profesional, clara, práctica, reflexiva, sin inflación, sin tono influencer
- post_format_fixed: TODOS los posts llevan (1) emojis en bullets + 👉 insight + 💭 CTA, (2) imagen o video provista por Lucía. Sin excepciones. No publicar sin visual.
- tools_used: Claude API, JavaScript, HTML, Excel, Bill.com, NetSuite, Make (a evaluar), Slack API, Google Sheets
- weak_patterns_to_avoid: generalizaciones sin base real, métricas inventadas, frases corporativas vacías, tono de gurú
- posting_frequency: LinkedIn 2x/semana | Substack 1x/2 semanas (Fase 1–2), 1x/semana (Fase 3+)
- posting_time_optimal: 8:30am ART (11:30 UTC) — martes y jueves. Dato combinado: Post #1 (18:30) 4.6x más impresiones que Post #2 (20:30) + B2B LinkedIn best practice (mañana > tarde). Experimento activo: Post #3 viernes 17 abr 8:30am para validar.
- linkedin_metrics_baseline: Post #1: 1326 imp, 877 alc, 2.79% eng | Post #2: 290 imp, 179 alc, 2.07% eng
- audience_confirmed: AP specialists + finance ops con experiencia, enterprise (10k+ empleados), alcance internacional cuando el tema es universal. Empresas que ya llegaron: EY, ExxonMobil, Air Liquide, Genpact, NetSuite.
- comment_protocol: responder TODOS los comentarios en las primeras 2 horas post-publicación. No responder con "gracias" — responder con pregunta de vuelta o dato adicional.
- substack_funnel: activar mención de Substack en Post #4 o #5. Sin menciones todavía.
- zernio_status: MCP activo (uvx). Bug en posts_create → usar REST API directamente (POST luego PUT). Post #3 programado ID: 69debc75e13608bd119221f2
- notion_workaround: Notion MCP no carga → usar REST API directo con token del settings.json
- channels: LinkedIn (descubrimiento y visibilidad) + Substack (autoridad y profundidad)
- substack_cadence: Fase 1–2: 1 artículo cada 2 semanas | Fase 3+: 1 artículo por semana
- reddit_research_cadence: 1 sesión cada 2 semanas — subreddits: r/Accounting, r/excel, r/nocode, r/automation, r/sysadmin, r/smallbusiness, r/FinancialCareers
- channel_relationship: LinkedIn genera descubrimiento → Substack genera autoridad. Cada proyecto genera 1 artículo Substack + 2–3 posts LinkedIn
- 3_4_month_goal: conseguir rol en automatización de procesos / finance ops
- 6_month_goal: ser reconocida como referente en automatización de procesos AP y tener entrevistas activas
- 12_month_goal: transición completada hacia rol vinculado a automatización, mejora continua u ops design

## Proyectos activos (roadmap 16 semanas)

### Proyecto 1 — AP Reconciliation App (COMPLETADO)
- Herramientas: Claude API, JavaScript, HTML, Excel
- Estado: construida, funciona — Posts #1 (publicado) y #2 (publicado) en LinkedIn. Posts #3 y #4 programados.
- Proof of work #1 — ancla de toda la narrativa

### Proyecto 2 — Vendor Statement Automation (COMPLETADO)
- Herramientas: Google Apps Script (Mail.gs, DriveSync.gs, Code.gs)
- Estado: en producción — envía emails lunes 8am, sincroniza Drive, genera tab Current
- Posts #5, #6, #7 listos en Notion y Zernio. Artículo Substack #2 borrador listo.

### Proyecto 3 — Slack Bot para Supply (semanas 5–9)
- Herramientas: Slack API, Google Sheets o Airtable
- Objetivo: formulario de intake estructurado para equipo de Supply vía Slack + resumen lunes
- Estado: por empezar

### Proyecto 4 — Invoice Ingestion automática (semanas 8–12)
- Herramientas: email parsing, PDF → Sheet, APIs
- Objetivo: parsear mails de vendors (Imperial, US Foods, Cisco), consolidar en Sheet
- Estado: por empezar

### Proyecto 5 — Post-close Reporting Integration (semanas 11–14)
- Herramientas: trigger automático, generación de reporte
- Objetivo: reporte post-cierre generado automáticamente con trigger
- Estado: por empezar

## Posicionamiento final (para posts y entrevistas)

"Automatizo procesos financieros en AP — reconciliación, comunicación con vendors,
intake de datos y reporting — reduciendo tiempo manual y errores operativos."
