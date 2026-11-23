# Año 2085 — Plaza V2, resultados reales en RTX 5090 (22/11/2026)

**Estado creativo: no hay plaza aprobada.** Ciudad V3 sigue siendo la referencia aprobada. Se produjeron **cinco PNG reales** en **ComfyUI 0.46.0 / Juggernaut XL Ragnarok / RTX 5090 Clore** y se recuperaron desde la API privada vía túnel SSH en laptop Hache. Todos concluyeron `status_str=success` (1344×768); no se hizo video Wan ni despliegue a producción.

## Qué funcionó y qué falló

| Versión | Método | Resultado tras inspección visual | Decisión |
| --- | --- | --- | --- |
| V2A | Img2img desde Plaza F (0.77) | Buen pavimento antiguo y jugadores, pero parece plaza actual con automóviles, sin skyline 2085 | Rechazada |
| V2B | Img2img desde Plaza F (0.86) | Pavimento antiguo y copa de árbol, pero perdió por completo la identidad arquitectónica futurista; árbol prominente sin follaje | Rechazada |
| V2C | Inpaint selectivo sobre Ciudad V3 | Conservó **edificios y cielo** de Ciudad V3, produjo mesas de ajedrez y plaza usada; NO produjo el árbol grande | Base intermedia, no final |
| V2D | Inpaint de árbol sobre V2C | Aparece árbol, pero es demasiado pequeño, follaje brillante con apariencia de arbusto | Provisional, no aprobado |
| V2E | Inpaint de árbol sobre V2C | Conserva ciudad y árbol verde junto al ajedrez; copa demasiado compacta, mobiliario poco coherente y plaza parece terraza elevada | **Mejor base provisional**, NO aprobada |

**Siguiente ajuste**: mantener el skyline y el ajedrez de V2C/V2E, pero conseguir un **árbol antiguo de copa amplia, tronco robusto**, sombra coherente, pavimento viejo y plaza reconocible como espacio público histórico, no terraza corporativa. No es razonable llamar final a V2E ni iniciar aún el video de esta locación.

## Reproducibilidad

- A/B: entrada real `plaza_central_ref_provisional.png` de R2; workflows en `docs/workflows/2085/plaza_v2_a_api.json`, `plaza_v2_b_api.json`.
- C: entrada `ciudad_v3_ref.png`, máscara generada con `scripts/build_2085_plaza_mask.py`, workflow `plaza_v2_c_inpaint_api.json`.
- D/E: entrada es el **PNG EXACTO de salida V2C** cargado como `plaza_v2c_candidate.png` (también respaldado en R2); máscara de `scripts/build_2085_plaza_tree_mask.py`; workflows `plaza_v2_d_tree_api.json`, `plaza_v2_e_tree_api.json`.
- Parámetros, semillas, IDs de ejecución, hashes locales, ETag y claves R2 de las cinco versiones están en `docs/workflows/2085/plaza_v2_results_manifest.json`.
- Todos los objetos están en bucket privado **`hache-ai-youtube-media`**, bajo `refs/2085/candidates/` y `refs/2085/masks/`. No hay URLs públicas ni se incluyen PNG en GitHub.
- Verificación: la API de ComfyUI confirma éxito y dimensiones; Cloudflare lista objetos/tamaños; ETag MD5 de subida de un solo bloque coincide con el MD5 de cada archivo local. Los SHA-256 del manifiesto son de archivos locales; **no** se afirma verificación SHA-256 por lectura de R2 en esta etapa.

## Vista y archivos locales

- Laptop Hache: `C:\\Users\\hache\\Documents\\HACHE-YOUTUBE-AI\\assets\\2085\\references\\` (todos los originales y máscaras).
- Comparativa local: `comparativa_plaza_v2_gpu.jpg`, también en R2 `refs/2085/candidates/comparativa_plaza_v2_gpu.jpg`.
- Copias en Escritorio OneDrive de la laptop: `Comparativa_Plaza_2085_GPU_20261122.jpg` y `Plaza_2085_V2E_preliminar_20261122.png`.

## Seguridad y gasto

No se modificó el VPS de Hache Natación, no se tocaron activos privados de Lucía, no se publicaron enlaces R2 ni se expuso ComfyUI. Se usó el túnel local `127.0.0.1:18188`. El resultado no implica que Clore deje de cobrar; se debe detener la renta Spot desde My Orders al terminar. No se comprobó terminación del alquiler.
