# Proyecto 5 — Post-close Reporting Integration

**Estado:** Por empezar
**Timeline:** Semanas 11–14 (si da el tiempo)
**Proof of work:** #5

---

## Problema

El reporte post-cierre se genera manualmente:
- Compilación de datos de múltiples fuentes
- Formateo y revisión repetitiva
- Sin trigger automático — depende de que alguien lo inicie
- Difícil de delegar o replicar exactamente

## Solución objetivo

Trigger automático que genera el reporte post-cierre:
- Se activa al cierre del período (trigger manual o automático)
- Extrae datos relevantes de las fuentes definidas
- Genera reporte con formato estándar
- Entrega por mail o Slack al equipo

## Herramientas (a definir según madurez del stack en ese momento)

- Trigger: Make, script, o botón manual
- Fuentes: NetSuite, Google Sheets, Bill.com
- Output: PDF generado o Google Doc formateado

## Impacto esperado

- Eliminar tiempo de compilación manual
- Estandarizar formato del reporte
- Reducir errores por omisión
- Proceso replicable por cualquier persona del equipo

## Insight clave (para posts)

El reporte no cambia mucho — lo que cambia es quién lo tiene que armar.
Automatizar el reporte no fue sobre código: fue sobre dejar de ser el único que sabía hacerlo.

## Contenido planificado (fase 4)

- Post de cierre de roadmap: "5 procesos de AP que automaticé en 4 meses"
- Puede ser el post de "llegué" si coincide con conseguir rol nuevo

## Pendientes

- [ ] Definir alcance según tiempo disponible en semanas 11–14
- [ ] Mapear fuentes de datos del reporte actual
- [ ] Definir formato del output
- [ ] Armar MVP — trigger + extracción básica
