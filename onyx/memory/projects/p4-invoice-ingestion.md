# Proyecto 4 — Invoice Ingestion automática

**Estado:** Por empezar
**Timeline:** Semanas 8–12
**Proof of work:** #4

---

## Problema

Facturas de vendors llegan por mail (Imperial, US Foods, Cisco y otros):
- Procesamiento manual: abrir mail, descargar adjunto, cargar en sistema
- Formatos distintos por vendor
- Sin consolidación automática
- Riesgo de omisión o doble carga

## Solución objetivo

Pipeline automático de ingesta de facturas:
- Parseo de mails entrantes de vendors específicos
- Extracción de datos clave de PDF o Excel adjunto
- Consolidación automática en Google Sheets centralizado
- Validación básica (monto, número de factura, vendor)

## Herramientas (a definir)

- Email parsing (Make, Zapier, o script con IMAP)
- PDF → Sheet (Claude API para extracción, o parser específico)
- Google Sheets (destino)
- APIs de Bill.com / NetSuite (integración futura)

## Impacto esperado

- Eliminar carga manual de facturas
- Reducir errores de transcripción
- Crear pipeline replicable para nuevos vendors
- Base para automatización de aprobación (fase futura)

## Insight clave (para posts)

Cada vendor tiene su propio formato — el trabajo no fue técnico, fue de estandarización.
Entender qué varía entre vendors y qué es constante es el 80% del problema.

## Contenido planificado (fase 3)

- Post: "Cómo diseño un sistema antes de automatizarlo"
- Mini case study: "3 procesos de AP que automaticé este trimestre" (incluye P4)
- Post con imagen: arquitectura del flujo de ingesta

## Pendientes

- [ ] Mapear vendors prioritarios (Imperial, US Foods, Cisco)
- [ ] Documentar formato de cada uno (PDF? Excel? campos clave)
- [ ] Elegir herramienta de parseo de mail
- [ ] Armar MVP para un vendor antes de escalar
- [ ] Definir esquema del Sheet de destino
