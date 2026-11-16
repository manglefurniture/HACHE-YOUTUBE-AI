# GPU → R2: transferencia con credenciales limitadas

El controlador confiable (por ejemplo, laptop Hache) posee `HACHE_ISSUER_SECRET`. La GPU alquilada **nunca** recibe este secreto ni `SIGNING_SECRET`; solo recibe un token HMAC con prefijo, métodos y caducidad.

## Controlador

Desde `worker/`, establecer `HACHE_ISSUER_SECRET` localmente, y ejecutar:

```sh
node scripts/issue-gpu-token.mjs jobs/job-001/ PUT 300 gpu-token.txt
```

El archivo de token se crea sin sobrescribir uno existente. Es una credencial temporal: mantenerlo fuera de Git y borrarlo después de usarlo. Entregar a la GPU solo este token por un canal privado. No registrar tokens en logs ni argumentos de comandos.

## GPU

```sh
HACHE_R2_TOKEN_FILE=/ruta/privada/gpu-token.txt node scripts/gpu-r2-transfer.mjs PUT jobs/job-001/segment-001.bin /ruta/segment-001.bin
```

Para descarga, emitir un token `GET` específico y usar `GET` con un archivo de destino inexistente.

## Limitaciones

- El Worker admite objetos de hasta **20 MiB**. No enviar videos grandes ni dividirlos sin definir primero ensamblado y validación.
- El token expira en 15 minutos como máximo; el controlador debe emitir uno nuevo por trabajo.
- No hay orquestador de GPU, cola de tareas, publicación en YouTube ni transferencia multipart implementados en este repositorio.
- Antes de producción: autorización granular del emisor, rate limiting, revocación y protección contra replay; aprovisionamiento seguro del token a la GPU y limpieza de archivos temporales.
