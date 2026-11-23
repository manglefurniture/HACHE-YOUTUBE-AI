# Año 2085 — Plaza V3, prueba peatonal (22/11/2026)

**Estado creativo: NO HAY PLAZA APROBADA.** Ciudad V3 continúa siendo la referencia visual; Plaza V2E sigue siendo la mejor base provisional. Esta iteración corrigió parcialmente el nivel de cámara, pero **no** logró simultáneamente perspectiva de plaza pública + futurismo.

## Resultados reales

| Prueba | Tecnología | Resultado | Decisión |
| --- | --- | --- | --- |
| V3G | RTX 5090, Juggernaut XL, img2img de V2E (denoise 0.83) | Plaza pública a nivel de suelo, ajedrez y personas; **edificios clásicos y torre de reloj, sin skyline futurista** | Rechazada |
| V3H | RTX 5090, Juggernaut XL, txt2img 1344 × 768 | Buen árbol robusto y pavimento de plaza; **calle/plaza clásica actual, no 2085** | Rechazada |
| V3I | Inpaint de 60.27 % de V2E, protegiendo parte del skyline y reconstruyendo suelo/árbol | Prompt `50d1ae10-6e40-4282-965e-bbb812443a5d` aceptado; **el túnel SSH se perdió durante la ejecución** y no hubo imagen recuperada | Resultado desconocido |
| V3J | Segunda variación de inpaint (CFG 8) | **No fue enviada** porque el runner terminó tras desconexión | Pendiente |

No interpretar la pérdida de túnel como fallo probado de GPU ni como confirmación de que la instancia haya quedado detenida. La conexión privada `127.0.0.1:18188` dejó de escuchar; diagnóstico remoto en curso.

## Activos locales y trazabilidad

- Laptop Hache: `C:\Users\hache\Documents\HACHE-YOUTUBE-AI\assets\2085\references\plaza_v3g_candidate.png` y `plaza_v3h_candidate.png`.
- V3G: 1,560,696 bytes; SHA-256 `34cd2e1d8f97003ab5b1f2d0fe2b0199e551bdc603be42db41df3e49eb8bf9af`.
- V3H: 1,824,630 bytes; SHA-256 `e65862fa9235813287272d6f2d0ccf887b0e00c4c70a1bce83ecbee97c77a51b`.
- Máscara I/J: `plaza_v3ij_ground_mask.png`; SHA-256 `294e2eda61a96282831599ed27378d8c5a212a771e5a7ff2a384e42389643ad7`; cobertura media 60.27 %.
- Los workflows y runners de V3G/H/I/J se encuentran en `docs/workflows/2085/` y `scripts/`; detalles en [manifiesto V3](workflows/2085/plaza_v3_results_manifest.json).
- **No se ha verificado respaldo R2 de los nuevos G/H**; no inventar claves ni ETags. Imágenes no añadidas al repositorio.

## Siguiente acción recomendada

1. Comprobar el estado del alquiler Spot en Clore y el puerto SSH asignado antes de intentar reconexión o nuevos cargos.
2. Si continúa activa la RTX 5090, reabrir el túnel privado, consultar `/history/50d1ae10-6e40-4282-965e-bbb812443a5d` antes de reenviar V3I. Descargar el resultado existente si ya terminó.
3. Ejecutar V3J solo si V3I merece una segunda semilla; no repetir las pruebas G/H sin cambiar la estrategia.
4. Hacer revisión visual humana, respaldo R2 privado con verificación y registrar hashes. **No iniciar aún video Wan de la plaza.**
5. Detener Spot desde My Orders al terminar, para evitar más cargos. No se ha confirmado detención del alquiler.

No se modificó el VPS ni se desplegó a producción; no se tocaron activos privados de Lucía.
