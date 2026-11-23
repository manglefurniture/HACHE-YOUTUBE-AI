# Clore: ComfyUI preinstalado con inicio por etapas

**Estado:** alternativa preparada para una siguiente prueba; **no validada en GPU real**. No inicia alquiler, despliegue ni transferencia. La imagen anterior `ghcr.io/manglefurniture/hache-youtube-ai-gpu` permanece como respaldo, sin cambios.

## Plantilla comprobada en documentación

- **Imagen propuesta:** `yanwk/comfyui-boot:cu130-slim`, recomendada en la [guía de ComfyUI de Clore](https://docs.clore.ai/guides/image-generation/comfyui).
- **Origen/mounts:** [YanWenKun/ComfyUI-Docker: cu130-slim](https://github.com/YanWenKun/ComfyUI-Docker/blob/main/cu130-slim/README.adoc). Directorio modelo del contenedor: `/root/ComfyUI/models`.
- **Alternativa por compatibilidad de controlador:** `yanwk/comfyui-boot:cu126-slim` (CUDA 12.6). No elegirla automáticamente: primero verificar GPU/driver y el tag realmente disponible en Clore.
- **Imagen de tercero:** no es nuestra imagen ni una garantía de compatibilidad con Wan, custom nodes o VRAM. No asumir tamaño de descarga, seguridad, nodos ni éxito sin inspección real. Registrar nombre/tag y digest del contenedor al probarlo.

## Fase A: arranque limpio, SIN R2

1. Antes de pagar, seleccionar un servidor con GPU NVIDIA, memoria adecuada para SDXL, suficiente disco y red. Registrar GPU, VRAM, driver, almacenamiento y precio. Definir presupuesto y punto de corte. La [guía de Clore](https://docs.clore.ai/guides/image-generation/comfyui) orienta 8 GiB de VRAM mínimo SDXL y 12 GiB+ recomendado; la inferencia con este checkpoint aún está por verificar.
2. En Clore, elegir la plantilla `yanwk/comfyui-boot:cu130-slim`. Configurar `CLI_ARGS=--listen 127.0.0.1` para comprobación por SSH. **No publicar 8188 mediante `http_pub` sin autenticación**: ComfyUI no está protegido por nuestro Worker. Permitir solo SSH durante esta prueba; acceso a la UI únicamente mediante túnel autenticado. Ajustar el puerto según las opciones reales del proveedor.
3. Conservar almacenamiento persistente según la configuración real de Clore (no asumir que sobrevivirá a una cancelación). **No poner credenciales R2 en las variables de la instancia durante la fase A**.
4. Una vez desplegada la plantilla, entrar por SSH y comprobar:

```bash
nvidia-smi -L
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
df -h /root /root/ComfyUI/models
python3 - <<'PY'
import json
import urllib.request
url = "http://127.0.0.1:8188/system_stats"
with urllib.request.urlopen(url, timeout=5) as response:
    data = json.load(response)
print("COMFYUI_OK", list(data.keys()))
PY
```

**Puerta de salida A:** GPU visible, ComfyUI responde localmente y no hay fallos de arranque. Si falla, diagnosticar el host antes de descargar modelos; detener la prueba si el gasto previsto se supera. Un HTTP 200 no demuestra inferencia ni que los modelos abran.

## Fase B: SOLO Juggernaut XL desde el bucket privado

Se activa **manualmente después de aprobar A**. Descarga `checkpoints/juggernautXL_ragnarok.safetensors` de la allowlist versionada (7,105,350,162 bytes, aproximadamente 6.62 GiB); no descarga Wan, FaceID, LoRA, datos privados de Lucía ni los otros ocho modelos. Se necesita espacio adicional para descarga temporal (~8.2 GB libres como mínimo técnico; reservar holgura de almacenamiento para salidas).

La descarga reutiliza `gpu/provision_models.py`, que comprueba tamaño y SHA-256 en streaming y hace reemplazo atómico. El comportamiento **sin `--only` sigue siendo el original: nueve modelos**.

```bash
# Dentro de la instancia de ComfyUI, DESPUÉS de verificar fase A:
git clone --depth 1 --branch main https://github.com/manglefurniture/HACHE-YOUTUBE-AI.git /root/hache-youtube-ai
cd /root/hache-youtube-ai
git rev-parse HEAD

# Un entorno aislado para boto3; no cambiar Python ni dependencias de ComfyUI:
python3 -m venv /root/.cache/hache-youtube-r2-venv
/root/.cache/hache-youtube-r2-venv/bin/pip install --disable-pip-version-check boto3==1.35.99

# Revisar disco del mount antes de transferir:
df -h /root/ComfyUI/models

# Introducir credenciales de R2 solo en la sesión SSH (no pegarlas aquí, en logs ni en Git):
read -r -p "R2 account ID: " R2_ACCOUNT_ID
read -r -s -p "R2 read-only access key ID: " AWS_ACCESS_KEY_ID; echo
read -r -s -p "R2 read-only secret: " AWS_SECRET_ACCESS_KEY; echo
export R2_ACCOUNT_ID AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY

/root/.cache/hache-youtube-r2-venv/bin/python gpu/provision_models.py \
  --models-dir /root/ComfyUI/models --only juggernaut
unset R2_ACCOUNT_ID AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY

# Validar únicamente el checkpoint, con SHA-256; NO exige otros ocho modelos:
python3 gpu/verify-shared-models.py \
  --models-dir /root/ComfyUI/models --only juggernaut --hash
```

**Puerta de salida B:** `MODEL_VERIFIED` o `MODEL_READY` y verificador `ok` para `checkpoints/juggernautXL_ragnarok.safetensors`. Si no aparece, no lanzar un workflow de inferencia.

Si falla el primer intento, **no reinstalar ComfyUI ni borrar modelos verificados**: revisar conexión a R2, credenciales de lectura, montaje del volumen, espacio y logs. El script borra el `.part` incompleto y puede reintentarse.

## Fase C: prueba de generación posterior (fuera del alcance de esta preparación)

Usar un workflow **SDXL básico con nodos estándar** para generar una imagen de prueba, con parámetros y consumo registrados; después preparar personajes de «Año 2085» usando la biblia visual aprobada. Verificar que el checkpoint aparece en la interfaz, se carga para inferencia, que la salida se guarda y que la GPU no se agota. **Presencia y SHA-256 no prueban que el modelo se pueda cargar ni generar**.

Wan 2.2, sus nodos y compatibilidad de VRAM requieren otra validación. No aprovisionar los nueve modelos como condición de arranque para esta prueba de SDXL.

## Seguridad, operación y límites

- Nunca colocar tokens/emisor, secretos de Lucía, fotos ni LoRA privados en un servidor alquilado. **Usar exclusivamente claves R2 de solo lectura y prefijo permitido**, con duración/acceso mínimo. Las credenciales temporales de la sesión deben limpiarse y rotarse si se sospecha exposición.
- Evitar publicar el puerto 8188 sin capa de autenticación; el Worker actual de medios no autentica automáticamente la UI ComfyUI.
- El proveedor de la imagen podría modificar tags: comparar digest y drivers antes de usarla. Una plantilla ajena sigue necesitando inspección de seguridad.
- La ruta de salida y volumen son **distintos de la imagen Docker anterior**. No reutilizar a ciegas `/workspace/models` ni `/opt/ComfyUI`.
- GitHub Actions verifica el script y las pruebas de selección, **no prueba arranque en GPU, calidad, generación ni costes**.
- Al finalizar una futura prueba, conservar únicamente resultados autorizados y detener la instancia de Clore para evitar cargos.

## Reversión

Esta ruta es solo documentación y soporte de selección/verificación; no modifica `gpu/Dockerfile`, `gpu/start-youtube.sh`, el workflow de publicación ni modelos almacenados en R2. Para volver al método anterior, usar la imagen GHCR del repositorio: `gpu/provision_models.py` y `gpu/verify-shared-models.py` mantienen `--only all` como valor predeterminado.
