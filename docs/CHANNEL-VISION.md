# Visión editorial y audiovisual — HACHE-YOUTUBE-AI

**Estado:** dirección creativa aprobada (16 de noviembre de 2026).  
**Alcance:** referencia obligatoria para guiones, identidad visual, elección de modelos y diseño del pipeline. No implica aprobación de presupuestos, publicación ni despliegue.

## Concepto central

**Ciencia real extrapolada hacia futuros posibles mediante historias originales de ciencia ficción fundamentada.**

Inspiración temática y narrativa en Isaac Asimov: consecuencias humanas de la tecnología, dilemas éticos, sociedades futuras y preguntas filosóficas. No imitar textos ni reutilizar personajes, universos o tramas protegidas.

No será un canal de noticias de gadgets ni una colección de predicciones sensacionalistas. El foco está en cómo la ciencia y la tecnología podrían transformar a las personas y las civilizaciones.

## Pilares temáticos

1. **Inteligencia artificial y robótica:** autonomía, trabajo, convivencia y decisiones de las máquinas.
2. **Futuro de la humanidad:** sociedades, economía, ciudades, salud, longevidad y cambios culturales.
3. **Universo y civilizaciones futuras:** exploración y colonización espacial, límites científicos y dilemas de nuevas sociedades.

## Fórmula de cada historia

1. **Ciencia comprobada:** presentar los conocimientos y capacidades actuales, con fuentes verificables.
2. **Extrapolación fundamentada:** explicar las hipótesis y sus incertidumbres; no vender proyecciones como certezas.
3. **Historia del futuro:** desarrollar personajes originales, conflictos, decisiones y consecuencias humanas.

Distinguir explícitamente **hechos**, **hipótesis** y **ficción especulativa** en el guion y cuando sea necesario en pantalla. Priorizar una historia con principio, desarrollo y desenlace sobre una lista de predicciones.

## Identidad audiovisual aprobada

- **Documentales largos:** realismo cinematográfico, escenarios y tecnologías visualmente creíbles.
- **Shorts:** experimentar con animación estilizada, manteniendo coherencia temática.
- **Lenguaje visual:** mezcla de recreaciones cinematográficas y recursos documentales/editoriales (mapas, diagramas, gráficos) cuando aporten claridad.
- **Narración:** reflexiva, inteligente, intrigante y rigurosa; evitar exageraciones y afirmaciones científicas infundadas.
- **Duración inicial orientativa:** 8–12 minutos por documental, con Shorts complementarios; ajustar según pruebas.
- **Revisión humana:** aprobar los materiales antes de publicarlos.

**Pendiente de definir:** nombre público del canal, logotipo, paleta, tipografía, voz/narrador, música, plantilla de miniaturas, estilo preciso de personajes, ritmo de edición y manual visual. No dar estos puntos por aprobados.

## Piloto editorial recomendado (no producido)

**«Año 2085: El último trabajador humano».**

Premisa: la automatización ha transformado el empleo; una sociedad donde trabajar es opcional se enfrenta a la pregunta de qué significa ser útil.

El piloto debe contrastar avances actuales de IA y automatización con extrapolaciones plausibles, y contar una historia humana original. La fecha y el escenario son **ficción especulativa**, no pronósticos.

Otras ideas en reserva:
- «Año 2150: Los primeros humanos que nunca conocerán la Tierra».
- «Año 2100: La inteligencia que decidió protegernos».
- El mecanismo de Anticitera puede servir para un episodio sobre los orígenes de la computación, pero no es el piloto prioritario.

## Tecnología y validación

- **Reutilizar cuando convenga:** ComfyUI y SDXL del proyecto Lucía como punto de partida técnico, **sin utilizar el LoRA personal de Lucía**.
- **Por evaluar:** modelos de animación/video (por ejemplo Wan o LTX), narración, edición, consistencia temporal y costo por minuto terminado. Ninguno queda aprobado automáticamente.
- **Prueba creativa previa:** producir dos versiones de una misma escena de aproximadamente 30 segundos (realista y animada), comparar calidad, consistencia, tiempo y costo; los datos de retención solo existirán después de publicar pruebas autorizadas.
- **No adelantar infraestructura:** antes de nuevas funciones de GPU, transferencias grandes o despliegues, terminar guion piloto, referencias visuales y requisitos reales de producción.

## Orden de trabajo

1. Definir el guion y el tratamiento narrativo del piloto.
2. Preparar referencias y biblia visual; decidir los elementos de marca pendientes.
3. Hacer pruebas visuales y de voz con modelos candidatos; medir costos.
4. Elegir modelos y adaptar el pipeline a los resultados.
5. Implementar únicamente la infraestructura faltante y realizar una producción piloto con revisión humana.

**Regla de proyecto:** ante dudas de alcance o nuevas propuestas técnicas, consultar este documento antes de implementar.

## Validación creativa posterior — 23 de noviembre de 2026

**Aprobado por el usuario:** el resultado de la primera prueba animada de **Wan 2.2 Image-to-Video** a partir de la ilustración retrofuturista **D (robot doméstico)**. Se acepta como referencia para seguir experimentando con una línea visual **editorial retrofuturista adulta**, inspirada en las ilustraciones científicas y de ciencia ficción de los años cincuenta y sesenta (paleta crema, verde azulado y naranja, textura de tinta/impresión).

**Alcance de la aprobación:** se aprueba la **prueba visual y de movimiento** como punto de partida para nuevos experimentos, **no** se aprueba automáticamente una pieza final publicable ni se reemplazan las referencias cinematográficas ya aprobadas para «Año 2085». La convivencia o sustitución de ambos estilos se decidirá después de pruebas narrativas comparables. Persisten problemas por corregir en manos, manipulación de objetos y consistencia temporal.

**Prueba comprobada:** RTX 4090 (Vast.ai), Wan 2.2 I2V FP8 de dos etapas, 640 × 384, 33 fotogramas, 16 fps, MP4 de 2.0625 s. Documentación técnica y rutas: [smoke test Wan 2.2](VAST-RTX4090-WAN22-I2V-SMOKE-2026-11-23.md). Próximo experimento: una escena más larga (aprox. 5 s) manteniendo estilo, personajes y acciones controladas, con revisión humana antes de publicar.
