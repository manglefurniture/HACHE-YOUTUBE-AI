# S01 — animatic CPU v2
25/11/2026 · America/Cancun. Complementa [checkpoint de sincronización](S01-TIMING-ASSET-BACKUP-2026-11-25.md). No autoriza publicación.

## Resultado verificado
- S01_montaje_provisional.mp4: H.264, 720×1280, 25 fps, 1315 frames, 52,60 s, 7.470.709 bytes. Render CPU con FFmpeg; 16 planos, zoom simple, subtítulos SRT incrustados y marca. Revisados fotogramas de los 16 planos y corregida la posición de subtítulos para no cubrir gráficos. No es versión final ni contiene audio ni Wan.
- El usuario confirmó que descargó el MP3 aprobado a su teléfono. No se pudo descargar al entorno por falta de resolución DNS; no se regeneró. No se probó el mux con audio real. El MP3 sigue en ElevenLabs y en teléfono según usuario.
- Nuevo respaldo privado en biblioteca ChatGPT: Cronicas del Manana/S01_preproduccion_v2.zip, 24.035.057 bytes, SHA-256 d7a24e863d7ad6aca617cb853eb3afc70e4bc23cf5d847f70168507a76a3a2c3. ZIP validado, 25 archivos, incluidos 16 composiciones 720×1280, vídeo, CSV, SRT, prompts Wan, manifiesto, scripts de preparación/montaje y borrador de publicación. No reemplaza originales del ZIP previo. Laptop/R2 no confirmados.
- P11: recorte de P10 para mantener vestuario. P15: previsualización ampliada (360×640 de origen), falta master. No presentar composiciones 720p como masters definitivos.
- P03/P04/P05/P06: gráficos originales; se excluyeron fotos sintéticas del chip y esquema previo inexacto. P04 conceptual, no fotografía ni escala exacta. Figura auténtica de terceros no recuperada/verificada para reutilización. P01/P02 rotulados recreación IA; P07 salto temporal; P08–P15 rotulados ficción especulativa.

## Ciencia comprobada
Holz et al., NEJM, publicación electrónica 20/10/2025, https://doi.org/10.1056/NEJMoa2501396. 38 implantados; 32 evaluados a 12 meses; 26/32 mejoraron agudeza visual de forma clínicamente significativa. No equivale a 26 curaciones ni a 26 pacientes que recuperaron lectura. PRIMA proyecta luz infrarroja cercana al implante subretinal fotovoltaico inalámbrico. Tamaño 2×2 mm y 378 píxeles según Palanker et al., https://pubmed.ncbi.nlm.nih.gov/32249038/. No se usaron imágenes de terceros. Historia 2045 ficticia.

## Mux pendiente, sin regenerar voz
Con FFmpeg, comprobar MP3 original 51,12 s y mantener duración 52,60 s:
```sh
ffmpeg -i S01_montaje_provisional.mp4 -i S01_Axel_aprobado.mp3 -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 160k -af apad -t 52.6 S01_con_voz.mp4
```
No se ha ejecutado este comando con el audio real. Revisar escucha y sincronización; no publicar automáticamente.

## Borrador de publicación
Título: ¿Podremos recuperar la vista? El implante PRIMA y el futuro de la visión.
Descripción: explicar resultados limitados del estudio, la historia ficticia de Elena, enlaces primarios y nota de recreaciones IA. Marcar contenido alterado/sintético por recreaciones clínicas realistas; revalidar políticas. Música ambiental instrumental discreta, no seleccionada ni licenciada; verificar derechos antes de utilizar.

Siguiente: recibir MP3 o incorporarlo al montaje; revisión con voz; terminar masters, P15 y continuidad de P11; confirmar derechos de figura si se quiere sustituir P04; Wan vertical y exportación 1080×1920 tras validación. No se contrató GPU ni se usó laptop o VPS.

## Actualización: animatic V3 con voz aprobada

El usuario adjuntó el MP3 descargado de Axel. Se conservó byte a byte como `S01_Axel_aprobado.mp3` (835951 bytes, SHA-256 `1637516b558e76bfe093ee0a5a886ea434b2dc7e0240fe7a829e2a9e768ecb22`). Duración PCM decodificada: 51,12 s; MP3 contenedor: 51,148 s. Las pausas son compatibles con las marcas Scribe previas. No se regeneró ni se cambió el ritmo de la voz.

Resultado: `S01_animatic_con_voz_v3.mp4`, 52,60 s, H.264 720×1280 a 25 fps, AAC mono 44,1 kHz, 8621364 bytes, SHA-256 `5af68c05ae9ef0a5d2da2068f405152bc0af613e176b06517f1d56d75510b963`. Decodificación completa FFmpeg sin errores. Vídeo original copiado sin recodificar; audio normalizado en el montaje desde -35,93 LUFS hasta -17,74 LUFS, pico verdadero final -1,95 dBTP. El original no se modificó; sin música ni efectos. Se añadió silencio al final hasta 52,60 s.

Respaldo confirmado de ambos archivos en biblioteca privada ChatGPT, carpeta Cronicas del Manana. No se verificó copia en laptop ni R2. No se utilizó GPU externa. No se publicó. La integración de voz queda resuelta; sigue pendiente la aprobación del montaje provisional, revisión de masters, música/efectos si procede, animaciones Wan y exportación final. La comprobación de pausas no sustituye la revisión audiovisual humana.
