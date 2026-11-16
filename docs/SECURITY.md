# Seguridad de R2 (prototipo)

El Worker verifica tokens HMAC-SHA256 con vencimiento máximo de una hora, prefijo de objeto y métodos GET/PUT. No existe endpoint público de emisión de tokens. La clave SIGNING_SECRET se configura exclusivamente como secreto del Worker y en un entorno privado del emisor.

## Emitir token desde un entorno de confianza

```sh
cd worker
SIGNING_SECRET='valor-privado-de-32-o-mas-caracteres' node scripts/mint-token.mjs pilot/ GET,PUT 300
```

Nunca ejecutar con secretos reales en terminales compartidas ni registrar tokens en logs. No entregar SIGNING_SECRET a instancias GPU Spot. El emisor confiable debe entregar únicamente tokens de vida corta y prefijo restringido. No hay servicio de emisión implementado todavía.

El Worker limita las subidas a 20 MiB midiendo bytes realmente recibidos, además de comprobar Content-Length cuando existe. Este diseño acumula como máximo 20 MiB en memoria; para videos grandes implementar transferencia multipart directa y firma temporal específica.

Pendiente antes de producción: rate limiting, revocación/rotación de secretos, protección de replay, autorización del emisor y validación con R2 real. El endpoint GET entrega el contenido solo con autorización, sin caché pública.
