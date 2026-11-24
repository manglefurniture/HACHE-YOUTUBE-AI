# EP01 · Referencias visuales maestras — 23/11/2026

**Episodio:** «¿Dejarías entrar un robot en tu casa?»  
**Estado:** referencias iniciales generadas y respaldadas; selección creativa provisional. No son activos finales publicables ni se incluyen binarios en GitHub.

## Alcance completado

Se generaron en la RTX 4090 de Vast.ai referencias maestras para establecer la dirección visual de EP01:

| Activo | Archivo original | Resultado de revisión |
| --- | --- | --- |
| Inés | `EP01_MASTER_INES_00001_.png` | Utilizable como referencia inicial: mujer madura, cocina, paleta y textura coherentes. |
| Vera | `EP01_MASTER_VERA_00001_.png` | Utilizable como referencia inicial: personaje visualmente distinguible de Inés. |
| Cocina | `EP01_MASTER_KITCHEN_00001_.png` | Utilizable como layout de ambiente: gabinetes verde azulado, acentos naranja, ventana/cortinas y puerta posterior. |
| Luma (primera prueba) | `EP01_MASTER_LUMA_00001_.png` | Rechazada como referencia definitiva: aspecto humanoide/femenino demasiado marcado. |
| Luma V2 | `EP01_MASTER_LUMA2_00001_.png` | Rechazada: la generación introdujo dos robots y no es apta para continuidad. |
| Luma V3 | `EP01_MASTER_LUMA3_00001_.png` | Mejor candidato provisional; reduce el aspecto femenino, pero aún necesita una nueva iteración antes de fijarlo como diseño final. |

## Dirección visual usada

- Ilustración editorial retrofuturista adulta de revistas de ciencia ficción de los años 50–60.
- Gouache/tinta, textura de semitono discreta, base crema, verde azulado y naranja óxido.
- Luz matinal cálida y tecnología funcional; sin cyberpunk, fotorrealismo ni texto generado.
- Resolución: 1024 × 576 (16:9).
- Modelo: `juggernautXL_ragnarok.safetensors`.
- Muestreo: 28 pasos, CFG 6.5, `dpmpp_2m`, scheduler `karras`.

## Semillas y reproducibilidad

| Activo | Semilla |
| --- | ---: |
| Inés | 20852032 |
| Vera | 20852033 |
| Cocina | 20852034 |
| Luma V2 | 20852035 |
| Luma V3 | 20852036 |

El manifiesto de la primera tanda conserva prompt, negativo, grafo, semillas y prompt IDs. Los binarios y el manifiesto completo no se versionan en GitHub.

## Respaldo comprobado

Paquete guardado en la laptop Hache:

`C:\Users\hache\Pictures\HacheYouTube\EP01_ROBOTS_HOGAR\Referencias_maestras\EP01_MASTER_PACKAGE.zip`

Contiene Inés, Vera, cocina, Luma V3, manifiesto y hoja de revisión.  
Tamaño: 3,755,852 bytes.  
SHA-256: `417B42CB25D801EFB4FBF2CCFA230A9C8BF9E61F17006CE3B205D1BCCA013C9E`.

## Límites y próximo paso

1. No animar a Luma como personaje final hasta corregir su silueta para eliminar la apariencia humanoide residual.
2. Mantener Inés, Vera y el layout de cocina como referencias provisionales, no como frames finales de montaje.
3. Una vez aprobado Luma, generar una imagen maestra conjunta que fije los tres personajes dentro de la cocina y luego producir clips Wan de 2–5 segundos.
4. No se subieron medios pesados, credenciales, modelos ni material de Lucía a GitHub.
