# Año 2085 — referencias GPU: ciudad y plaza central (22/11/2026)

**Estado:** ciudad **aprobada como referencia visual**; plaza **provisional, pendiente de validación creativa**. Son **imágenes generadas realmente en ComfyUI con una RTX 5090 de Clore**, no imágenes creadas con ChatGPT. No son fotogramas finales ni validan consistencia entre distintas tomas.

## 1. Activos y ubicación

Bucket **privado**: `hache-ai-youtube-media` (dominio `r2.dev` deshabilitado). Los dos objetos se confirmaron después de subirlos mediante Cloudflare; no hay enlaces públicos.

| Activo | Estado | Clave R2 | Bytes | SHA-256 del archivo local |
| --- | --- | --- | ---: | --- |
| Ciudad V3 | Referencia aprobada por el usuario | `refs/2085/ciudad_v3_ref.png` | 1,473,747 | `471966b3ec158fb56ab324421318327dfee614228bb555a2a6357d6cd7b2100f` |
| Plaza F | Provisional, no aprobada aún | `refs/2085/plaza_central_ref_provisional.png` | 1,231,617 | `b6b4b4273cb5e99d0962f6b07cf1ab8a5c74c09fbd994cf8814e6c0d7a5cb259` |

**Archivos de trabajo adicionales:** `C:\Users\hache\Documents\HACHE-YOUTUBE-AI\assets\2085\references\` en la laptop Hache. Allí también están los candidatos A–F, historiales de ComfyUI y un `manifest.json`; el Escritorio contiene copias de las dos referencias seleccionadas. Las copias locales no forman parte de GitHub: **los PNG originales están en R2, y GitHub conserva sus identificadores, hashes y workflows**.

## 2. Workflow reproducible en GitHub

| Imagen | Archivo de workflow API | Seed | Steps | CFG | Denoise |
| --- | --- | ---: | ---: | ---: | ---: |
| Ciudad V3 | [`gpu/workflows/2085/ciudad_v3_api.json`](../gpu/workflows/2085/ciudad_v3_api.json) | `20852029` | 30 | 7.2 | 1.00 |
| Plaza F | [`gpu/workflows/2085/plaza_central_provisional_api.json`](../gpu/workflows/2085/plaza_central_provisional_api.json) | `20853016` | 32 | 7.4 | 0.82 |

Ambos: `juggernautXL_ragnarok.safetensors` (Juggernaut XL Ragnarok), **1344 × 768**, `dpmpp_2m`, `karras`, 1 imagen por ejecución, ComfyUI **0.46.0** en **RTX 5090 32 GB**. Prompts positivos, negativos y conexiones se conservaron íntegros en los JSON (formato **API prompt**, no exportación visual del lienzo).

**Dependencia importante:** el workflow de plaza F utiliza **img2img**, cargando la imagen `ciudad_v3_ref.png` mediante `LoadImage` + `VAEEncode`. Para repetirlo en una GPU nueva, descargar esa referencia del bucket privado y subirla primero al directorio `input` de ComfyUI con ese nombre; también aprovisionar y verificar Juggernaut XL. El workflow de ciudad es `txt2img` y no tiene esa dependencia.

## 3. Comparación visual — qué se validó

**Similitudes logradas:** lenguaje de arquitectura blanca curva, torres esbeltas y nervadas, vegetación urbana, luz ámbar rasante, colores naturales, textura fotográfica. La plaza F tiene una mesa y varias personas en torno al ajedrez. Reutilizar la ciudad como imagen de partida contribuyó a esta coherencia visual.

**Diferencias pendientes:** la plaza F todavía parece un patio moderno más que un espacio público antiguo, y el árbol central de gran copa no ocupa un papel suficientemente prominente. El pavimento y los bancos aún carecen de suficiente desgaste/reparaciones; no hay demostración de identidad de Mara ni Leo. Las candidatas A/B/C/D fallaron en uno u otro extremo (plaza contemporánea genérica o contexto histórico ajeno al 2085); E mantuvo la arquitectura pero casi no incluyó ajedrez.

**Decisión de producción:** usar **ciudad V3 como ancla aprobada**, y **plaza F solo como base para la siguiente iteración**, nunca como escena definitivamente aprobada. No generar un video final de la plaza hasta resolver continuidad espacial y conseguir aprobación humana.

## 4. Próximos pasos y límites

1. Generar una nueva versión de plaza a partir de F que destaque el árbol viejo, las mesas de ajedrez y el pavimento usado, manteniendo las torres/edificios de V3; fijar una vista maestra y variantes día/audiencia/atardecer.
2. Recuperar las referencias originales aprobadas de Mara y Leo, sin inventar caras ni usar activos privados de Lucía.
3. Registrar calidad, seed, tiempo y VRAM de una prueba de movimiento; **Wan 2.2 sigue sin estar probado en generación de video**.
4. Si la GPU alquilada deja de utilizarse, detener el alquiler para no prolongar el costo.

Referencias: [Biblia visual](PILOT-2085-VISUAL-BIBLE-V1.md), [Estado anterior del piloto](PILOT-2085-VISUAL-TEST-STATUS.md), [Runbook real de Clore/R2](CLORE-RTX5090-R2-RUNBOOK-2026-11-22.md). La información verificable de las imágenes está en el [manifiesto](../gpu/workflows/2085/references_manifest.json).
