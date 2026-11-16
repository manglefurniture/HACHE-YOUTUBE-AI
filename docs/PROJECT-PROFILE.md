# HACHE-YOUTUBE-AI — perfil inicial

- Objetivo: producción supervisada de documentales en español sobre misterios, historia y curiosidades.
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
- Etapa: prototipo técnico, sin publicación automática ni GPU contratada.
- Pendiente: permisos granulares, tokens de corta duración, multipart para archivos grandes, CI, aprobación humana.
