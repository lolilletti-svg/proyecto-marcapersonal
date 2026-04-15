# Substack Artículo #1 — AP Reconciliation App

**Título:** How I built an AP reconciliation app without knowing how to code
**Estado:** Borrador completo — listo para revisar y publicar
**Fecha sugerida:** Jueves 24 abril 2026
**Largo estimado:** 1.200–1.500 palabras
**Proyecto:** P1 — AP Reconciliation App

---

## INTRO

Every week, I spent 2+ hours matching vendor statements against two financial systems.

Not because the process was complicated. Because it was entirely manual.

I had a system — Excel tabs, vlookups, color coding — and it worked. Until it didn't.
The vlookup would break. The PDF wouldn't convert cleanly. The vendor would format invoice numbers differently from how we stored them in NetSuite.

Each of those exceptions required me to stop, think, fix, and continue.
And I was the only one who knew how to handle them.

This is the story of how I automated that process — and what I actually learned in the process.

---

## 1. The problem wasn't the task. It was the fragility.

[Body: describir el proceso manual — Excel tabs apiladas, vlookups rotos, conversión de PDF a mano, leading zeros, multi-location vendors. No es que tardaba mucho: era que dependía completamente de que Lucía no se equivocara. Sin respaldo, sin trazabilidad, sin lógica transferible.]

Key line: "I wasn't just running the reconciliation. I was the reconciliation."

---

## 2. Before automating, I had to document

[Body: el momento incómodo de escribir el proceso paso a paso. Los tres fixes que encontró que nunca había nombrado: (1) convertir PDFs a mano, (2) normalizar leading zeros, (3) consolidar ubicaciones. No los notó hasta que tuvo que explicárselos a Claude.]

Key line: "You can't automate a process you haven't fully understood. And you can't fully understand it until you have to explain it to something that won't guess."

---

## 3. Building the app: what that actually looked like

[Body: cómo usó Claude API + JS + HTML. No fue "le pedí que hiciera una app." Fue iterativo: primero el parser de Excel, luego el matching de facturas, luego el fix de leading zeros, luego el handler de múltiples ubicaciones. Cada fix surgió de un caso real que apareció en los datos.]

Technical details (non-developer friendly):
- Input: PDF o Excel del vendor statement
- Paso 1: parsear el archivo y extraer números de factura + montos
- Paso 2: normalizar (strip leading zeros, lowercase, quitar caracteres especiales)
- Paso 3: cruzar contra Bill.com y NetSuite
- Paso 4: consolidar vendors multi-location
- Output: Excel con matched, unmatched, y discrepancias marcadas

Key line: "The hardest part wasn't writing the code. It was writing down every exception I had been handling silently for months."

---

## 4. What it does now

[Body: descripción del flujo automatizado. Subir un archivo → resultado en segundos. Lo que tardaba 2+ horas por vendor ahora tarda menos de un minuto. Pero lo más importante no es la velocidad — es que el proceso es ahora auditable, transferible, y consistente.]

Key line: "Speed was a side effect. The real gain was that the process no longer depended on me being there."

---

## 5. What this taught me about AP work

[Body: el insight de fondo. AP builds a very specific skill: the ability to decompose messy, exception-heavy processes into clean logic. That's also exactly what automation requires. The people who understand the process deeply are the ones who can automate it well — not the developers who've never touched a vendor statement.]

Key line: "AP isn't a dead-end role. It's a process design role that most people don't realize they're doing."

---

## CIERRE

[Body: no es un tutorial de código — es un caso de estudio de cómo pensar en procesos. El próximo artículo va a ser sobre el script que alimenta este app: el que solicita automáticamente los statements a los vendors cada lunes. Porque el pipeline completo empieza antes de que llegue el archivo.]

CTA: Si trabajás en finance ops y querés ver el código o hacerle preguntas al proceso, respondé este email — estoy documentando cada decisión mientras lo construyo.

---

## NOTAS DE EDICIÓN

- No inventar métricas exactas — "2+ hours" es honesto, no agregar porcentajes sin base real
- El tono es de practitioner compartiendo aprendizajes, no de experto dando lecciones
- Agregar el link al GitHub del proyecto una vez subido
- Imagen de cabecera sugerida: screenshot del output de la app (con datos anonimizados)
