# R2 — integración privada (prototipo)

Bucket: `hache-ai-youtube-media`. No cambiar `hache-ai-models`.

## Seguridad
- Bucket privado, sin dominio r2.dev ni dominio público.
- Configurar `API_TOKEN` como **Worker secret** en Cloudflare, nunca en GitHub ni en `wrangler.jsonc`.
- El token inicial es de prototipo: no entregar a GPU Spot ni a terceros. Antes de usar GPU externa, sustituir por URLs firmadas de corta duración y permisos por prefijo/operación.
- `/health` no revela información sensible; `/objects/<key>` requiere Bearer token.
- PUT limitado a 20 MiB. Videos grandes requieren multipart directo a R2 y credenciales limitadas.

## Verificación pendiente de despliegue
1. Crear secreto API_TOKEN fuera de GitHub.
2. Ejecutar pruebas del Worker localmente y revisar CI.
3. Desplegar únicamente tras aprobación de checks y merge.
4. Confirmar 401 sin token, 400 con clave inválida, PUT/GET privado con archivo pequeño.
5. Comprobar que r2.dev sigue deshabilitado.

No se ha realizado una prueba real de transferencia ni despliegue desde este PR.
