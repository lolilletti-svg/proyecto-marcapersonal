# Post #5 — "The pipeline: how P2 feeds P1"

**Estado:** Listo para publicar
**Fecha sugerida:** Semana 5-6 mayo 2026 (martes o jueves)
**Tipo:** Workflow end-to-end — el ángulo más poderoso de P2
**Proyecto referenciado:** P2 + P1 — pipeline completo

---

## Versión completa (English)

I didn't realize I had built a pipeline until it was already running.

Project 1 was an app that reconciles vendor statements against Bill.com and NetSuite.
It worked. But it assumed someone had already requested the statements.

That someone was me. Every week. Manually.

So I built Project 2: a Google Apps Script that runs every Monday at 8 AM
and sends statement requests to every vendor in my portfolio — automatically.

Now the workflow looks like this:
1. Monday: script sends emails to vendors requesting updated statements
2. Vendors reply with PDFs or Excel files
3. Those files go directly into the AP Reconciliation App
4. App parses, matches, flags discrepancies, exports result

I automated the request.
Then I automated what happens after the request.

Neither project was designed to connect to the other.
They connected because they were solving the same workflow from different ends.

That's what happens when you document processes carefully enough to see where the gaps are.

---

## Hashtags

#AccountsPayable #ProcessAutomation #FinanceOps #GoogleAppsScript #Automation #NoCode #WorkflowDesign

---

## CTA

Have you ever automated one part of a process and then realized the step before it also needed to be automated?

---

## Por qué funciona

- Cuenta una historia de evolución, no un anuncio de producto
- El insight "they connected because they were solving the same workflow from different ends" es genuino y difícil de inventar
- Muestra pensamiento de sistemas, no solo habilidad técnica
- Alta resonancia en audiencia de ops/finance/automation

---

## Notas de uso

- No modificar la estructura narrativa — la progresión 1→2→workflow completo es el corazón
- Publicar como texto puro, sin imagen necesaria
- Si se agrega imagen: diagrama simple del pipeline (flecha: Email → Statement → App → Report)
