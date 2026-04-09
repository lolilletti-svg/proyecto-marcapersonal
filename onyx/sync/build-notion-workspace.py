#!/usr/bin/env python3
"""
Construye el workspace completo de Marca personal - Onyx en Notion.
Crea 3 bases de datos + contenido de la página principal.
"""
import requests, json, time, sys

TOKEN = "tu_notion_token"  # Setear en variable de entorno NOTION_TOKEN
PAGE_ID = "32e6e7364ef780bbb3b6e147c74604b0"
BASE_URL = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def api_post(endpoint, data):
    r = requests.post(f"{BASE_URL}/{endpoint}", headers=HEADERS, json=data)
    result = r.json()
    if result.get("object") == "error":
        print(f"  ❌ Error [{endpoint}]: {result.get('message')}")
    time.sleep(0.35)
    return result

def api_patch(endpoint, data):
    r = requests.patch(f"{BASE_URL}/{endpoint}", headers=HEADERS, json=data)
    result = r.json()
    if result.get("object") == "error":
        print(f"  ❌ Error [{endpoint}]: {result.get('message')}")
    time.sleep(0.35)
    return result

# ─── helpers ───────────────────────────────────────────────
def txt(s):       return [{"type": "text", "text": {"content": str(s)}}]
def title_p(s):   return {"title": [{"text": {"content": str(s)}}]}
def select_p(s):  return {"select": {"name": s}}
def rt_p(s):      return {"rich_text": [{"text": {"content": str(s)[:2000]}}]}
def num_p(n):     return {"number": n}
def date_p(d):    return {"date": {"start": d}}

def p_block(s):
    return {"object":"block","type":"paragraph","paragraph":{"rich_text":txt(s)}}
def h2_block(s):
    return {"object":"block","type":"heading_2","heading_2":{"rich_text":txt(s)}}
def h3_block(s):
    return {"object":"block","type":"heading_3","heading_3":{"rich_text":txt(s)}}
def bullet(s):
    return {"object":"block","type":"bulleted_list_item","bulleted_list_item":{"rich_text":txt(s)}}
def divider():
    return {"object":"block","type":"divider","divider":{}}
def callout(s, emoji="⚡"):
    return {"object":"block","type":"callout","callout":{"rich_text":txt(s),"icon":{"type":"emoji","emoji":emoji}}}
def quote(s):
    return {"object":"block","type":"quote","quote":{"rich_text":txt(s)}}

def create_db(parent_id, title, props):
    data = {
        "parent": {"type": "page_id", "page_id": parent_id},
        "title": txt(title),
        "properties": props
    }
    result = api_post("databases", data)
    db_id = result.get("id")
    if db_id:
        print(f"  ✅ DB creada: {title}")
    return db_id

def add_entry(db_id, props, children=None):
    data = {"parent": {"database_id": db_id}, "properties": props}
    if children:
        data["children"] = children
    result = api_post("pages", data)
    return result.get("id")

# ─── PASO 1: contenido de la página principal ───────────────
print("\n📄 Agregando contenido a la página principal...")
main_blocks = [
    callout("Sistema Onyx v3 | LinkedIn 2x/semana + Substack | 16 semanas | Job search activo desde semana 9", "⚡"),
    h2_block("Posicionamiento"),
    quote("Automatizo procesos financieros en AP — reconciliación, comunicación con vendors, intake de datos y reporting — reduciendo tiempo manual y errores operativos."),
    h2_block("Estado actual — Semana 1 (marzo 2026)"),
    bullet("✅ Post #1 listo para publicar — 'Nadie me pidió...'"),
    bullet("🔧 P1 completada — pendiente: README, demo, GitHub"),
    bullet("⏳ P2–P5 definidos, sin empezar"),
    bullet("⏳ Substack: sin artículos publicados aún"),
    bullet("📅 Job search activo desde semana 9 (~mayo 2026)"),
    divider(),
    h2_block("Roadmap rápido"),
    bullet("Fase 1 (sem 1–4): Documentar P1, lanzar P2, primeros posts + Artículo Substack #1"),
    bullet("Fase 2 (sem 5–8): P2 MVP + P3, enseñar no solo contar, Artículo Substack #2"),
    bullet("Fase 3 (sem 9–12): Portfolio completo + job search activo, artículos semanales"),
    bullet("Fase 4 (sem 13–16): Cierre — '5 proyectos, 4 meses, 1 transición'"),
    divider(),
    h2_block("📋 Tareas & Roadmap"),
    p_block("Todas las tareas del roadmap organizadas por fase, semana y fecha. Filtrá por Tipo, Proyecto o Estado."),
    divider(),
    h2_block("✍️ Posts LinkedIn"),
    p_block("Todos los posts con copy completo, hook, CTA, estado y fecha de publicación."),
    divider(),
    h2_block("📰 Artículos Substack"),
    p_block("Artículos planificados con título, resumen, fase y fecha de publicación."),
]
api_patch(f"blocks/{PAGE_ID}/children", {"children": main_blocks})
print("  ✅ Contenido de página principal agregado")

# ─── PASO 2: base de datos Tareas & Roadmap ─────────────────
print("\n📋 Creando base de datos: Tareas & Roadmap...")
tareas_db = create_db(PAGE_ID, "📋 Tareas & Roadmap", {
    "Tarea": {"title": {}},
    "Tipo": {"select": {"options": [
        {"name": "🔨 Proyecto",          "color": "blue"},
        {"name": "📝 Post LinkedIn",     "color": "green"},
        {"name": "📰 Artículo Substack", "color": "purple"},
        {"name": "🔍 Reddit Research",   "color": "orange"},
        {"name": "💼 Job Search",        "color": "red"},
        {"name": "⚙️ General",           "color": "gray"},
    ]}},
    "Proyecto": {"select": {"options": [
        {"name": "P1", "color": "blue"},   {"name": "P2", "color": "green"},
        {"name": "P3", "color": "orange"}, {"name": "P4", "color": "red"},
        {"name": "P5", "color": "purple"}, {"name": "General", "color": "gray"},
    ]}},
    "Fase": {"select": {"options": [
        {"name": "Fase 1", "color": "blue"},  {"name": "Fase 2", "color": "green"},
        {"name": "Fase 3", "color": "orange"},{"name": "Fase 4", "color": "red"},
    ]}},
    "Semana":  {"number": {"format": "number"}},
    "Fecha":   {"date": {}},
    "Estado": {"select": {"options": [
        {"name": "⬜ Por hacer",    "color": "gray"},
        {"name": "🔄 En progreso", "color": "blue"},
        {"name": "✅ Listo",       "color": "green"},
        {"name": "🚀 Publicado",   "color": "purple"},
    ]}},
    "Notas": {"rich_text": {}},
})

tasks = [
    # FASE 1 ── Semana 1
    ("Documentar P1: escribir README",                        "🔨 Proyecto",          "P1",      "Fase 1", 1,  "2026-03-24", "🔄 En progreso"),
    ("Documentar P1: comentar el código",                     "🔨 Proyecto",          "P1",      "Fase 1", 1,  "2026-03-25", "⬜ Por hacer"),
    ("Grabar demo corto de P1 (2–3 min)",                     "🔨 Proyecto",          "P1",      "Fase 1", 1,  "2026-03-26", "⬜ Por hacer"),
    ("Publicar Post #1 — Nadie me pidió...",                  "📝 Post LinkedIn",     "P1",      "Fase 1", 1,  "2026-03-27", "✅ Listo"),
    # FASE 1 ── Semana 2
    ("Subir P1 a GitHub con README",                          "🔨 Proyecto",          "P1",      "Fase 1", 2,  "2026-03-31", "⬜ Por hacer"),
    ("Publicar Post #2 — Lo que encontré cuando documenté",   "📝 Post LinkedIn",     "P1",      "Fase 1", 2,  "2026-04-01", "⬜ Por hacer"),
    ("Reddit Research — Sesión baseline de audiencia",        "🔍 Reddit Research",   "General", "Fase 1", 2,  "2026-04-02", "⬜ Por hacer"),
    ("Publicar Post #3 — Por qué saber procesos vale más que código", "📝 Post LinkedIn", "General","Fase 1",2,"2026-04-03","⬜ Por hacer"),
    # FASE 1 ── Semana 3
    ("Arrancar P2: setup Make/script + Gmail",                "🔨 Proyecto",          "P2",      "Fase 1", 3,  "2026-04-07", "⬜ Por hacer"),
    ("Publicar Post #4 — Demo visual: así funciona la app",   "📝 Post LinkedIn",     "P1",      "Fase 1", 3,  "2026-04-08", "⬜ Por hacer"),
    ("P2: lógica de automatización del email de jueves",      "🔨 Proyecto",          "P2",      "Fase 1", 3,  "2026-04-09", "⬜ Por hacer"),
    ("Publicar Post #5 — ¿Por qué Excel sigue siendo #1 de AP?","📝 Post LinkedIn",  "General", "Fase 1", 3,  "2026-04-10", "⬜ Por hacer"),
    # FASE 1 ── Semana 4
    ("P2: testing + ajustes del automation",                  "🔨 Proyecto",          "P2",      "Fase 1", 4,  "2026-04-14", "⬜ Por hacer"),
    ("Publicar Post #6 — El problema de los procesos que solo vos sabés hacer","📝 Post LinkedIn","General","Fase 1",4,"2026-04-15","⬜ Por hacer"),
    ("Escribir Artículo Substack #1 — borrador completo",     "📰 Artículo Substack", "P1",      "Fase 1", 4,  "2026-04-16", "⬜ Por hacer"),
    ("Publicar Post #7 — Make vs script: qué elegí y por qué","📝 Post LinkedIn",    "P2",      "Fase 1", 4,  "2026-04-17", "⬜ Por hacer"),
    ("Publicar Artículo Substack #1 — Cómo construí la app", "📰 Artículo Substack", "P1",      "Fase 1", 4,  "2026-04-19", "⬜ Por hacer"),
    # FASE 2 ── Semana 5
    ("P2 MVP: completar, documentar y subir a GitHub",        "🔨 Proyecto",          "P2",      "Fase 2", 5,  "2026-04-21", "⬜ Por hacer"),
    ("Publicar Post #8 — Cómo normalizar facturas entre 3 sistemas","📝 Post LinkedIn","General","Fase 2",5,"2026-04-22","⬜ Por hacer"),
    ("Arrancar P3: diseño del Slack bot para Supply",         "🔨 Proyecto",          "P3",      "Fase 2", 5,  "2026-04-23", "⬜ Por hacer"),
    ("Publicar Post — P2 case study: resultado del email automation","📝 Post LinkedIn","P2",    "Fase 2", 5,  "2026-04-24", "⬜ Por hacer"),
    # FASE 2 ── Semana 6
    ("Reddit Research — Sesión ajuste de temas",              "🔍 Reddit Research",   "General", "Fase 2", 6,  "2026-04-28", "⬜ Por hacer"),
    ("Publicar Post — Preview P3: construyendo un Slack bot", "📝 Post LinkedIn",     "P3",      "Fase 2", 6,  "2026-04-29", "⬜ Por hacer"),
    ("P3: setup Slack API + modal de intake",                 "🔨 Proyecto",          "P3",      "Fase 2", 6,  "2026-04-30", "⬜ Por hacer"),
    ("Escribir Artículo Substack #2 — El stack mínimo para AP automation","📰 Artículo Substack","General","Fase 2",6,"2026-05-01","⬜ Por hacer"),
    # FASE 2 ── Semana 7
    ("Publicar Artículo Substack #2 — El stack mínimo viable","📰 Artículo Substack", "General", "Fase 2", 7,  "2026-05-05", "⬜ Por hacer"),
    ("P3: backend en Google Sheets/Airtable",                 "🔨 Proyecto",          "P3",      "Fase 2", 7,  "2026-05-06", "⬜ Por hacer"),
    ("Publicar Post — Insight: diseño de formularios de intake","📝 Post LinkedIn",   "P3",      "Fase 2", 7,  "2026-05-07", "⬜ Por hacer"),
    ("P3: automatizar resumen de lunes",                      "🔨 Proyecto",          "P3",      "Fase 2", 7,  "2026-05-08", "⬜ Por hacer"),
    ("Publicar Post — Aprendizaje técnico de P3",             "📝 Post LinkedIn",     "P3",      "Fase 2", 7,  "2026-05-09", "⬜ Por hacer"),
    # FASE 2 ── Semana 8
    ("P3: testing con el equipo de Supply",                   "🔨 Proyecto",          "P3",      "Fase 2", 8,  "2026-05-12", "⬜ Por hacer"),
    ("Publicar Post — Así funciona el Slack bot para Supply", "📝 Post LinkedIn",     "P3",      "Fase 2", 8,  "2026-05-14", "⬜ Por hacer"),
    ("Publicar Post — Aprendizaje P3: perspectiva de proceso","📝 Post LinkedIn",     "P3",      "Fase 2", 8,  "2026-05-16", "⬜ Por hacer"),
    ("Preparar portfolio: docs P1 + P2 + P3",                 "⚙️ General",           "General", "Fase 2", 8,  "2026-05-17", "⬜ Por hacer"),
    # FASE 3 ── Semana 9
    ("ACTIVAR JOB SEARCH — empezar a aplicar",                "💼 Job Search",        "General", "Fase 3", 9,  "2026-05-19", "⬜ Por hacer"),
    ("Reddit Research — Sesión: qué buscan en finance ops",   "🔍 Reddit Research",   "General", "Fase 3", 9,  "2026-05-20", "⬜ Por hacer"),
    ("Publicar Post — Case study completo P2 email automation","📝 Post LinkedIn",    "P2",      "Fase 3", 9,  "2026-05-21", "⬜ Por hacer"),
    ("Publicar Artículo Substack #3 — Documentar antes de automatizar","📰 Artículo Substack","General","Fase 3",9,"2026-05-22","⬜ Por hacer"),
    ("Publicar Post — Arquitectura visual P3",                "📝 Post LinkedIn",     "P3",      "Fase 3", 9,  "2026-05-23", "⬜ Por hacer"),
    # FASE 3 ── Semana 10
    ("Arrancar P4: setup email parsing (Imperial, US Foods, Cisco)","🔨 Proyecto",    "P4",      "Fase 3", 10, "2026-05-26", "⬜ Por hacer"),
    ("Publicar Post — Cómo automaticé el intake de Supply vía Slack","📝 Post LinkedIn","P3",   "Fase 3", 10, "2026-05-28", "⬜ Por hacer"),
    ("Escribir Artículo Substack #4 — Historia completa P3",  "📰 Artículo Substack", "P3",      "Fase 3", 10, "2026-05-29", "⬜ Por hacer"),
    ("Publicar Post — Portfolio update + job search activo",  "📝 Post LinkedIn",     "General", "Fase 3", 10, "2026-05-30", "⬜ Por hacer"),
    # FASE 3 ── Semana 11
    ("P4: parseo PDF→Sheet centralizado",                     "🔨 Proyecto",          "P4",      "Fase 3", 11, "2026-06-02", "⬜ Por hacer"),
    ("Publicar Artículo Substack #4",                         "📰 Artículo Substack", "P3",      "Fase 3", 11, "2026-06-03", "⬜ Por hacer"),
    ("Publicar Post — Automatizando intake de facturas de vendors","📝 Post LinkedIn","P4",      "Fase 3", 11, "2026-06-04", "⬜ Por hacer"),
    ("Publicar Post — Insight técnico P4: email parsing",     "📝 Post LinkedIn",     "P4",      "Fase 3", 11, "2026-06-06", "⬜ Por hacer"),
    # FASE 3 ── Semana 12
    ("P4 MVP completado + documentar + GitHub",               "🔨 Proyecto",          "P4",      "Fase 3", 12, "2026-06-09", "⬜ Por hacer"),
    ("Publicar Post — Arquitectura completa del portfolio (4 proyectos)","📝 Post LinkedIn","General","Fase 3",12,"2026-06-11","⬜ Por hacer"),
    ("Escribir Artículo Substack #5 — Framework: cómo pienso un proceso antes de automatizar","📰 Artículo Substack","General","Fase 3",12,"2026-06-12","⬜ Por hacer"),
    ("Publicar Post — '5 proyectos, lo que aprendí hasta acá'","📝 Post LinkedIn",   "General", "Fase 3", 12, "2026-06-13", "⬜ Por hacer"),
    # FASE 4 ── Semana 13
    ("Publicar Artículo Substack #5",                         "📰 Artículo Substack", "General", "Fase 4", 13, "2026-06-16", "⬜ Por hacer"),
    ("Arrancar P5 si da el tiempo (post-close reporting)",    "🔨 Proyecto",          "P5",      "Fase 4", 13, "2026-06-17", "⬜ Por hacer"),
    ("Publicar Post — Entrevistas en curso / job search progress","📝 Post LinkedIn", "General", "Fase 4", 13, "2026-06-19", "⬜ Por hacer"),
    ("Publicar Post — Learnings de 3 meses construyendo en público","📝 Post LinkedIn","General","Fase 4",13,"2026-06-21","⬜ Por hacer"),
    # FASE 4 ── Semana 14
    ("Publicar Post — Insight de entrevistas en finance ops", "📝 Post LinkedIn",     "General", "Fase 4", 14, "2026-06-25", "⬜ Por hacer"),
    ("Escribir Artículo Substack cierre — 5 proyectos, 4 meses, 1 transición","📰 Artículo Substack","General","Fase 4",14,"2026-06-26","⬜ Por hacer"),
    ("Publicar Post — Case study final (el proyecto más impactante)","📝 Post LinkedIn","General","Fase 4",14,"2026-06-27","⬜ Por hacer"),
    # FASE 4 ── Semana 15
    ("Publicar Post — Cierre: lo que me llevé de 4 meses de content","📝 Post LinkedIn","General","Fase 4",15,"2026-07-02","⬜ Por hacer"),
    ("Publicar Post — Transición completada (si corresponde)","📝 Post LinkedIn",     "General", "Fase 4", 15, "2026-07-04", "⬜ Por hacer"),
    # FASE 4 ── Semana 16
    ("Publicar Artículo Substack CIERRE — 5 proyectos, 4 meses, 1 transición","📰 Artículo Substack","General","Fase 4",16,"2026-07-11","⬜ Por hacer"),
    ("Revisión final: sistema Onyx + contenido + resultados", "⚙️ General",           "General", "Fase 4", 16, "2026-07-13", "⬜ Por hacer"),
]

print(f"  Cargando {len(tasks)} tareas...")
for i, (nombre, tipo, proyecto, fase, semana, fecha, estado) in enumerate(tasks):
    add_entry(tareas_db, {
        **title_p(nombre),
        "Tipo":     select_p(tipo),
        "Proyecto": select_p(proyecto),
        "Fase":     select_p(fase),
        "Semana":   num_p(semana),
        "Fecha":    date_p(fecha),
        "Estado":   select_p(estado),
    })
    if (i+1) % 10 == 0:
        print(f"    {i+1}/{len(tasks)}...")
print(f"  ✅ {len(tasks)} tareas cargadas")

# ─── PASO 3: base de datos Posts LinkedIn ───────────────────
print("\n✍️  Creando base de datos: Posts LinkedIn...")
posts_db = create_db(PAGE_ID, "✍️ Posts LinkedIn", {
    "Título": {"title": {}},
    "Hook":   {"rich_text": {}},
    "Estado": {"select": {"options": [
        {"name": "📌 Idea",                  "color": "gray"},
        {"name": "✍️ Borrador",              "color": "yellow"},
        {"name": "✅ Listo para publicar",   "color": "green"},
        {"name": "🚀 Publicado",             "color": "purple"},
    ]}},
    "Proyecto": {"select": {"options": [
        {"name": "P1", "color": "blue"},   {"name": "P2", "color": "green"},
        {"name": "P3", "color": "orange"}, {"name": "P4", "color": "red"},
        {"name": "P5", "color": "purple"}, {"name": "General", "color": "gray"},
    ]}},
    "Semana":            {"number": {"format": "number"}},
    "Fecha publicación": {"date": {}},
    "CTA":               {"rich_text": {}},
})

POST1_COPY = """Nadie me pidió que mejorara el proceso de reconciliación de vendors.

Era funcional. Lo hacía de memoria. Nadie se quejaba.

Pero todas las semanas: tabs de Excel apiladas, vlookups que se rompían, statements en PDF que convertía a mano, facturas que no matcheaban porque el número estaba escrito distinto en cada sistema.

Un día decidí documentarlo para entenderlo mejor.

Y cuando lo tuve escrito, me di cuenta de algo incómodo: estaba ejecutando un proceso que dependía completamente de que yo no me equivocara. Sin respaldo. Sin trazabilidad. Sin lógica que pudiera transferirle a alguien más.

Entonces lo automaticé.

No soy developer. Usé Claude para construir una app desde cero: parsea statements de vendors (PDF o Excel), los cruza contra Bill y NetSuite, consolida múltiples ubicaciones, normaliza números de factura, y exporta el resultado.

Lo que aprendí no fue sobre código. Fue que cuando tenés que explicarle un proceso a una IA con suficiente precisión como para que lo construya — primero tenés que entenderlo vos.

Eso es lo que entrena AP todos los días. Y es lo que estoy empezando a documentar y mostrar."""

posts = [
    # (título, hook, estado, proyecto, semana, fecha, cta, copy_completo)
    (
        "Post #1 — Nadie me pidió...",
        "Nadie me pidió que mejorara el proceso de reconciliación de vendors.",
        "✅ Listo para publicar", "P1", 1, "2026-03-27",
        "¿Qué proceso de tu trabajo depende de que vos específicamente no te equivoques?",
        POST1_COPY
    ),
    (
        "Post #2 — Lo que encontré cuando documenté",
        "Lo que encontré cuando documenté mi proceso de reconciliación.",
        "📌 Idea", "P1", 2, "2026-04-01", "", ""
    ),
    (
        "Post #3 — Por qué saber procesos vale más que código",
        "Saber código te hace más rápido. Saber procesos te hace más valioso.",
        "📌 Idea", "General", 2, "2026-04-03", "", ""
    ),
    (
        "Post #4 — Demo visual: así funciona la app de reconciliación",
        "Así se ve el antes y el después de automatizar la reconciliación de vendors.",
        "📌 Idea", "P1", 3, "2026-04-08", "", ""
    ),
    (
        "Post #5 — ¿Por qué Excel sigue siendo #1 de AP?",
        "¿Por qué Excel sigue siendo la herramienta #1 de AP en 2026? Una respuesta honesta.",
        "📌 Idea", "General", 3, "2026-04-10", "", ""
    ),
    (
        "Post #6 — El problema de los procesos que solo vos sabés hacer",
        "El proceso más peligroso de tu equipo no es el más complejo — es el que solo una persona sabe hacer.",
        "📌 Idea", "General", 4, "2026-04-15", "", ""
    ),
    (
        "Post #7 — Make vs script: qué elegí y por qué",
        "Make vs script: qué elegí para automatizar mi email semanal de vendors y por qué lo cambiaría.",
        "📌 Idea", "P2", 4, "2026-04-17", "", ""
    ),
    (
        "Post #8 — Cómo normalizar facturas entre 3 sistemas",
        "Cómo normalizar el número de factura entre Bill, NetSuite y el statement del vendor sin perder el hilo.",
        "📌 Idea", "General", 5, "2026-04-22", "", ""
    ),
]

print(f"  Cargando {len(posts)} posts...")
for titulo, hook, estado, proyecto, semana, fecha, cta, copy in posts:
    children = None
    if copy:
        children = [
            h2_block("Copy completo"),
            *[p_block(par) for par in copy.split("\n\n") if par.strip()],
            divider(),
            h3_block("CTA"),
            p_block(cta),
        ]
    add_entry(posts_db, {
        **title_p(titulo),
        "Hook":              rt_p(hook),
        "Estado":            select_p(estado),
        "Proyecto":          select_p(proyecto),
        "Semana":            num_p(semana),
        "Fecha publicación": date_p(fecha),
        "CTA":               rt_p(cta),
    }, children)

print(f"  ✅ {len(posts)} posts cargados")

# ─── PASO 4: base de datos Artículos Substack ───────────────
print("\n📰 Creando base de datos: Artículos Substack...")
substack_db = create_db(PAGE_ID, "📰 Artículos Substack", {
    "Título":   {"title": {}},
    "Resumen":  {"rich_text": {}},
    "Estado": {"select": {"options": [
        {"name": "💡 Idea",        "color": "gray"},
        {"name": "✍️ En proceso",  "color": "yellow"},
        {"name": "✅ Listo",       "color": "green"},
        {"name": "🚀 Publicado",   "color": "purple"},
    ]}},
    "Proyecto": {"select": {"options": [
        {"name": "P1", "color": "blue"},   {"name": "P2", "color": "green"},
        {"name": "P3", "color": "orange"}, {"name": "P4", "color": "red"},
        {"name": "P5", "color": "purple"}, {"name": "General", "color": "gray"},
    ]}},
    "Fase": {"select": {"options": [
        {"name": "Fase 1", "color": "blue"},  {"name": "Fase 2", "color": "green"},
        {"name": "Fase 3", "color": "orange"},{"name": "Fase 4", "color": "red"},
    ]}},
    "Semana publicación": {"number": {"format": "number"}},
    "Fecha publicación":  {"date": {}},
    "Companion post LinkedIn": {"rich_text": {}},
})

articles = [
    (
        "Artículo #1 — Cómo construí una app de reconciliación sin saber programar",
        "Historia completa de P1: el problema, el proceso, las herramientas, lo que aprendí. Formato narrativo con secciones pedagógicas. ~1200 palabras.",
        "💡 Idea", "P1", "Fase 1", 4, "2026-04-19",
        "Post #7 — Make vs script (mismo período, ángulo diferente)"
    ),
    (
        "Artículo #2 — El stack mínimo viable para automatizar AP en 2026",
        "Guía práctica con herramientas reales: Claude API, Make, Slack API, Google Sheets. Cuándo usar cada una, por qué, y qué no funcionó.",
        "💡 Idea", "General", "Fase 2", 7, "2026-05-05",
        "Post — P2 case study (ángulo resultado vs. ángulo herramientas)"
    ),
    (
        "Artículo #3 — Documentar antes de automatizar: el paso que todos saltan",
        "Por qué documentar el proceso ANTES de automatizarlo es el paso más importante y el más ignorado. Framework de 4 preguntas.",
        "💡 Idea", "General", "Fase 3", 9, "2026-05-22",
        "Post — Arquitectura visual P3"
    ),
    (
        "Artículo #4 — Cómo construí un Slack bot para Supply sin ser dev",
        "Historia completa de P3: necesidad real, diseño del flujo, Slack API + Sheets, testing con el equipo, resultados operativos.",
        "💡 Idea", "P3", "Fase 3", 11, "2026-06-03",
        "Post — Así funciona el Slack bot para Supply"
    ),
    (
        "Artículo #5 — Cómo pienso un proceso antes de automatizarlo",
        "El framework mental: qué automatizar, cómo documentarlo, cómo validar que vale la pena. Basado en 4 proyectos reales.",
        "💡 Idea", "General", "Fase 3", 12, "2026-06-16",
        "Post — Arquitectura completa del portfolio"
    ),
    (
        "Artículo CIERRE — 5 proyectos, 4 meses, 1 transición",
        "El cierre del roadmap: qué construí, qué aprendí, qué cambió, hacia dónde voy. Narrativa completa de la transición de AP a automation.",
        "💡 Idea", "General", "Fase 4", 16, "2026-07-11",
        "Post — Transición completada"
    ),
]

print(f"  Cargando {len(articles)} artículos...")
for titulo, resumen, estado, proyecto, fase, semana, fecha, companion in articles:
    add_entry(substack_db, {
        **title_p(titulo),
        "Resumen":                 rt_p(resumen),
        "Estado":                  select_p(estado),
        "Proyecto":                select_p(proyecto),
        "Fase":                    select_p(fase),
        "Semana publicación":      num_p(semana),
        "Fecha publicación":       date_p(fecha),
        "Companion post LinkedIn": rt_p(companion),
    })

print(f"  ✅ {len(articles)} artículos cargados")

# ─── RESUMEN FINAL ──────────────────────────────────────────
print(f"""
╔══════════════════════════════════════════╗
║  ✅  Workspace construido con éxito       ║
╠══════════════════════════════════════════╣
║  📋 Tareas & Roadmap  →  {len(tasks)} tareas        ║
║  ✍️  Posts LinkedIn    →  {len(posts)} posts         ║
║  📰 Artículos Substack →  {len(articles)} artículos     ║
╚══════════════════════════════════════════╝
""")
