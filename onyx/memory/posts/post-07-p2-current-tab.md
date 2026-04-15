# Post #7 — "The vendor analysis that used to take 2 hours"

**Estado:** Listo para publicar
**Fecha sugerida:** Semana 19-20 mayo 2026 (martes o jueves)
**Tipo:** Caso específico — automatización de análisis semanal (Code.gs)
**Proyecto referenciado:** P2 — Code.gs (generación de tab Current)

---

## Versión completa (English)

Every week in AP, you need to know which vendors actually need attention.

Not all of them. Just the ones that matter this week:
- The ones with the largest outstanding balances
- The ones with credits that could offset other invoices
- The ones that are mandatory regardless of amount

Figuring that out used to mean: open the weekly aging sheet, scan 200+ vendors, apply judgment, build a working list.

Now a script does it.

It reads the weekly aging tab, calculates which vendors represent the top X% of total outstanding debt, which represent the top X% of credits, and which are on the mandatory review list.
Then it builds a "Current" tab — sorted, formatted, with vendor contact info and Drive links already populated.

When I open my laptop on Monday, the list is ready.

What changed:
- The selection is consistent — same logic applied every week, not dependent on who's reviewing
- The time to build the working list went from 2 hours to the time it takes the script to run
- I can focus on the actual analysis — not on building the dataset for it

Consistency matters more than speed.
When a process runs the same way every week, you can measure it.
And when you can measure it, you can improve it.

---

## Hashtags

#AccountsPayable #ProcessAutomation #GoogleAppsScript #FinanceOps #Automation #APAutomation #DataQuality

---

## CTA

What's a weekly report you build manually that could run on its own?

---

## Por qué funciona

- Abre con el problema real antes de hablar de la solución
- Explica la lógica de selección (Top X% deuda + créditos + mandatory) — real y específico
- El insight final "consistency matters more than speed" es la ganancia real del script
- "When you can measure it, you can improve it" — pensamiento de sistema, no solo de tarea

---

## Notas de uso

- El "2 hours" puede ajustarse si el tiempo real era diferente — es estimación honesta
- El X% en el script es configurable desde una tab "Principal" — no mencionar eso en el post, añade complejidad innecesaria
- Publicar como texto puro
- Post ideal para acompañar con screenshot del output de la tab Current (con datos anonimizados)
