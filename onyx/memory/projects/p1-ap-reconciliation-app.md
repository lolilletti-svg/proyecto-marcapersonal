# Proyecto 1 — AP Reconciliation App

**Estado:** Completado — en GitHub, pendiente documentación y demo
**GitHub:** https://github.com/lolilletti-svg/ap-reconciliation-app
**Timeline:** Semanas 1–2 (pulir y documentar)
**Proof of work:** #1 — ancla de toda la narrativa

---

## Problema

Proceso de reconciliación de vendors 100% manual:
- Múltiples tabs de Excel apiladas
- VLOOKUPs que se rompían
- Statements en PDF que se convertían a mano
- Facturas que no matcheaban porque el número estaba escrito distinto en cada sistema
- Proceso dependía completamente de que Lucía no se equivocara — sin trazabilidad, sin backup

## Solución

App construida desde cero con Claude API + JavaScript + HTML:
- Parsea statements de vendors (PDF o Excel)
- Cruza contra Bill.com y NetSuite
- Consolida múltiples ubicaciones
- Normaliza números de factura (formatos distintos entre sistemas)
- Exporta resultado consolidado

## Herramientas

- Claude API
- JavaScript / HTML
- Excel (input/output)
- Bill.com (sistema fuente)
- NetSuite (sistema fuente)

## Impacto

- Eliminó matching manual entre múltiples fuentes
- Redujo significativamente tiempo dedicado a la tarea
- Agregó trazabilidad y lógica transferible
- Proceso que antes dependía de una persona ahora es reproducible

## Insight clave (para posts)

"Cuando tenés que explicarle un proceso a una IA con suficiente precisión como para
que lo construya — primero tenés que entenderlo vos."

El proceso de automatizar forzó entender el proceso en profundidad antes de tocarlo.

## Contenido generado / planificado

- Post #1: "Nadie me pidió que mejorara este proceso. Lo hice igual." — LISTO
- Post #4: "Así funciona mi app de reconciliación" — demo con imagen/video corto (semana 2)
- Post técnico sobre normalización de números de factura (opcional, fase 2)

## Pendientes

- [ ] Documentar código con comentarios
- [ ] Grabar demo de 2–3 minutos
- [x] Subir a GitHub — https://github.com/lolilletti-svg/ap-reconciliation-app
- [ ] Captura de pantalla del output para post visual
