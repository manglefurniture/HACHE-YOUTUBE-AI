# EP01 · Casting y audios de personajes — V1

**Estado:** voces elegidas y **diálogos generados**, pendientes de revisión y aprobación auditiva del usuario.  
**Proyecto:** HACHE-YOUTUBE-AI, episodio «¿Dejarías entrar un robot en tu casa?».  
**Fuente del texto:** [Guion EP01 V1](EP01-ROBOTS-HOGAR-GUION-V1.md).  
**Modelo:** ElevenLabs `eleven_v4`; un único audio generado por línea, respetando el texto literal del guion. Etiquetas de entonación, no diálogos nuevos.  
**Flow:** [EP01 · Diálogos de Inés, Vera y Luma](https://elevenlabs.io/app/flows/MldLhswym4j8nchkw4iv), ID `MldLhswym4j8nchkw4iv`. Se trata de un flujo nuevo y separado del audio aprobado de Axel.

## Casting propuesto y generado

| Personaje | Caracterización | Voz ElevenLabs y ID | Número de pistas |
| --- | --- | --- | ---: |
| **Inés, 58** | Mujer mexicana madura; voz cálida y con carácter, diferenciada del narrador. | **Gabriela — Spanish from Mexico Professional Voice** `hHjbwzYZW17oh0p05AKv` | 6 |
| **Vera, 29** | Joven mexicana; tono cercano y conversacional. | **Ana María — Calm & natural neutral Spanish** `m7yTemJqdIqrcNleANfX` | 5 |
| **Luma, robot** | Sereno y preciso, sin caricatura ni voz amenazadora; neutralidad conseguida por interpretación del texto, no por distorsión artificial. | **Isabel — Neutral Latino Pacefully Voice** `rixsIpPlTphvsJd2mI03` | 4 |

Los identificadores de voz se verificaron en `creative_list_voices`. **Esta selección no se considera aprobada por el usuario hasta que escuche las pistas nuevas**. Axel sigue aprobado e intacto.

## Manifiesto completo de las 15 intervenciones

| Nº | Escena | Personaje | Duración | Generation ID | Node ID |
| ---: | --- | --- | ---: | --- | --- |
| 01 | E01-S01 | LUMA | 4.88 s | `TzDrjyzuHxYLXXaz8HZe` | `Kp800Fl7v0NDlGjovz8q` |
| 02 | E01-S01 | INÉS | 2.88 s | `NTi7gVDwrHyc37T0UzqX` | `oLWVMstQUwJj94GujjBB` |
| 03 | E01-S05 | VERA | 3.68 s | `ezhCP7lfJIzbkiLjdfns` | `2uehLep76h6WjDMIy7Hv` |
| 04 | E01-S05 | INÉS | 1.92 s | `pcnm3KlTk3LrzGNFIWjL` | `oAMhIazge614pd9G6tYM` |
| 05 | E01-S05 | LUMA | 1.84 s | `vXRPQtVdTpcMU9MmbOU9` | `fC22dmbFAnTZ7mQ9pVFO` |
| 06 | E01-S06 | LUMA | 6.72 s | `v54i95GLyanWYuVYWeYv` | `WgqkSoZrRcXEDL8e7aaW` |
| 07 | E01-S06 | INÉS | 3.20 s | `J5pD38nad9wNIOhMgVR7` | `AxQly0qNp0xl7d1N0OcB` |
| 08 | E01-S06 | VERA | 4.88 s | `T9xppIL1f7kJhUVX3zFS` | `BO9DqvDDWzNhBwwqDVbj` |
| 09 | E01-S06 | INÉS | 4.80 s | `OtSwjEvHDIgLc8VAL6N6` | `wbSfuDhdSZ7GcYIR3UkM` |
| 10 | E01-S06 | VERA | 4.72 s | `pnIz23sMyrAR1ctmPZVB` | `C5MZR8J8nlaiiGUS8aHO` |
| 11 | E01-S06 | INÉS | 5.12 s | `zZRhgq6SzE2aQCMVPv7w` | `aTHF0PjVnlWl8vBNSUxi` |
| 12 | E01-S06 | VERA | 4.40 s | `V4nQAzqVzq8ZM5NsB1cX` | `XcECnxIj93qZhi9ZJj3V` |
| 13 | E01-S07 | LUMA | 3.68 s | `tW7nq0MhdrYmUmjdY5E6` | `yNxX0SirvdmfddiNiD3V` |
| 14 | E01-S07 | INÉS | 2.00 s | `6x2OWns07DSqm2qp08PU` | `OhnPHx114m2GtZiv7Sg2` |
| 15 | E01-S07 | VERA | 1.68 s | `keVNvWAxxTkfdLENe2LV` | `OvIahxHpu52M9DmA0LZX` |
| | **TOTAL** | **15 pistas** | **56.40 s** | **15 generaciones completadas** | |

**Verificación ElevenLabs:** `all_completed=true`, `has_failures=false`; todas las generaciones tienen `status=completed` y duración informada por el proveedor. Las líneas se generaron en el orden del guion, pero deben intercalarse con Axel en montaje, no concatenarse consecutivamente.

## Texto de cada línea (orden de montaje)

- **01 · E01-S01 · LUMA:** Esta tarea requiere asistencia humana remota. ¿Desea autorizar una sesión?
- **02 · E01-S01 · INÉS:** ¿Asistencia de quién? ¿Y qué puede ver?
- **03 · E01-S05 · VERA:** No tienes que demostrar que puedes hacerlo todo sola, mamá.
- **04 · E01-S05 · INÉS:** ¿Dónde dejaste mis lentes?
- **05 · E01-S05 · LUMA:** En la repisa de la entrada.
- **06 · E01-S06 · LUMA:** No puedo doblar esta pieza con seguridad. Hay una sesión de asistencia disponible. Esperando autorización.
- **07 · E01-S06 · INÉS:** Vera, ¿qué significa asistencia remota?
- **08 · E01-S06 · VERA:** Que un operador puede ayudarlo cuando se equivoca. Yo lo habilité para que aprendiera.
- **09 · E01-S06 · INÉS:** ¿Y puede ver la cocina? ¿Las fotografías? ¿La puerta de mi habitación?
- **10 · E01-S06 · VERA:** No sé exactamente qué muestra. Pensé que solo era una ayuda técnica.
- **11 · E01-S06 · INÉS:** Si alguien va a mirar desde afuera, quiero saber cuándo, por qué y hasta dónde.
- **12 · E01-S06 · VERA:** Tienes razón. Lo acepté yo, pero aquí vivimos las dos.
- **13 · E01-S07 · LUMA:** Sesión no autorizada. Puedo intentar otra tarea.
- **14 · E01-S07 · INÉS:** La toalla la doblo yo.
- **15 · E01-S07 · VERA:** Entonces te ayudo.

## Duración y restricciones de montaje

- Narrador Axel V1, aprobado anteriormente: **338.40 s** según [manifiesto aprobado](EP01-AXEL-NARRACION-APROBADA-2026-11-23.md).
- **Diálogos en prueba:** **56.40 s**.
- **Audio verbal sumado de ambos:** **394.80 s = 6:34.80**; todavía faltan silencios, transiciones, ambiente, música y montaje, y no corresponde inflar el tiempo con silencios vacíos para alcanzar una duración orientativa de 8–9 minutos.
- Los tiempos de escena del storyboard son objetivos previos, **no marcas reales de sincronización**. Crear EDL/timeline real una vez aprobadas las voces de personajes.
- Estas generaciones están en ElevenLabs, **sin respaldo local ni R2 verificado**. Los `generation_id` son referencias duraderas; las URL temporales de descarga no.
- No se volvió a generar ninguna pista de Axel. No se publicaron audios o videos ni se modificó el VPS.

**Próximo paso:** usuario escucha los diálogos, señala ajustes si son necesarios y aprueba/corrige personajes. Solo entonces se marcan las voces y diálogos como referencia final de producción; después respaldar archivos y comenzar el primer montaje.
