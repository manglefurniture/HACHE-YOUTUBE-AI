# HACHE-YOUTUBE-AI — perfil inicial

- Objetivo vigente: producción supervisada en español sobre ciencia, tecnología y futuros posibles; marca Crónicas del Mañana, lanzamiento Shorts-first experimental. Ver [estado de lanzamiento](CHANNEL-LAUNCH-2026-11-24.md).
- Usuarios: operador/editor autorizado; audiencia final en YouTube.
- Zona horaria: America/Cancun.
- SEO_MODE: none (el panel interno no se indexa).
- Superficie: API privada; no hay panel público.
- Roles iniciales: operador con acceso de lectura/escritura; acceso anónimo denegado.
- Datos: guiones, fuentes, imágenes, clips, narraciones, renders, estado de trabajos.
- Almacenamiento: R2 privado `hache-ai-youtube-media` (sin exponer r2.dev).
- Infraestructura: Workers para transferencia pequeña; GPU externa para generación; no usar VPS productivo.
- Riesgos: filtración de secretos, archivos públicos, costos, interrupciones Spot, material sin licencia.
- Hache-Base: adoptar seguridad, pruebas, separación de secretos y trazabilidad; no clonar módulos PHP ni multisede.
- Etapa: canal creado, pruebas técnicas de GPU externa realizadas; migración de instancia en curso según última captura del 24/11. Sin publicación automática; estado operativo del destino pendiente de validar.
- Pendiente: permisos granulares, tokens de corta duración, multipart para archivos grandes, CI, aprobación humana.
