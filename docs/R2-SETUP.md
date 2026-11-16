# R2 — integración privada (prototipo)

Bucket: `hache-ai-youtube-media`. No cambiar `hache-ai-models`.

## Seguridad
- Bucket privado, sin dominio r2.dev ni dominio público.
- Configurar `SIGNING_SECRET` como secreto del Worker, nunca en GitHub ni en wrangler.
- Los tokens HMAC-SHA256 caducan en un máximo de 3600 segundos y restringen prefijo y métodos. Ver `docs/SECURITY.md`.
- No proporcionar SIGNING_SECRET a una GPU Spot: solo tokens emitidos por un entorno de confianza.
- PUT limitado a 20 MiB reales. Videos grandes necesitan multipart directo con firma temporal.

## Verificación pendiente
1. Crear SIGNING_SECRET fuera de GitHub y configurar un emisor confiable.
2. Ejecutar CI y revisar resultados y comentarios automáticos.
3. Merge solo con checks y revisión satisfactorios.
4. Desplegar y probar 401 sin token, PUT/GET con token limitado y expiración.
5. Verificar privacidad del bucket y ausencia de exposición pública.

No se ha realizado una transferencia real ni despliegue desde este PR.
