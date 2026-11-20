# GPU compartida: Lucía → HACHE-YOUTUBE-AI

## Estado y límites

La imagen derivada se construye mediante `.github/workflows/gpu-image.yml`. La auditoría de Clore #2458580 está en el PR #10 (borrador); una imagen publicada **no implica** que ComfyUI, los modelos o Wan funcionen en GPU.

Fuente de verdad del bootstrap original: [lucia-gpu/bootstrap](https://github.com/manglefurniture/lucia-gpu/tree/main/bootstrap). Su script original requiere **activos privados de Lucía** y no debe ejecutarse sin cambios para YouTube.

## Reutilización permitida

- ComfyUI, dependencias y nodos compatibles.
- Juggernaut XL Ragnarok (SDXL) y Wan 2.2 I2V (High/Low Noise), con sus encoder/VAE.
- Montaje de modelos compartidos en almacenamiento de GPU, idealmente como volumen de solo lectura cuando sea viable.

## Separación obligatoria

- No montar ni copiar `lucia_lora_ragnarok_v2.safetensors`, `lucia_ref_01.png`, datasets, workflows privados ni credenciales de Lucía.
- Usar `/workspace/hache-youtube/` para entradas, salidas y workflows del canal, separados de `/workspace/lucia/`.
- No publicar la API de ComfyUI en Internet sin autenticación y control de acceso; mantenerla local o mediante túnel seguro.
- No incluir secretos de Cloudflare R2 en Dockerfile, imagen, logs o GitHub; usar credenciales efímeras y limitadas.
- El arranque comprueba primero ComfyUI, el mount, una GPU NVIDIA y el espacio libre; después descarga solo las nueve keys públicas incluidas en `gpu/model-inventory.json` a `/workspace/models`, transmite en bloques, reintenta y verifica tamaño/SHA-256 antes de renombrar el archivo. Se necesitan al menos unos 46 GiB libres para el conjunto completo. R2 requiere credenciales de lectura de mínimo privilegio (`R2_ACCOUNT_ID`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`) montadas en runtime; el script las elimina del entorno antes de lanzar ComfyUI.
- Si un archivo local ya coincide con el inventario, se conserva sin descargar duplicados; un archivo parcial nunca se considera listo. El healthcheck requiere que la API local de ComfyUI responda.
- No descargar modelos pesados, construir imágenes remotas ni contratar GPU sin confirmar costos y disponibilidad.

## Inspección segura de un contenedor existente

Dentro de una GPU autorizada que **ya esté en ejecución**, sin modificarla:

```bash
python3 gpu/verify-shared-models.py --models-dir /workspace/models
python3 gpu/verify-shared-models.py --models-dir /workspace/models --hash
```

El primer comando verifica presencia; el segundo verifica SHA-256. Ambos son de solo lectura. El verificador utiliza hashes de modelos públicos referenciados por el bootstrap original y **no** exige archivos privados de Lucía. Un resultado correcto no demuestra por sí solo que Wan pueda generar video: faltan validar GPU/VRAM, nodos, workflow y ejecución.

## Almacenamiento híbrido (comprobado el 19-11-2026)

- VPS `/srv/lucia-models`: volumen de 14 GB, ~12 GB usados y ~2.2 GB libres; contiene Juggernaut XL, IP-Adapter/CLIP y activos privados de Lucía. **No es un endpoint público ni un volumen montado automáticamente en Clore**. No modificar, borrar ni copiar privados a YouTube.
- R2 privado `hache-ai-models`: cuatro archivos Wan I2V/UMT5/VAE (35.58 GB) verificados por SHA-256 desde GitHub Actions. Están en `shared/wan22/<run-uuid>/<filename>`; no asumir una ruta plana.
- GPU: montar el volumen en `/workspace/models`; el arranque aprovisiona la allowlist pública de nueve modelos desde las keys exactas de R2 y los coloca en las carpetas ComfyUI (`checkpoints`, `clip_vision`, `diffusion_models`, `ipadapter`, `loras`, `text_encoders`, `ultralytics`, `vae`). La ruta remota del VPS no se usa.
- `HACHE_MODELS_DIR` permite personalizar el mount. El arranque falla claramente si ComfyUI, el mount, una GPU NVIDIA o el espacio libre requerido faltan. El healthcheck comprueba la API local de ComfyUI; no demuestra que un workflow de inferencia funcione.

## Próxima fase

1. Recuperar el nombre, tag/digest y Dockerfile o configuración de la imagen usada en Clore.
2. Verificar arquitectura, VRAM, ComfyUI, modelos y licencias aplicables.
3. Crear Dockerfile/derivación versionada en este repo, sin modificar el de Lucía.
4. Añadir workflows originales de escenas para el piloto y una prueba controlada de imagen y video.
5. Conectar resultados al R2 privado existente y medir costo por escena.

El runtime no incluye `buffalo_l`, modelos ni datos privados de Lucía. No se ha desplegado ni contratado ninguna GPU en esta fase.
