Ejecutar el protocolo completo de cierre de sesión para el proyecto marca personal.

Ejecutar los siguientes pasos en orden. No omitir ninguno aunque la sesión haya sido corta.

---

## STEP 1 — Actualizar memoria del sistema

Archivos en `/Users/luciacamilletti/.claude/projects/-Users-luciacamilletti-Documents-claude-code-proyecto-marcapersonal/memory/`

- Leer `project_marca_personal.md` y actualizarlo con el estado actual, decisiones tomadas y próximos pasos de esta sesión
- Si hubo cambios en Zernio, Notion, bots u otras integraciones: actualizar o crear el archivo `project_` correspondiente
- Si hubo feedback nuevo sobre cómo trabajar (estilo, preferencias, correcciones): actualizar o crear el archivo `feedback_` correspondiente
- Si se aprendió algo nuevo sobre el perfil o goals de Lucía: actualizar `user_profile.md`
- Si se registró una referencia nueva (DB Notion, endpoint, herramienta): actualizar o crear el archivo `reference_` correspondiente
- Actualizar `MEMORY.md` si se crearon archivos nuevos (agregar línea al índice)

---

## STEP 2 — Agregar entrada en bitácora

Archivo: `onyx/memory/logs/bitacora-sesiones.md`

Agregar al tope (antes de la entrada más reciente) una nueva entrada con este formato:

```
## Sesión [FECHA] — [Título breve de lo hecho]

**Qué se hizo:**
[Lista numerada, concreto y específico — no genérico]

**Estado al cerrar:**
[Estado de cada cosa relevante con ✅ / ⏳ / ❌]

**Próximos pasos:**
[Lista numerada, accionable]

---
```

---

## STEP 3 — Actualizar checkpoint

Archivo: `.cloudcode/state/checkpoint.md`

Actualizar el archivo completo con el estado actual de la sesión. Mantener la estructura existente:
- `## 🎯 Objetivo actual`
- `## 🧠 Contexto funcional`
- `## ✅ Decisiones tomadas`
- `## 📊 Análisis y estrategia`
- `## 📁 Archivos y rutas clave`
- `## ⚠️ Riesgos y dudas abiertas`
- `## ➡️ Próximos pasos exactos`
- `## 🔁 Instrucción de rehidratación`

Actualizar el campo `last_updated` en el frontmatter con la fecha y hora actual.

---

## STEP 4 — Actualizar README.md

Archivo: `README.md` en la raíz del proyecto.

- Si no existe: crearlo
- Si existe: actualizar con cualquier cambio relevante de esta sesión (integraciones nuevas, comandos nuevos, estado de proyectos, herramientas)

---

## STEP 5 — Git commit y push

Ejecutar en orden:

```bash
git add -A
git commit -m "Session [FECHA]: [resumen breve de lo hecho en la sesión]"
git push origin main
```

Si el push falla por falta de remote o credenciales: avisar a Lucía con los comandos exactos para resolverlo.

---

## REGLAS

- Ejecutar los 5 pasos siempre, sin preguntar si hacerlo
- No omitir pasos aunque la sesión haya sido breve
- Si no hay nada nuevo en algún archivo, igual registrar en bitácora que se revisó
- El commit message debe ser descriptivo pero conciso — máximo 1 línea de resumen
- Confirmar al final: "✓ Protocolo de cierre completado — [resumen de 1 línea de lo guardado]"
