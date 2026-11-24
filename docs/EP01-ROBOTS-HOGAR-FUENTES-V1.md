# EP01 · Auditoría de fuentes y afirmaciones — 23/11/2026

**Estado:** comprobación inicial del guion [EP01 V1](EP01-ROBOTS-HOGAR-GUION-V1.md). Esta matriz diferencia información comprobada, materiales comerciales, inferencias y ficción. No es una autorización para reutilizar material audiovisual de terceros.

## Fuentes primarias o periodísticas comprobadas

| Código | Fuente | Fecha, tipo y ubicación | Qué sostiene exactamente | Qué NO autoriza afirmar |
|---|---|---|---|---|
| F01 | 1X, sitio oficial de NEO | Página consultada 23/11/2026: https://www.1x.tech/neo | NEO está anunciado como robot doméstico y el fabricante describe funcionamiento autónomo para ciertas tareas y **Expert Mode programado** cuando necesita guía humana; también declara que el acceso de expertos puede supervisarse en horarios acordados | No demuestra tasa real de éxito, autonomía total, despliegue masivo ni política universal de protección de datos |
| F02 | J. R. Stone, ABC7/ABC News | 31/07/2026: https://abcnews.com/Technology/san-francisco-company-offers-cleaning-service-using-humanoid-robots/story?id=135258956 | Tau Robotics ofreció servicios de limpieza a **solicitantes seleccionados** en San Francisco; su CEO afirmó que un operador remoto maneja el robot con asistencia de IA | No sustenta que el servicio sea totalmente autónomo, global, disponible para cualquiera o libre de problemas técnicos |
| F03 | Windl, Leusmann, Schmidt, Feger y Mayer, USENIX SOUPS 2024 | https://www.usenix.org/conference/soups2024/presentation/windl | Estudio sobre preocupaciones de privacidad en robots domésticos y comunicación del estado de sensores; incluye patrones relativos a cámaras, micrófonos y conectividad | No demuestra una vulnerabilidad específica en 1X o Tau ni avala un modelo ficticio de permisos |
| F04 | Wan, Xu, Huynh, Dai, Sun, Xu y Xue, ACM/IEEE SenSys 2026 | https://doi.org/10.1145/3774906.3802795 | Estudio de **56 dispositivos de IoT doméstico**, no necesariamente robots, donde se identificaron riesgos en compartir y revocar accesos | No atribuir esos riesgos concretos a robots NEO/Tau, ni generalizar estadísticamente a todos los hogares |
| F05 | Grace Huckins, MIT Technology Review | 06/11/2026: https://www.technologyreview.com/2026/11/06/1148090/i-watched-a-humanoid-robot-clean-my-apartment-it-felt-like-a-taste-of-the-future/ | Reportaje periodístico original existente y reseñado en otras fuentes; **su texto íntegro no se pudo abrir** en la comprobación actual | No extraer citas textuales ni detalles finos del reportaje sin revisar directamente el artículo |

**Corrección del tratamiento:** se sustituyó la referencia no comprobada a «CBS News del 11 de agosto de 2026» por F02 (ABC News de 31 de julio). No presentar CBS como fuente hasta verificar URL, título y fecha.

## Matriz de afirmaciones que aparecerán en pantalla

| ID | Escena | Afirmación del guion | Tipo | Soporte / advertencia de redacción |
|---|---|---|---|---|
| A01 | S02 | 1X presenta NEO como robot doméstico | Hecho sobre anuncio comercial | F01; atribuir a fabricante |
| A02 | S02 | Algunos trabajos de NEO pueden requerir asistencia programada de expertos | Declaración de fabricante | F01; no sugerir teleoperación constante ni conexión arbitraria |
| A03 | S02 | Tau ofrece servicios de limpieza con robots humanoides en SF | Hecho periodístico | F02; dirigido a participantes seleccionados |
| A04 | S02 | El director de Tau admite control remoto humano apoyado por IA | Afirmación reportada | F02; atribuir al CEO y evitar generalizar al sector |
| A05 | S03 | Tela flexible y hogares variables plantean dificultad de manipulación | Explicación técnica general | Narración conceptual, sin números ni porcentajes |
| A06 | S03 | Autónomo, supervisado y teleoperado no son equivalentes | Distinción conceptual | Explicación técnica, usar infografía propia |
| A07 | S08 | Privacidad en sensores y conectividad de robots domésticos se investiga | Hecho científico | F03; no afirmar que un diseño concreto ya está estandarizado |
| A08 | S06–S07 | Vera puede activar apoyo sin discutirlo con Inés; sistema espera nueva autorización | **Ficción 2042** | Historia original; no atribuir como fallo real de un fabricante |
| A09 | S07 | Permisos por habitación, sesión y revocación inmediata | **Propuesta ficticia** | No equivaler a cumplimiento técnico de productos reales |
| A10 | S04 y S05–S09 | 2042 con robots comunes y Luma como ayudante del hogar | **Hipótesis + ficción** | Rótulo obligatorio y descripción independiente de marcas reales |

## Lista de verificación antes de publicar

- [x] Consultar directamente F01, F02 y F03; distinguir afirmaciones comerciales y periodísticas.
- [x] Verificar existencia y ámbito de F04 (IoT general, no solo robótica).
- [x] Retirar la fuente CBS no confirmada.
- [x] Rotular hechos, hipótesis y ficción en guion y storyboard.
- [x] Redactar historia original sin reutilizar personaje o marca comercial.
- [ ] Revisar pronunciamiento o políticas reales de las compañías si el guion añade afirmaciones de privacidad específicas.
- [ ] Registrar fechas finales de acceso y créditos en gráficos.
- [ ] Obtener permisos/licencias de cualquier clip, fotografía, música o voz externa; preferir ilustraciones y esquemas originales.
- [ ] Corregir cualquier texto de marketing que pudiera dar apariencia de prueba técnica independiente.
- [ ] Verificar con audio real duración, tono y cortes.
- [ ] Revisar animática final y subtítulos con humanos antes de publicarla.

**Alcance real de esta revisión:** verifica las frases utilizadas, pero no certifica exhaustivamente el estado del sector ni el cumplimiento de privacidad de ningún fabricante.
