# Lote A S04–S08 — checkpoint de voz y sincronización

Fecha operativa: 26/11/2026 (Cancún). El PR #51 consolidó los guiones V2, registro visual y preparación en main (fa577205c2deb06c22aca6daf568c089f099dc5c). La autorización del usuario permitió generar una sola toma por episodio. No se publicaron videos ni se alquilaron GPUs.

## Voz original y respaldo
Flow privado: https://elevenlabs.io/app/flows/owVZBmIWRqZTp4I6maLd. Axel (U7je2I3DMxe8ZOLb6vmd), eleven_v4. El proveedor confirmó cinco generaciones completadas. Los MP3 se respaldaron en la laptop Hache, Documentos/Crónicas del Mañana/Robótica - Lote A S04-S08, con los siguientes hashes, verificados nuevamente durante el preflight:

| ID | Generación voz | Duración s | Bytes | SHA-256 |
|---|---|---:|---:|---|
| S04 | 87iKryh09hZ57SVANYW7 | 36.16 | 596878 | 6b6934350598994cdd5a50e03c733de484a0e9cfc2644fdf843eadce02912af2 |
| S05 | vhAlz4I5VMXogAoaVoGH | 42.40 | 696770 | 8632ec0704c9e8c1d4f0a8344b036acdf1d438a27831737e262a268ac25ac5a0 |
| S06 | PlWfGbF273uXpPJRTm21 | 40.64 | 668349 | e04abcba9551e83d29b4cb15bcd7dffeafa26b7f65e6ad6e7cebb0866afbc654 |
| S07 | BMRE3EKafXo0KlAZ71BY | 43.28 | 710563 | fe2a510d4cff5dd56ce387009531f65792482191f3c50ad34d08d7e7b5ad1d44 |
| S08 | twYsF5wa4DZQHbJfDZGz | 40.64 | 668349 | 53986987337446dcdccf6095a7565f5ed702cb0afb188315bac1c816bd13011f |

Coste de voz reportado por proveedor: 3662.4776 créditos, equivalente 68 centavos USD según sus resultados de generación. No se compraron créditos. Cinco transcripciones Scribe con coste estimado de 0 créditos, completadas; no hay precio final separado informado. Sin consultas nuevas vidIQ.

## Sincronización real
Transcripción y texto de origen coinciden después de normalizar espacios en cada caso. Los datos por palabra, IDs y audio permanecen en los directorios privados S04–S08, archivo alignment-input.json. Las marcas de Scribe excedieron en 0.08 s la duración de audio reportada por proveedor; el límite de última palabra se recortó a esa duración, dentro de tolerancia documentada de 0.12 s. El constructor comprueba SHA-256, texto, tiempos y anclajes; no inventa marcas.

| Episodio | Scribe ID | Subtítulos | Planos incluyendo cierre | Objetivo de duración con cierre s |
|---|---|---:|---:|---:|
| S04 | SdzWV6cCCOiFZjjANsjR | 16 | 13 | 38.76 |
| S05 | 1EzDLtmuStMraTkDfUth | 17 | 12 | 45.00 |
| S06 | 2LbSkAJi26y0UfgTaWO9 | 18 | 13 | 43.24 |
| S07 | oE73AQHcKrJIuYPCL9CK | 17 | 14 | 45.88 |
| S08 | dAlHNWWoN3Y1Qc2VPC9z | 16 | 15 | 43.24 |

Resultados de timing-v2: 84 cues, 67 planos (incluidos 5 cierres), 0 advertencias de duración/lectura según validación heurística; 6 pruebas unitarias locales aprobadas. El archivo final SRT usa puntuación exacta del guion, máximo dos líneas y 27 caracteres por línea como preflight, no como medición de ancho tipográfico. La revisión visual móvil y audio final siguen pendientes. Los 5 planos largos de V1 se subdividieron con anclajes de voz reales. Se conserva V1 en el respaldo, sin sobrescribir.

## Reproducción
`python scripts/build_shorts_timing.py alignment-input.json --shots production/series/humanoid-robots-batch-a-shots.json --audio ORIGINAL.mp3 --output timing-v2`
Usar directorio de salida nuevo para cambios. Genera subtitulos.srt, storyboard.csv, timing-report.json. Los resultados no prueban el montaje ni certifican licencias. El cierre oficial aún requiere comprobación binaria. La duración final será la medida al renderizar, no se añade relleno para alcanzar 50 s.

## Puertas siguientes
Generar fichas de referencia e imágenes maestras; comparar con material de S01–S03 y EP01 antes de escenas, incluyendo personajes secundarios; la laptop solo mostró carpetas S01 y S02 y no se corroboró el respaldo persistente S03. Mantener cada historia independiente. Verificar tipografía y cierre, música/licencias, QA y aprobación de publicación. No usar esta etapa como autorización de GPU ni publicación.
