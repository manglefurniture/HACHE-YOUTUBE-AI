# L01 — El día que compramos nuestro primer robot
## Guion maestro V1 — 28/11/2026
Estado: redacción completada, pendiente de aprobación editorial del usuario. Base: [checkpoint de investigación](L01-IRON-PRODUCTION-CHECKPOINT.md), corte 28/11/2026. Versión congelada: no sobrescribir; crear V2 si el usuario solicita cambios. No generar audio/imágenes sin aprobación. Título público recomendado, no aprobado: «¿Comprar un robot humanoide en 2027?».

Narrador único Axel, español. Los textos bajo «Narración» son el único material para sintetizar; referencias, títulos, ventanas y dirección visual no se leen. «equis peng» es guía de pronunciación provisional para la marca XPeng, «Iron» debe probarse en audio; mantener grafía XPeng/IRON en subtítulos. Revisar pronunciación de Guangzhou, TOPS, VLA, GXO y BMW antes de sintetizar el bloque pertinente. Números en voz se escriben en palabras. No usar voces adicionales. Los ocho bloques constituyen una narración continua, sin intros ni despedidas internas.

Duración objetivo: 12–15 min; ventanas nominales de 15:00 (incluyen pausas y cierre). Recuento de narración: 2141 palabras por separación de espacios, excluidas notas; a 135–145 palabras/min ≈ 14.8–15.9 min de voz sin pausas. Duración exacta se medirá después de aprobar cada audio; no acelerar para cuadrar ventanas. Formato 1920×1080 30 fps, animación CPU. Referencias C/R remiten al dossier congelado; no son citas que se lean.

| Bloque | Ventana nominal | Palabras narradas | Estado |
|---|---|---:|---|
| B01 | 00:00–00:45 | 103 | Guion V1 pendiente de aprobación |
| B02 | 00:45–02:30 | 253 | Guion V1 pendiente de aprobación |
| B03 | 02:30–05:00 | 373 | Guion V1 pendiente de aprobación |
| B04 | 05:00–07:00 | 287 | Guion V1 pendiente de aprobación |
| B05 | 07:00–09:00 | 278 | Guion V1 pendiente de aprobación |
| B06 | 09:00–11:00 | 292 | Guion V1 pendiente de aprobación |
| B07 | 11:00–14:00 | 422 | Guion V1 pendiente de aprobación |
| B08 | 14:00–15:00 | 133 | Guion V1 pendiente de aprobación |
| Total | 15:00 | 2141 | Redacción cerrada |

## B01 — El robot que tuvo que demostrar que era una máquina (00:00–00:45)

**Trazabilidad:** C02, C04, C12 · R02, R04, R05, R06 · H/A.

**Dirección visual (orientativa; no es storyboard final):** Abrir en negro con detalle de la pierna mecánica de 2025 (archivo auténtico si hay permiso; si no, esquema propio identificado). Corte por contraste a micrófono y escenario 2026. Cronología breve 2025→2026→2027; el futuro se marca como objetivo. Nada de intro larga.

### Narración

En noviembre de dos mil veinticinco, una empresa china abrió la cubierta de la pierna de su robot humanoide para mostrar que debajo no había una persona.

Un año después, el robot volvió a un escenario. Esta vez llevaba un micrófono y hablaba ante el público.

Su nombre es Iron. Lo desarrolla equis peng, una compañía de automóviles eléctricos que ahora se propone fabricarlo en masa a partir de enero de dos mil veintisiete.

Pero entre construir una máquina que parece humana y vender una que pueda trabajar a nuestro lado hay una distancia enorme.

Hoy vamos a descubrir qué falta para recorrerla.

---

## B02 — De prototipo a producto (00:45–02:30)

**Trazabilidad:** C01–C05 · R01–R05 · H/E.

**Dirección visual (orientativa; no es storyboard final):** Cronología 2024/2025/septiembre 2026/noviembre 2026. Archivo de cada generación o recreaciones claramente identificadas; fábrica representada por esquemas originales si no hay licencia. No intercambiar modelos. Cierre con comparación visual cuerpo/cerebro.

### Narración

La historia comenzó en dos mil veinticuatro, cuando equis peng presentó la primera generación de Iron. En aquel momento, la pregunta era si una compañía especializada en vehículos eléctricos podía trasladar parte de su experiencia a un cuerpo humanoide.

Un automóvil autónomo necesita interpretar su entorno, elegir una trayectoria y ejecutar movimientos con precisión. Un robot que camina sobre dos piernas debe resolver problemas semejantes, pero añade otros. Tiene que mantener el equilibrio, coordinar los brazos y adaptarse a espacios diseñados para nosotros.

Durante la presentación de dos mil veinticinco, su manera de caminar despertó dudas sobre lo que el público estaba viendo. La empresa mostró entonces el mecanismo de una de sus piernas. Aquella demostración aclaraba una cuestión: había una máquina bajo la cubierta. No demostraba, por sí sola, que pudiera actuar sin supervisión.

En septiembre de dos mil veintiséis, la compañía anunció la puesta en marcha de una línea dedicada a Iron. Es un cambio importante. Fabricar un prototipo permite corregir problemas pieza por pieza. Preparar una línea de producción exige que componentes, montaje y controles de calidad puedan repetirse.

El veinticinco de noviembre, en Guangzhou, presentó la versión orientada a producción. La cobertura presencial describe al robot sosteniendo un micrófono y respondiendo preguntas.

La apariencia externa también evolucionó hacia un diseño neutro.

La historia, por tanto, ya no consiste únicamente en lograr que un robot camine. Ahora importa saber si pueden construirse muchas unidades capaces de repetir las mismas tareas.

Para entender ese salto, necesitamos mirar debajo de la cubierta.

---

## B03 — Un cuerpo que debe aprender a moverse (02:30–05:00)

**Trazabilidad:** C06–C10 · R03–R06 · E + explicación conceptual.

**Dirección visual (orientativa; no es storyboard final):** Diagramas originales por capas: articulaciones, mano, puntos táctiles, bucle percepción→plan→acción→retroalimentación, batería y carga. Los esquemas se rotulan como conceptuales; cifras atribuidas a XPeng. Alternar planos generales, detalles y gráficos, no una única silueta repetida.

### Narración

Comencemos por el movimiento. Equis peng declara que esta generación de Iron cuenta con setenta y seis grados de libertad. En robótica, un grado de libertad representa una posibilidad independiente de movimiento. Por ejemplo, doblar una articulación o girar una muñeca.

La cantidad importa, pero no lo explica todo. Una mano humana puede recoger un huevo sin romperlo, sujetar una herramienta o desenredar un cable. Cada acción combina movilidad, percepción y control de la fuerza.

Según las especificaciones del fabricante, cada mano de Iron dispone de veintiún grados de libertad. El robot incorpora además más de mil quinientos puntos de sensibilidad táctil.

Imaginemos la diferencia entre ordenar a una pinza que se cierre y conseguir que una mano se adapte a una taza de café. Primero debe localizar el objeto. Después tiene que decidir dónde sujetarlo, aplicar la fuerza adecuada y corregir el movimiento si la taza empieza a deslizarse.

Ese proceso requiere información constante. La visión ayuda a interpretar la forma y la posición de los objetos. El tacto informa sobre lo que sucede durante el contacto. Y el sistema de control transforma esos datos en movimientos.

Para realizar parte de ese trabajo, Iron incorpora tres procesadores Turing. La compañía los asocia a una capacidad de cálculo de hasta dos mil doscientos cincuenta billones de operaciones por segundo, medida en TOPS. Esa cifra no equivale a una medida de inteligencia: indica capacidad de procesamiento bajo determinadas condiciones, no lo bien que resolverá cualquier problema.

La arquitectura denominada VLA tres punto cero busca conectar la percepción visual, las instrucciones y la ejecución física de las acciones. En términos sencillos, la máquina debe pasar de entender una petición a convertirla en una serie de movimientos.

También necesita energía. La empresa anuncia una batería de estado sólido. Según la información comunicada durante la presentación, veinte minutos de carga permitirían noventa minutos de funcionamiento. No conocemos el rendimiento en todas las condiciones de uso.

Un robot que se recarga varias veces al día puede estar disponible durante más tiempo del que dura cada carga, pero disponibilidad no significa trabajo continuo.

Toda esa tecnología tiene un propósito: actuar en un mundo físico que cambia a cada instante.

Y es precisamente allí donde empieza la prueba más difícil.

---

## B04 — Lo que una demostración no demuestra (05:00–07:00)

**Trazabilidad:** C04, C08, C10, C11, C17 · R04–R06, R08–R09, R13–R14 · H/E/I.

**Dirección visual (orientativa; no es storyboard final):** Escenario y salón del automóvil con archivo licenciado; separar demostración de diagrama hipotético de entorno variable. Secuencia comparativa: entorno preparado frente a objeto desplazado, obstáculo y presencia de personas. Gráficos de intervención humana y parada segura, sin atribuir pruebas no documentadas.

### Narración

Dos días después de su presentación, Iron participó en el salón del automóvil de Guangzhou, donde recibió visitantes y formó parte de una conferencia. La capacidad de caminar, sostener un micrófono e interactuar con personas es interesante. Sin embargo, no sabemos con qué grado de supervisión se realizó cada acción.

Hay una diferencia entre completar una demostración y trabajar durante meses sin producir fallos graves.

Supongamos que un robot debe colocar una caja en una estantería. En un entorno preparado, la caja estará en un lugar conocido, el camino permanecerá despejado y la estantería tendrá una altura prevista.

Ahora cambiemos las condiciones. La caja tiene un asa rota. Alguien cruza frente al robot. Un objeto cae al suelo. La tarea sigue siendo aparentemente la misma, pero aparecen decisiones que no estaban en el recorrido original.

Este ejemplo es hipotético. Sirve para entender por qué el rendimiento en una presentación no puede trasladarse directamente a un establecimiento real.

Equis peng describe funciones de detección de colisiones, límites de fuerza de los motores, control del equilibrio y parada de emergencia. Son características relevantes, pero no constituyen una prueba independiente de seguridad doméstica.

La Federación Internacional de Robótica identifica cuestiones como la fiabilidad, el consumo energético, el mantenimiento y la viabilidad económica entre los retos de la adopción de estas máquinas.

Un cliente industrial necesitará saber cuántas tareas termina correctamente el robot, cuántas veces debe intervenir una persona y cuánto tiempo permanece fuera de servicio.

No basta con que Iron pueda hacer algo una vez. Debe hacerlo de manera repetible, segura y a un coste razonable.

Y esa última condición nos lleva a la noticia que ha convertido este proyecto en algo más que una curiosidad tecnológica: su posible precio.

---

## B05 — ¿Cuánto costará un humanoide? (07:00–09:00)

**Trazabilidad:** C12–C16 · R04, R06–R07, R10–R12 · A/H/E.

**Dirección visual (orientativa; no es storyboard final):** Calendario 2027 con palabra «objetivo anunciado»; coche eléctrico como referencia de escala, nunca rango de precio del robot. Comparación contextual Figure en automoción y Digit en logística, no tabla de rendimiento. Mostrar coste de compra y servicios separados.

### Narración

La compañía sitúa el comienzo de la fabricación en masa en enero de dos mil veintisiete. Durante el primer trimestre pretende entrenar a Iron para asistir en sus establecimientos comerciales. El lanzamiento público figura como objetivo para el segundo trimestre.

Son fechas anunciadas, no entregas ya realizadas.

En una entrevista con Bloomberg, Brian Gu, vicepresidente de equis peng, indicó que el precio podría acercarse al precio mediano de un automóvil eléctrico.

Es una comparación reveladora porque sugiere una escala comercial distinta a la de una máquina experimental. Pero todavía no hay un precio definitivo, ni sabemos cuándo podría comprarse para utilizarlo en una vivienda.

La empresa también contempla ingresos por software y nuevas habilidades. Eso significa que el precio de adquisición podría ser solo una parte del coste de tener el robot.

Iron no está solo. En Estados Unidos, Figure ha comunicado el despliegue de sus humanoides en instalaciones de BMW. Agility Robotics, por su parte, trabaja con GXO en tareas logísticas mediante su robot Digit, y ha anunciado una ampliación de esa colaboración.

Estos casos tienen algo en común: comienzan con funciones delimitadas dentro de entornos laborales. No prueban que una misma máquina pueda sustituir a cualquier trabajador o realizar todas las tareas de una casa.

La competencia no se decidirá exclusivamente por quién construya la figura más parecida a una persona.

También importarán las horas de servicio útil, la facilidad de reparación, el soporte técnico y la posibilidad de integrarla en una empresa sin rediseñar cada espacio.

Si estas máquinas llegan a ser asequibles y fiables, podrían cambiar la manera en que se organiza el trabajo.

Pero queda una cuestión mucho menos visible que su precio.

---

## B06 — El coste de delegar (09:00–11:00)

**Trazabilidad:** C14, C17, C18 · R06–R07, R13–R14 · I (escenarios condicionados).

**Dirección visual (orientativa; no es storyboard final):** Escenarios hipotéticos: comercio, hogar, mantenimiento y supervisión. Gráfico de coste total sin cifras inventadas. Capas de datos/permisos con símbolos legibles. Cerrar con transición cromática y rótulo «Ficción especulativa · Año 2045».

### Narración

Cuando una empresa compra una máquina, no adquiere únicamente un conjunto de piezas. Adquiere la expectativa de obtener un servicio.

Con un robot humanoide habría que considerar el precio inicial, la electricidad, las reparaciones, el software, la formación y las horas de supervisión. Un robot barato que permanece detenido la mitad del tiempo puede resultar más costoso que otra máquina menos flexible pero más fiable.

Tampoco es necesario que desaparezca una profesión para que cambie el trabajo de quienes la ejercen. Si un robot se encarga de transportar mercancías, quizá una persona pase a organizar recorridos, resolver incidentes o revisar el mantenimiento.

En otros casos, una empresa podría necesitar menos personal. El resultado dependerá del coste, de la regulación y de cómo se repartan las ganancias de productividad. Hoy no podemos determinar la magnitud de ese cambio.

En el hogar, las preguntas serían distintas.

Un robot capaz de interpretar órdenes, reconocer objetos y desplazarse por nuestra casa tendría acceso a información especialmente íntima: rutinas, conversaciones y momentos en los que somos vulnerables.

¿Quién conservaría esos datos? ¿Podríamos impedir que salieran de nuestra vivienda? ¿Qué ocurriría si dejamos de pagar una suscripción? Y si una decisión del robot causa un daño, ¿quién respondería por ella?

Son cuestiones abiertas, no características que podamos atribuir sin más a Iron.

La utilidad de estas máquinas dependerá tanto de sus capacidades físicas como de los límites que decidamos establecer.

No sabemos cómo serán los robots domésticos dentro de veinte años. Pero podemos imaginar una situación en la que esos límites dejen de ser una discusión técnica y se conviertan en una decisión familiar.

Viajemos ahora a un futuro posible. No es una predicción ni una demostración de equis peng.

Es el año dos mil cuarenta y cinco.

---

## B07 — La casa de Rafael (11:00–14:00)

**Trazabilidad:** C19 · F · relato original; ningún comportamiento atribuido a IRON real.

**Dirección visual (orientativa; no es storyboard final):** Rotular solo al entrar «Ficción especulativa · Año 2045». Retrofuturismo adulto crema/petróleo/óxido; Rafael (padre mayor), Inés (hija adulta). Ambos personajes originales ficticios. Robot doméstico genérico, sin logo XPeng; conservar diseño. Diseñar 3 espacios: recibidor, cocina y salón. Notificación de emergencia y configuración de permisos como gráficos diegéticos discretos. Animar acciones simples por capas; evitar deformaciones, multitudes o lip sync.

### Narración

Rafael llevaba cuarenta años viviendo en el mismo apartamento. Conocía el ruido de las tuberías, la luz que entraba por la ventana cada tarde y el lugar exacto donde había que golpear el armario para que cerrara bien.

Su hija Inés había intentado convencerlo de que se mudara con ella. Rafael siempre respondía lo mismo: aquella era su casa.

Una mañana llegó un vehículo de reparto. Inés había comprado un robot doméstico. No tenía una cara que imitara la de una persona. Tenía una superficie lisa, dos brazos articulados y una voz tranquila.

Antes de instalarlo, la máquina pidió a Rafael que eligiera qué información podía compartir con otras personas.

Rafael autorizó los avisos de emergencia, pero rechazó el envío de informes sobre sus rutinas.

Durante las primeras semanas, el robot le ayudó a colocar las compras, alcanzar objetos difíciles y mantener el apartamento en orden. Aprendió dónde estaban las llaves y a qué hora prefería desayunar.

Cuando Rafael preparaba café, la máquina esperaba a su lado. A veces le ofrecía ayuda. A veces, él prefería hacerlo solo.

Una tarde, mientras recogía un libro, Rafael perdió el equilibrio y cayó. El robot interrumpió su tarea. Siguiendo el protocolo de emergencia autorizado, solicitó asistencia y avisó a Inés.

El incidente terminó sin consecuencias graves. Pero aquella noche, Inés abrió la configuración del robot. Quería activar un informe diario sobre las actividades de su padre.

La máquina pidió confirmación al residente.

Inés explicó que ella había comprado el robot y quería asegurarse de que todo estaba bien.

Rafael observó la pantalla. Podía imaginar a su hija recibiendo un registro de cada vez que salía de casa, cada comida que omitía y cada visita que recibía.

No le preocupaba que la máquina conociera sus rutinas. Le preocupaba dejar de decidir quién más podía conocerlas.

Inés insistió. No quería volver a pasar una tarde sin saber qué había ocurrido.

Rafael tampoco quería que su hija viviera preocupada. Después de conversar, decidieron conservar los avisos de emergencia y añadir una llamada diaria que él podía iniciar cuando quisiera.

El robot guardó la nueva configuración.

Al día siguiente, Rafael pidió a la máquina que le acercara una silla al balcón. Se sentó frente a la calle y llamó a su hija.

No era un informe. Era una conversación.

Aquel aparato había sido diseñado para asistir a una persona. La dificultad no consistía solamente en aprender cómo servirle una taza o evitar un obstáculo.

Consistía en dejar espacio para que esa persona continuara siendo dueña de su propia vida.

---

## B08 — La pregunta que nos queda (14:00–15:00)

**Trazabilidad:** C12, C13, C18–C19 · A/I/F (regreso explícito a 2026).

**Dirección visual (orientativa; no es storyboard final):** Regresar desde el balcón de 2045 a imagen documental contemporánea o gráfico de IRON 2026. Última pregunta sobre fondo limpio; no repetir gancho visual. Cierre oficial horizontal adaptado 2,6 s sin nueva marca.

### Narración

Volvamos a noviembre de dos mil veintiséis.

Iron todavía tiene que recorrer el camino que separa una presentación pública de un producto fabricado y utilizado a gran escala.

Equis peng anuncia que quiere comenzar ese proceso en dos mil veintisiete. Las fechas, el precio y las capacidades comerciales deberán confirmarse en el mundo real.

La historia de Rafael no ha ocurrido. Pero nos ayuda a formular una pregunta que probablemente tendremos que responder mucho antes de que un robot entre por la puerta de nuestra casa.

Si algún día podemos comprar una máquina capaz de realizar parte de nuestro trabajo, acompañarnos y conocer nuestras rutinas, tendremos que decidir algo más que cuánto estamos dispuestos a pagar.

¿Qué tareas le confiaríamos? ¿Y qué decisiones deberían seguir siendo exclusivamente nuestras?

Esto es Crónicas del Mañana.

## Revisión editorial V1
- El argumento parte de la demostración de 2025 y del lanzamiento de 2026, explica el salto industrial, distingue especificaciones y anuncios de pruebas independientes, y llega al dilema de privacidad/autonomía de Rafael e Inés. Regresa explícitamente a 2026 en B08.
- Se omiten precio exacto, número de asistentes, peso/altura y fechas domésticas no verificadas. Las demostraciones no se presentan como prueba de autonomía universal ni seguridad certificada. Los ejemplos de caja, empleo, coste y hogar son hipotéticos. No se atribuyen capacidades ficticias a XPeng.
- No producir todavía narración, imágenes, storyboard sincronizado, música ni montaje. Derechos de archivo/voz/música y divulgación IA siguen pendientes de verificación. Próximo paso único: aprobación del guion maestro y, después, autorización para voz B01; registrar ID, duración, parámetros y hash. No comenzar B02 antes de cerrar B01.
