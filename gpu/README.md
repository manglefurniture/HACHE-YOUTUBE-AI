# GPU compartida: Lucía → HACHE-YOUTUBE-AI

## Estado y límites

Este directorio prepara la **adaptación**, no afirma que exista una imagen Docker publicada o validada para YouTube. La imagen exacta utilizada en Clore.ai aún debe identificarse en el registro o la configuración de la instancia; no se debe inventar un nombre/tag ni iniciar alquileres para averiguarlo.

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
- No descargar modelos pesados, construir imágenes remotas ni contratar GPU sin confirmar costos y disponibilidad.

## Inspección segura de un contenedor existente

Dentro de una GPU autorizada que **ya esté en ejecución**, sin modificarla:

```bash
python3 gpu/verify-shared-models.py --models-dir /workspace/ComfyUI/models
python3 gpu/verify-shared-models.py --models-dir /workspace/ComfyUI/models --hash
```

El primer comando verifica presencia; el segundo verifica SHA-256. Ambos son de solo lectura. El verificador utiliza hashes de modelos públicos referenciados por el bootstrap original y **no** exige archivos privados de Lucía. Un resultado correcto no demuestra por sí solo que Wan pueda generar video: faltan validar GPU/VRAM, nodos, workflow y ejecución.

## Próxima fase

1. Recuperar el nombre, tag/digest y Dockerfile o configuración de la imagen usada en Clore.
2. Verificar arquitectura, VRAM, ComfyUI, modelos y licencias aplicables.
3. Crear Dockerfile/derivación versionada en este repo, sin modificar el de Lucía.
4. Añadir workflows originales de escenas para el piloto y una prueba controlada de imagen y video.
5. Conectar resultados al R2 privado existente y medir costo por escena.

No se ha desplegado ni contratado ninguna GPU en esta fase.
