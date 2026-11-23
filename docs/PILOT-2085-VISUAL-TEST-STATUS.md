# Estado de pruebas visuales — 2085

## Actualización — 22/11/2026: iteración de plaza V2A–V2E

**Cinco imágenes reales más generadas en RTX 5090**, en ComfyUI con Juggernaut XL. Se probaron img2img (V2A/B) y edición selectiva con máscaras (V2C/D/E). La ciudad V3 continúa aprobada; **ninguna plaza V2 está aprobada**. V2E conserva la ciudad y el árbol, pero aún parece terraza, sin copa antigua suficientemente amplia. Se respaldaron las cinco imágenes, las máscaras y una comparativa en el bucket privado de medios R2; tamaños/ETag MD5 cotejados con archivos locales. Guía y hashes: [Resultados de Plaza V2](PILOT-2085-PLAZA-V2-GPU-RESULTS.md), [Manifiesto](workflows/2085/plaza_v2_results_manifest.json).

---

## Actualización — 22/11/2026: GPU real y referencias respaldadas

La RTX 5090 de Clore ejecutó ComfyUI y Juggernaut XL con éxito. Se generó y aprobó como **referencia** una ciudad 2085 (V3) y se creó una plaza central mediante **img2img** a partir de esa ciudad (versión F, todavía **provisional**). Ambas imágenes están respaldadas como PNG en el bucket **privado** `hache-ai-youtube-media`; workflows, parámetros, SHA-256 locales y claves R2 están documentados en [Pruebas visuales de GPU: ciudad y plaza](PILOT-2085-GPU-VISUAL-REFERENCES-2026-11-22.md). La plaza todavía necesita un árbol central reconocible y materiales envejecidos; no existe prueba de video Wan ni escena final aprobada.

**Nota:** el siguiente registro de 18/11 se conserva como fotografía histórica del estado de aquella fecha; la frase final "Sin GPU alquilada" no describe la actualización anterior.

---


**Fecha:** 2026-11-18. **Estado:** referencias individuales y animática preliminar creadas en conversación, pendientes de incorporación al repositorio y validación técnica de video generativo.

## Imágenes maestras preliminares
- `mara.png`: retrato de Mara en taller.
- `leo.png`: retrato de Leo en plaza.
- `ciudad.png`: panorama costero con transporte autónomo.
- `plaza.png`: plaza comunitaria con ajedrez.

Las imágenes se entregaron como archivos descargables en la conversación, **no están versionadas todavía en GitHub**. La identidad visual general fue aprobada previamente; estas nuevas tomas individuales aún requieren revisión de consistencia con la lámina inicial.

## Montaje de prueba
- `2085_preview_20s.mp4`: 20 segundos, 960×540, 25 fps, cuatro imágenes con zoom lento, sin audio.
- Es **animática con imágenes fijas**, no video generativo ni animación de personajes.
- La secuencia incluye ciudad, plaza, Mara y Leo; **no** es todavía la escena S01 definitiva.

## Pendientes para video real
1. Verificar acceso y costo de proveedor/modelo de video antes de cualquier generación facturable.
2. Probar movimiento de tren y actividad de plaza usando referencias; controlar identidad y deformaciones.
3. Medir costo por segundo, tiempos de render y continuidad.
4. Añadir locución Axel solo tras confirmar sincronía y aprobación del material.
5. Incorporar activos finales a GitHub con ruta y procedencia documentadas, sin subir binarios enormes sin estrategia de almacenamiento.

**Sin GPU alquilada, sin publicación y sin despliegue.**
