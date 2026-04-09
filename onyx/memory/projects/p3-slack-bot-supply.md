# Proyecto 3 — Slack Bot para Supply (Monday Workflow)

**Estado:** Por empezar
**Timeline:** Semanas 5–9
**Proof of work:** #3

---

## Problema

Equipo de Supply comunica necesidades de forma desestructurada:
- Sin formato estándar
- Información faltante que requiere ir y venir
- Sin resumen consolidado para el inicio de semana
- Coordinación reactiva y difícil de escalar

## Solución objetivo

Slack bot con modal de intake estructurado:
- Formulario en Slack con campos definidos (tipo de solicitud, proveedor, monto estimado, urgencia, etc.)
- Respuestas guardadas en Google Sheets o Airtable como backend
- Resumen automático los lunes con todas las solicitudes de la semana anterior

## Herramientas (a definir)

- Slack API (Bolt for Python o JS, o Make + Slack integration)
- Google Sheets o Airtable (backend)
- Trigger de lunes para resumen automático

## Impacto esperado

- Eliminar solicitudes incompletas o ambiguas
- Tener registro estructurado de pedidos de Supply
- Resumen automático que reemplaza reunión de status o mails de lunes

## Insight clave (para posts)

Diseñar los campos del formulario fue el trabajo real.
No fue un problema técnico — fue entender qué información mínima necesitás
para que una solicitud sea procesable sin ir a buscar más datos.

## Contenido planificado (fase 2)

- Post: "Los campos que decidí pedir en mi Slack bot y por qué"
- Post técnico: "Así diseñé el intake estructurado para mi equipo de Supply"
- Post de v2: mejoras después de uso real

## Pendientes

- [ ] Listar campos necesarios para una solicitud procesable
- [ ] Definir herramienta: Make + Slack vs Bolt
- [ ] Armar MVP del modal
- [ ] Conectar a Sheet/Airtable
- [ ] Configurar resumen automático de lunes
