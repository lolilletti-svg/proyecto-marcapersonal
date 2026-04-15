# Proyecto 2 — Vendor Statement Request Automation

**Estado:** COMPLETADO
**Timeline:** Semanas 1–3 (completado junto a P1)
**Proof of work:** #2
**Herramientas:** Google Apps Script, Gmail, Google Sheets

---

## Problema

Para correr la reconciliación de vendors (P1), primero necesitás los updated statements de cada vendor. Antes:
- Solicitud manual a cada vendor por mail
- Sin trigger sistemático — dependía de que alguien se acordara
- Sin tracking de quién respondió y quién no
- Proceso desconectado de la app de reconciliación

## Solución construida

Script de Google Apps Script vinculado a Gmail que:
- Se ejecuta automáticamente los lunes
- Envía emails a vendors solicitando su updated statement de la semana
- Los statements que llegan de respuesta son exactamente los archivos que entran a la AP Reconciliation App (P1)

## Integración con P1

P2 → P1 forman un workflow completo:
1. Lunes: script envía emails automáticos a vendors pidiendo updated statements
2. Vendors responden con statements (PDF o Excel)
3. Esos statements son el input de la AP Reconciliation App
4. La app parsea, cruza contra Bill.com/NetSuite, exporta resultado

## Insight clave (para posts y Substack)

No son dos proyectos separados — es un pipeline. P2 genera el input que P1 procesa.
Esto hace la narrativa más poderosa: automatizaste el ciclo completo de reconciliación,
no solo una parte.

## Contenido planificado (actualizado)

- Post: "El script que prepara el trabajo para mi app de reconciliación" (P2 como upstream de P1)
- Post ángulo workflow: "Así se ve el pipeline completo: de email automático a reporte de reconciliación"
- Substack: P2 + P1 como caso de estudio de un workflow end-to-end
- Ángulo para entrevistas: "automaticé el ciclo completo — solicitud de statements + reconciliación"

## Detalles técnicos (a documentar)

- [ ] Nombre exacto del script en Google Apps Script
- [ ] Trigger: lunes a qué hora
- [ ] Lista de vendors incluidos
- [ ] Template del email que se envía
- [ ] Cómo llegan los statements (adjunto? body? formato?)
- [ ] Subir a GitHub como parte del portfolio
