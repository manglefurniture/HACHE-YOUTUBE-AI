# Clore RTX 5090 + ComfyUI: rescate de arranque y preparación R2

**Fecha de validación:** 22 de noviembre de 2026 (Cancún), registros del contenedor 23 de noviembre UTC.  
**Proyecto:** HACHE-YOUTUBE-AI.  
**Resultado comprobado:** ComfyUI v0.46.0 responde HTTP 200 localmente y mediante túnel SSH privado desde la laptop Hache. **No se ha probado todavía ninguna generación de imagen ni descargado un checkpoint a la GPU.**  
**Alcance:** registro operativo para repetir la prueba sin volver a pagar por instalaciones fallidas. No cambia la imagen GHCR ni el entorno productivo.

## 1. Instancia real y decisiones

- Clore Spot, servidor **#119714**, GPU **RTX 5090 (32 GB)**, CPU Ryzen 9 9950X3D, RAM vista por ComfyUI ~64 GB, almacenamiento observado **651 GB libres** en el contenedor durante la prueba.
- Host anunciado con **98.04 %** de confiabilidad; precio **US$0.44/h** (la pantalla de órdenes mostraba ~US$11.12/día con cargos). Estos datos son históricos, **no garantía de una renta futura**.
- Imagen de terceros: `yanwk/comfyui-boot:cu130-slim-v2`. Sin digest registrado; verificar la imagen y sus cambios en futuras rentas.
- Clore con **SSH auto-install entrypoint** activado; autorización mediante clave pública guardada `clore-prl-hache`; puertos internos 22/TCP y 8188/HTTP.
- Sesión observada desde SSH con hostname `O-2478599`. Las capturas de la interfaz pueden mostrar un identificador de orden distinto; **tomar la orden vigente de My Orders como autoridad y comprobarla con `hostname`**.
- El servidor previo #78153 falló repetidamente con errores 502 y SSH sin respuesta; no inferir de ello un problema general de la imagen.

## 2. Diagnóstico y causa verificada

1. La nueva GPU permitió conectarse por SSH desde la laptop Hache usando la clave privada que corresponde a `clore-prl-hache`. La RTX 5090 aparecía con ~32 GB VRAM.
2. Clore informó `Deployed`, pero el servicio web no escuchaba en `127.0.0.1:8188`; error HTTP externo 502. El proceso de Clore como PID 1 era `order_entrypoin`, no el entrypoint original de la imagen.
3. El entrypoint original existe en `/runner-scripts/entrypoint.sh`. Copia un ComfyUI ya incluido en la imagen desde `/default-comfyui-bundle/ComfyUI` hasta `/root/ComfyUI`; ejecuta `python3.13 ./ComfyUI/main.py --listen --port 8188 ...`. Se observó que `/root/ComfyUI` no existía antes de ejecutarlo manualmente.
4. Al ejecutar el entrypoint original, ComfyUI y PyTorch cargaron, pero falló el bind: `OSError: could not bind on any address out of [('::', 8188, 0, 0)]`. La instancia no ofrecía `/proc/net/tcp6` ni `/proc/sys/net/ipv6/conf/all/disable_ipv6`; el intento efectivo fue sobre IPv6.
5. Se inició ComfyUI con `--listen 0.0.0.0 --port 8188` explícitos. Respuesta local confirmada: `HTTP/1.1 200 OK`, `Server: Python/3.13 aiohttp/3.14.3`, HTML con título `ComfyUI`. PyTorch `2.13.0+cu130` reconoció `cuda:0 NVIDIA GeForce RTX 5090`.
6. La URL pública de Clore continuó devolviendo `403` / `Proxy Not Found` (en pruebas previas 502). **No es prueba de que ComfyUI esté roto**: la respuesta local 200 lo distingue del problema del proxy.
7. Se estableció un túnel SSH privado en la laptop Hache hacia `127.0.0.1:8188`, disponible como `http://127.0.0.1:18188/`. Se verificó `HTTP 200` y título `ComfyUI`; el usuario confirmó que la interfaz abre.

**Interpretación:** el auto-entrypoint de Clore sustituyó u omitió el arranque normal de esta imagen. Además, el comando original acabó tratando de escuchar en IPv6, no disponible en el contenedor de prueba. El problema público del proxy es independiente. **No afirmar que un reinicio mantendrá el arranque manual.**

## 3. Recuperación repetible (solo entorno Clore autorizado)

Prerequisitos: alquiler activo, endpoint SSH copiado de `My Orders`, clave pública ya asociada a la cuenta, acceso a laptop Hache. Nunca pegar claves privadas en chat, GitHub ni logs.

**Desde PowerShell de Hache:**

    ssh -i "$HOME\.ssh\clore_prl_ed25519" -o IdentitiesOnly=yes -p <PUERTO_EXTERNO> root@<HOST_DE_My_Orders>

**En el contenedor Clore (inspección, no instalar nada aún):**

    hostname
    nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
    test -f /runner-scripts/entrypoint.sh && echo ENTRYPOINT_PRESENT
    test -f /default-comfyui-bundle/ComfyUI/main.py && echo BUNDLE_PRESENT
    df -h /root
    curl -sS --max-time 5 -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8188/

Si la respuesta no es 200, confirmar que no hay ComfyUI activo antes de iniciar otra instancia. El script `/runner-scripts/entrypoint.sh` copia el bundle, **pero en este host falló al enlazar IPv6**. La ruta probada, tras crear `/root/ComfyUI` con ese script, fue:

    cd /root
    python3.13 ./ComfyUI/main.py --listen 127.0.0.1 --port 8188 --enable-manager --enable-manager-legacy-ui

Para mantener una sesión desconectable, usar `nohup` con un archivo de log local temporal, pero **no lanzar simultáneamente dos servidores ComfyUI**. La prueba original usó `--listen 0.0.0.0` para verificar IPv4; **para nuevas sesiones preferir `127.0.0.1`** y túnel autenticado para no exponer una UI sin autenticación.

**Desde PowerShell de Hache, en otra consola:**

    ssh -N -T -L 127.0.0.1:18188:127.0.0.1:8188 -i "$HOME\.ssh\clore_prl_ed25519" -o IdentitiesOnly=yes -o ExitOnForwardFailure=yes -p <PUERTO_EXTERNO> root@<HOST_DE_My_Orders>

Abrir en **esa laptop** `http://127.0.0.1:18188/`. Validar `/system_stats` (respuesta JSON) por túnel, no solo la página inicial. El túnel deja de funcionar al cerrar su proceso o suspender la laptop. No publicarlo en redes externas.

**Seguridad/reinicio:** el arranque manual y los archivos locales de esta GPU Spot no están garantizados tras reset o cierre de alquiler. Esta recuperación NO es todavía un despliegue reproducible automatizado. Evitar URL web abierta de Clore para UI sin autenticación; revisar port forwarding si el proveedor vuelve a activar su proxy.

## 4. Preparación de imágenes desde R2 (avance verificado)

- Bucket privado confirmado mediante Cloudflare el 22/11/2026: `hache-ai-models`. No confundir con el bucket de medios `hache-ai-youtube-media`.
- Objeto para la primera prueba de imágenes **existente en R2**:
  - Key: `shared/comfyui-public/checkpoints/cd815a8f4b714eb5a8fa7f5a69faa46d/juggernautXL_ragnarok.safetensors`
  - Tamaño R2: **7,105,350,162 bytes** (~6.62 GiB). Inventario fijo: SHA-256 `dd08fa32f98d05a2443ca1419e46df1575a0811f6e3b246d9dd47ff20f5eb66a`. **La presencia/longitud del objeto sí fue consultada en R2; el hash es el valor registrado por el repositorio y debe verificarse al descargar.**
- Ruta de destino ComfyUI: `/root/ComfyUI/models/checkpoints/juggernautXL_ragnarok.safetensors`. No usar las rutas de la imagen GHCR propia (`/workspace/models`) sin `--models-dir`.
- El script versionado existente `gpu/provision_models.py` implementa descarga selectiva de `--only juggernaut`, bloques de 4 MiB, reintentos, chequeo de bytes y SHA-256, `.part` y renombrado atómico. Su modo predeterminado `--only all` trae **nueve archivos (~43.88 GiB)**: nunca invocarlo para la prueba de imagen.
- El verificador versionado `gpu/verify-shared-models.py --hash --only juggernaut` verifica el archivo descargado. La presencia del archivo no prueba todavía inferencia.
- Los 4 Wan 2.2 y los otros modelos públicos están inventariados en `gpu/model-inventory.json`; **no descargarlos** para la primera imagen. Prohibido descargar LoRA, fotos, modelos privados o datasets de Lucía.

**Ruta de descarga prevista, solo si existen credenciales de lectura R2 autorizadas:**

    git clone --depth 1 --branch main https://github.com/manglefurniture/HACHE-YOUTUBE-AI.git /root/hache-youtube-ai
    cd /root/hache-youtube-ai
    python3.13 -m venv /root/.cache/hache-youtube-r2-venv
    /root/.cache/hache-youtube-r2-venv/bin/pip install boto3==1.35.99
    # Proveer R2_ACCOUNT_ID, AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY
    # por un canal privado y con mínimo privilegio; nunca en comandos o repositorios públicos.
    /root/.cache/hache-youtube-r2-venv/bin/python gpu/provision_models.py --models-dir /root/ComfyUI/models --only juggernaut
    python3.13 gpu/verify-shared-models.py --models-dir /root/ComfyUI/models --only juggernaut --hash

**PENDIENTE (no afirmar completado):** validar mecanismo autorizado de lectura del bucket en esta GPU, ejecutar descarga real, comprobar SHA-256 y carga del checkpoint en ComfyUI. Las credenciales existentes de GitHub Actions **no se pueden leer automáticamente desde la GPU**, y el conector de Cloudflare usado para metadatos no equivale a una credencial S3 transferible. No crear ni ampliar permisos sin autorización.

## 5. Validación funcional tras la descarga

1. Confirmar SSH y API local `/system_stats`; comprobar CUDA, VRAM y espacio libre.
2. Seleccionar únicamente `juggernautXL_ragnarok.safetensors` en un workflow SDXL básico (nodos nativos). No instalar nodos de terceros hasta que exista una necesidad verificada.
3. Generar una imagen de prueba original de la ciudad costera de **Año 2085**, con la dirección de `docs/PILOT-2085-VISUAL-BIBLE-V1.md`; anotar seed, sampler, pasos, resolución, tiempo real, VRAM y nombre del checkpoint.
4. Validar el archivo de salida y guardarlo en una ruta autorizada; R2 de medios `hache-ai-youtube-media` solo después de confirmar un mecanismo seguro de subida.
5. Mantener infraestructura de Lucía y Hache Natación sin cambios. Detener la renta al terminar para evitar cargos Spot.

## 6. Checkpoint final de esta sesión

| Criterio | Estado |
| --- | --- |
| Modelo de imagen en bucket R2 | Confirmado (objeto y bytes) |
| GPU RTX 5090 / CUDA 13 | Confirmado |
| Bundle de ComfyUI en imagen | Confirmado |
| ComfyUI local 8188 / túnel privado | **200 OK y UI abierta** |
| Clore HTTP público | **403 / Proxy Not Found**, no usar |
| Descarga de Juggernaut a la GPU | **Pendiente** |
| Verificación SHA-256 local | **Pendiente** |
| Generación real de una imagen | **Pendiente** |
| Reconexión tras reinicio | No probada |

**Fuente de verdad:** `gpu/model-inventory.json`, `docs/CLORE-COMFYUI-TEMPLATE.md`, `docs/CHANNEL-VISION.md`. Este runbook documenta pruebas reales, no sustituye revisión automática ni añade secretos.