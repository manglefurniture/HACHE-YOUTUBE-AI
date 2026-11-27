# Preparación automática del lote de Shorts

## Alcance
Esta fase transforma los guiones V2 y sus fichas visuales en un paquete reproducible de trabajo. No es un ejecutor de servicios de pago ni un renderizador. El lote A sigue sujeto a aprobación editorial. No se usan créditos de vidIQ, ElevenLabs ni GPU.

## Uso
Desde el repositorio, Python 3.12:

```sh
python scripts/prepare_shorts_batch.py --check
python scripts/prepare_shorts_batch.py --output /ruta/privada/lote-a-v2
```

El directorio recibe `handoff.json` (cinco solicitudes de narración, diez solicitudes de referencias visuales, cronología y registro de personajes/robots, fuentes, claves SHA-256 por solicitud) y `guiones.md` (lectura editorial). La salida es determinista; una repetición idéntica no sobrescribe; una entrada distinta requiere directorio nuevo. Las claves son identificadores locales, no garantía de idempotencia del proveedor. No ejecutar una solicitud de pago sin comprobar el historial de generaciones y el presupuesto autorizado; si el resultado de una llamada es ambiguo, reconciliarlo antes de reintentar.

La voz Axel y modelo eleven_v4 proceden de [S01](S01-VISION-PRODUCTION-CHECKPOINT.md). El cálculo de caracteres no es una cotización ni aprobación de gasto. El cierre oficial se identifica por su hash documentado y deberá comprobarse contra el binario privado antes de montar.

## Universo narrativo
Cada episodio contiene año ficticio, personaje, robot, escenario y suceso. Los hechos científicos están separados de ese registro. No hay conexiones aprobadas; se mantendrán independientes hasta una autorización editorial específica. Comparar referencias contra S01–S03 y los personajes reservados de EP01 antes de generar escenas. Las fichas previas (por ejemplo, Clara e Inés) deben tener referencias históricas revisadas; coincidencias de nombre no equivalen a identidad. No cambiar retroactivamente un capítulo publicado. Las fechas son ficción y no predicciones.

## Próximas puertas
1. Aprobar guiones y presupuesto de narración; comprobar licencia/plan y voz real antes de llamada.
2. Guardar generaciones originales con hash, identificador del proveedor y duración medida. Alinear transcripción con audio; no inventar marcas temporales.
3. Aprobar referencias y comparación visual real, antes de generar planos. El validador actual solo detecta coincidencias en metadatos.
4. Adaptar montaje CPU y controles de calidad; preservar marca, subtítulos, música autorizada y publicación humana.
