# HACHE-YOUTUBE-AI

Automated AI-powered YouTube documentary production pipeline.

## Dirección editorial aprobada

Ciencia real extrapolada hacia futuros posibles mediante historias originales de ciencia ficción fundamentada, con inspiración temática en Isaac Asimov. Marca pública: [Crónicas del Mañana](https://www.youtube.com/@CronicasdelManana2085). Lanzamiento experimental Shorts-first, con el capítulo largo EP01 en reserva. Ver [estado de lanzamiento y próximos pasos](docs/CHANNEL-LAUNCH-2026-11-24.md).

**Documentos rectores:** [Visión editorial y audiovisual](docs/CHANNEL-VISION.md) y [estándar de credibilidad, IA y monetización de Shorts](docs/SHORTS-EDITORIAL-STANDARD.md). Consultarlo antes de elegir modelos, desarrollar guiones o ampliar la infraestructura.

## Próxima prueba GPU (sin alquiler automático)

[Ruta alternativa con plantilla ComfyUI preinstalada en Clore](docs/CLORE-COMFYUI-TEMPLATE.md): comprobar primero GPU + API, descargar después solo Juggernaut XL desde R2 con validación SHA-256. La imagen GHCR actual se mantiene como respaldo; Wan 2.2 se valida en una fase posterior.

## Recuperación de ComfyUI validada en RTX 5090

[Runbook operativo de Clore (22/11/2026)](docs/CLORE-RTX5090-R2-RUNBOOK-2026-11-22.md): SSH con la clave de Hache, diagnóstico del entrypoint, arranque por IPv4, túnel privado y estado real de R2. El modelo Juggernaut XL está verificado como objeto en R2, pero su descarga y la generación SDXL aún están pendientes.
