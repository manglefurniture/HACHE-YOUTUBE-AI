# Piloto 2085 — paquete de preproducción (borrador)

**Estado:** propuesta para revisión humana, no aprobación editorial final.  
**Fuente rectora:** [CHANNEL-VISION.md](CHANNEL-VISION.md).  
**Título de trabajo:** Año 2085: El último trabajador humano.  
**Formato:** documental de ficción especulativa de 8–12 minutos; primera prueba audiovisual de 60–90 segundos y comparación visual de una escena de ~30 segundos en dos estilos.  
**Objetivo:** validar historia, coherencia visual, voz, montaje y costos antes de alquilar GPU.

## Logline
En 2085, cuando casi todo trabajo necesario es ejecutado por sistemas automáticos, una antigua técnica de mantenimiento descubre que la sociedad ha dejado de preguntarse quién decide qué vale la pena hacer.

## Tratamiento narrativo — propuesta original
1. **Gancho (0:00–0:45).** Ciudad al amanecer, infraestructura funcionando sin operadores visibles. Una persona guarda su antigua credencial. Voz: «La última fábrica no cerró. Simplemente dejó de necesitar trabajadores».
2. **Base científica (0:45–2:15).** Automatización e IA contemporáneas, límites y tareas todavía dependientes de personas. Investigar y citar fuentes actuales antes de redactar afirmaciones verificables.
3. **Puente de hipótesis (2:15–3:15).** Supuestos explícitos: robótica generalizada, energía suficiente, nuevas instituciones distributivas. Mostrar incertidumbres económicas y técnicas; no afirmar que ocurrirán en 2085.
4. **Historia humana (3:15–6:45).** Mara, ex técnica de mantenimiento, recibe la oportunidad de resolver un fallo que las máquinas podrían reparar. Su conflicto no es competir por salario sino decidir si intervenir tiene sentido.
5. **Dilema (6:45–9:15).** La red propone una solución eficiente que elimina una tradición comunitaria. Mara y sus vecinos debaten quién tiene autoridad para definir bienestar.
6. **Desenlace (9:15–10:30).** La comunidad decide mantener un espacio para decisiones humanas, incluso imperfectas. Pregunta final: «Si ya no necesitamos trabajar para vivir, ¿para qué queremos dedicar nuestra vida?».

Las duraciones son objetivos de escritura, no tiempos de audio medidos. Personajes, sociedad y año son ficción original.

## Prueba inicial: secuencia de 75 segundos
| ID | Tiempo orientativo | Imagen | Audio | Tipo |
|---|---|---|---|---|
| S01 | 0–12 s | Plano general de metrópolis sobria al amanecer; transporte y mantenimiento autónomos | Ambiente urbano, narración de apertura | Ficción |
| S02 | 12–25 s | Interior de centro industrial sin operarios; brazos robóticos tras cristal | Narración sobre el mundo imaginado | Ficción |
| S03 | 25–40 s | Primer plano de credencial gastada en manos de Mara; rostro sin exageraciones | Silencio breve y frase del personaje | Ficción |
| S04 | 40–55 s | Diagrama editorial sencillo: capacidad técnica frente a decisiones sociales | Explicación del supuesto, con rótulo «Hipótesis» | Hipótesis |
| S05 | 55–75 s | Mara ante una plaza donde vecinos conversan mientras la ciudad funciona | Pregunta abierta, cierre musical | Ficción |

**Control:** las escenas S01–S05 son una propuesta creativa, no renders existentes.

## Biblia visual provisional
- **Largos:** cinematografía realista, arquitectura funcional y físicamente plausible, iluminación natural, paleta contenida por escena, lentes y escala consistentes.
- **Shorts:** explorar animación estilizada por separado, sin asumir un modelo ganador.
- **Personaje Mara:** adulta de aproximadamente 50 años, cabello oscuro corto con canas, ropa utilitaria sin insignias, expresividad contenida. Crear hoja de personaje antes de generación; no basarse en personas reales.
- **Evitar:** ciudades de neón genéricas, interfaces ilegibles dominantes, manos deformadas, multitudes inconsistentes, logotipos de terceros y dramatización apocalíptica.
- **Marca:** nombre público, logo, paleta final, tipografía, voz y música pendientes de aprobación. No fijarlos en el render.

## Prompts de prueba (en inglés; candidatos, no validados)
**S01 realista:** `Wide cinematic establishing shot of a plausible coastal megacity in 2085 at sunrise, autonomous electric transit, maintenance robots in the distance, restrained functional architecture, believable materials, natural atmospheric haze, grounded science-fiction documentary aesthetic, coherent scale, no logos, no text, 16:9.`

**S01 animada:** `Stylized 2D animated establishing shot of the same plausible coastal city in 2085 at sunrise, functional architecture, autonomous transit, restrained palette, clean silhouettes, clear depth and scale, thoughtful speculative-science documentary mood, no logos, no text, 16:9.`

**S03 realista:** `Cinematic close-up of an older female maintenance technician's hands holding a worn blank access card, practical clothing, soft window daylight, subtle wear and tactile detail, emotionally restrained, photorealistic, no readable text, no logos, 16:9.`

**Negativos comunes:** `watermark, logos, legible interface text, oversaturated neon, distorted hands, extra fingers, impossible geometry, plastic skin`.

## Contrato mínimo de datos para futura automatización
Cada escena debe registrar: `scene_id`, `duration_target_s`, `narration_text`, `visual_prompt`, `negative_prompt`, `aspect_ratio`, `style_variant`, `asset_path`, `source_status` (fact/hypothesis/fiction), `review_status` y `render_metadata` (modelo, versión, semilla, tiempo, GPU, costo). No guardar secretos ni material privado de Lucía.

## Trabajo sin GPU y puertas de validación
1. Investigar y citar fuentes verificables para la sección científica; separar hechos de extrapolaciones.
2. Aprobar tratamiento y guion antes de generar escenas definitivas.
3. Crear storyboard con placeholders y narración temporal; medir duración real.
4. Probar montaje local con FFmpeg y assets sintéticos; validar MP4, audio, subtítulos y reanudación de tareas.
5. Revisar Docker y manifiesto de modelos por hashes, licencias, VRAM y compatibilidad; sin asumir que construir imagen equivale a ejecutarla.
6. Estimar GPU y presupuesto máximo **antes** de rentar; realizar solo una prueba corta y registrar resultados.
7. Comparar 30 segundos realistas frente a animados, calidad, consistencia y costo; revisión humana obligatoria.

## Criterios de aceptación antes de alquilar
- Guion piloto revisado; al menos una escena desglosada con prompts, referencias y duración.
- Fuentes y afirmaciones científicas verificadas, sin predicciones presentadas como hechos.
- Video de prueba ensamblado con placeholders, sin GPU, reproducible y con subtítulos.
- Lista de modelos, licencias, VRAM, pesos, almacenamiento y comandos de arranque verificados.
- Límite de gasto autorizado y plan de apagado/recuperación de artefactos.
- Sin publicación en YouTube, alquiler de GPU ni cambios en VPS hasta nueva decisión.
