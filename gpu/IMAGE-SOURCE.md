# Imagen base confirmada

Imagen de origen proporcionada por el propietario y confirmada mediante consulta **de solo lectura** al manifiesto remoto:

```text
ghcr.io/manglefurniture/lucia-gpu:clore-55b19cce89ee3eb3d3b0ee92010d52136e09ef70
```

El manifiesto remoto responde con esquema Docker v2 y config digest `sha256:6f6afd229d954f76e81f5cb77db3cec4559f0e704fecf826034b70fcdcbc280f`. **Ese digest corresponde a la configuración, no al manifiesto**, y no debe usarse como digest para `FROM`.

La imagen derivada se define en `gpu/Dockerfile`; reemplaza el ENTRYPOINT de Lucía por un arranque aislado de YouTube y no incorpora archivos privados de Lucía. Es una adaptación mínima, no una validación de generación de imágenes/video.

## Antes de construir o publicar

- Revisar el Dockerfile y los metadatos de la imagen base, su arquitectura y sus licencias.
- Resolver y fijar el digest del manifiesto remoto para builds reproducibles.
- Inspeccionar los modelos presentes y ejecutar `verify-shared-models.py`.
- Validar aislamiento de archivos, usuarios y acceso a API ComfyUI.
- Ejecutar un trabajo real de imagen y luego video en una GPU autorizada.
- Publicar una imagen nueva bajo el nombre del proyecto **solo tras validación**.

No se modificó la imagen original, la construcción/publicación se realiza únicamente mediante el workflow de GitHub Actions al fusionar los cambios en main; antes del merge no se realizó build/push, no se alquiló GPU ni se desplegó.

## Construcción y publicación automatizadas

El workflow `.github/workflows/gpu-image.yml` construye en PR **sin publicar** y publica en GHCR solamente desde `main` con `GITHUB_TOKEN` y permiso `packages:write`. Genera etiquetas `sha-<commit>` y `latest`. Si GHCR rechaza el acceso a la imagen base o la publicación del paquete, habrá que ajustar la visibilidad/permisos del paquete, sin ampliar privilegios automáticamente.

El entrypoint original `/usr/local/bin/start.sh` de Lucía requiere su LoRA, referencia y workflow privados, por lo que **se reemplaza** por `gpu/start-youtube.sh`. Este arranque escucha únicamente en `127.0.0.1:8188` y separa entradas/salidas en `/workspace/hache-youtube`. Los modelos se montan en `/workspace/models`; no se descargan durante la construcción. No conectar el puerto públicamente sin una capa autenticada.

La imagen base no copia los activos privados en su Dockerfile original; no obstante, no se ha auditado exhaustivamente el contenido de sus capas ni realizado una prueba de inferencia con GPU.
