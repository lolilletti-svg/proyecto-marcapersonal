# Proyecto 2 — Vendor Email Automation

**Estado:** Por empezar
**Timeline:** Semanas 3–6
**Proof of work:** #2

---

## Problema

Email semanal de seguimiento a vendors (cada jueves) es manual:
- Redacción repetitiva con variaciones mínimas
- Tiempo dedicado a personalización básica (nombre, número, monto)
- Sin log de quién respondió, quién no, y qué dijo
- Coordinación reactiva en lugar de sistemática

## Solución objetivo

MVP: automatización del envío del mail de los jueves + log de respuestas:
- Trigger semanal (jueves)
- Template con campos variables (vendor, factura, monto, fecha)
- Envío automático desde Gmail/Outlook
- Log de respuestas en Google Sheets o similar

## Herramientas (a definir)

- Make (recomendado sobre Zapier — más flexible para flujos AP)
- Gmail o Outlook (según entorno laboral)
- Google Sheets (log de tracking)

## Impacto esperado

- Eliminar tiempo de redacción y envío manual
- Crear registro estructurado de comunicaciones con vendors
- Reducir seguimientos perdidos o duplicados

## Insight clave (para posts)

El proceso antes: reactivo, sin log, dependiente de memoria.
El proceso después: sistemático, registrado, replicable.

## Contenido planificado (fase 2)

- Case study: "Cómo automaticé la comunicación semanal con vendors"
- Post de error: "El error que cometí en mi primera automatización de emails"
- Post antes/después: "3 horas vs 20 minutos"

## Pendientes

- [ ] Mapear flujo actual del mail: a quiénes, qué dice, qué varía
- [ ] Elegir Make o script (recomendación: Make para MVP)
- [ ] Armar template base
- [ ] Configurar trigger + log
- [ ] Probar con un vendor antes de escalar
