# S01 — V5 y preproducción Wan
25/11/2026 · Crónicas del Mañana. Provisional, no publicar.
- Recuperado S01_respaldo_completo.zip de Drive, 93.202.639 bytes; 9 hashes internos OK. PR #41 fusionada tras CI, verificador de modelos y revisión automática sin hallazgos.
- V5 720×1280, 25 fps, 1315 cuadros, 52.60 s, H.264/AAC; SHA-256 `0aaf07cb45ffbd335dcee077796023974e0bda746bd1f3c03619f8d320adab84`. Decodificación completa sin errores; AAC de V4 copiado sin recodificar, hash ADTS idéntico `0aed7c8b2be9aacf466514bef89cb9c459e7fb27d5359602958306fce179ac07`; MP3 Axel original intacto. SRT idéntico. Gráficos y subtítulos aprobados conservados.
- Recreación IA solo P01 0–1.52 s; ficción solo P07 23.04–25.28 s. P14 40.52–45.96 s cambia retrato repetido por capas perceptivas abstractas con distorsión progresiva; P15 45.96–49.92 s Elena reflexiva. Tarjeta P16 provisional sin desarrollar cierre nuevo. Revisados fotogramas; revisión humana y UI real de Shorts pendientes.
- Paquete S01_preproduccion_V5.zip: SHA-256 `dcd3ca44ea778b6f79e1afe209970916fae74d32058fbc0f4dafd4bfd04d1b41`. Contiene MP4, ASS, SRT, storyboard V5, script CPU reproducible, siete referencias 576×1024, manifiestos, plan JSON, cinco grafos API offline y hojas visuales. Se conserva respaldo anterior. Carpeta Drive: https://drive.google.com/drive/folders/1BqfTqpJLywOpkaCMpTMWyiucieOmX1Wb. 
- P08/P10/P13 derivados de originales; P11 recorte de P10 para conservar vestuario, requiere revisión de encuadre y manos; P15 ampliado desde referencia 360×640, **no es máster definitivo**. P09 CPU y P14 CPU recomendados; no generar salvo necesidad editorial.
- Usar [smoke test verificado](VAST-RTX4090-WAN22-I2V-SMOKE-2026-11-23.md), cuatro hashes de gpu/model-inventory.json y scripts de provisión existentes. RTX 4090 24 GB; comprobar API privada, espacio, cola, modelos y esquemas antes de enviar. No subir secretos R2.
- Candidato vertical 432×768, 16 fps, 20 pasos split 10/10, CFG 3.5, shift 5, Euler/simple, batch 1; no validado en GPU. Si OOM, bajar a 384×672 y recortar 9:16. Validación estructural offline de cinco grafos de 15 nodos, referencias, duraciones y masters; no equivale a prueba GPU.

| Orden | Plano | Edición s | Cuadros Wan | Movimiento / aceptación |
|---|---|---:|---:|---|
| 1 | P08 | 2.00 | 33 | Blink, respiración, push-in; identidad y equipo estables |
| 2 | P10 | 2.32 | 49 | Miradas, sonrisa sutil, manos quietas; continuidad de ambos rostros |
| 3 | P11 | 1.88 | 33 | Contacto inmóvil, blink; sin dedos extra, vestuario P10 |
| 4 | P13 | 1.92 | 33 | Sonrisa estable, blink; rostro, lazo y anatomía intactos |
| 5 | P15 | 3.96 | 81 | Reflexión, blink, push-in; esperar máster nativo de mayor calidad |

Prompts positivos/negativos específicos y parámetros en wan_plan_v5.json; los grafos usan el master S01_Pxx.png en input/. Generar uno a uno; revisar identidad, anatomía, parpadeo, continuidad cromática, textura y ausencia de flicker. Recortar a CSV sin alterar narración. Pendiente: aprobación V5, master P15, revisión P11, smoke vertical, generación Wan, música/SFX con derechos, cierre de marca reutilizable y exportación final 1080×1920. No GPU, gastos, publicación ni VPS.
