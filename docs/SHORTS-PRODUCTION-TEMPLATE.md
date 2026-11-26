# Plantilla reutilizable de producción de Shorts
Aplicar [estándar editorial](SHORTS-EDITORIAL-STANDARD.md) antes de comenzar. Los primeros episodios validan montajes CPU con voz Axel, gráficos, subtítulos y cierre oficial. Consultar [catálogo y reglas vigentes](SHORTS-PRODUCTION-STATUS-2026-11-26.md); no demuestran automatización completa.

## Manifiesto por episodio
ID, título, tema aprobado, versión de guion, hechos/hipótesis/ficción, fuente y fecha para cada afirmación, riesgos y límites, licencia de cada recurso, voz/modelo/ID de generación aprobada, audio original y SHA-256, subtítulos SRT, storyboard CSV, prompts por plano, referencias y hashes, costes, aprobaciones humanas y estado. Guardar binarios en almacenamiento privado; GitHub solo texto y scripts.

## Orden operativo
1. Investigación y argumento; comprobar las fuentes antes de generar guion.
2. Guion original, narración aprobada, respaldo y transcripción con marcas.
3. CSV por plano: plano,inicio_s,fin_s,contenido,tecnica,estado. Intervalos contiguos desde cero, duración positiva y corte ligado a audio real.
4. Imágenes individuales 9:16; revisar identidad, continuidad y claridad. Planos científicos auténticos licenciados o gráficos originales comprobados; rotular recreaciones.
5. Generar animatic CPU con FFmpeg (H.264, proxy 720×1280, fps según montaje, SRT/ASS, cámara y gráficos por capas). Inter Bold lógico 54 px a 720×1280 / 81 px a 1080×1920, calibrar ASS y revisar en móvil. Integrar voz Axel aprobada sin regenerar toma. Incorporar cierre oficial Órbita de conocimiento, 2,6 s, desde recurso verificado. Reservar planos críticos para revisión.
6. Animación de actuación/stop motion: probar un plano aislado, resolución y continuidad; si degrada nitidez o deforma caras, conservar CPU aprobado. Solo después, alquilar GPU autorizada si procede; probar Wan vertical con una imagen, validar dimensiones/VRAM y duración; animar únicamente planos seleccionados. No inferir rendimiento de la prueba horizontal.
7. Ensamblar audio, clips, gráficos, música autorizada y subtítulos; exportar objetivo 1080×1920. Medir duración y verificar decodificación completa, audio presente, LUFS y picos, subtítulos, continuidad, portada, licencia y atribución. No imponer fps distintos al montaje aprobado. No publicar sin aprobación.
8. Respaldar originales, versiones y exportación con hashes en biblioteca/laptop/R2 según acceso, nunca credenciales ni binarios grandes en GitHub.

## Estado de cada puerta
pendiente → preparado → revisado → aprobado; una etapa no aprueba automáticamente la siguiente. Registrar bloqueo real. No realizar compras, alquileres o publicaciones no autorizadas. Mantener la fuente de verdad en GitHub. No guardar información privada ni URLs firmadas.
