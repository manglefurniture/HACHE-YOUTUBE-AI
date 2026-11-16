# Emisor de tokens

El Worker expone `POST /mint`, protegido con el secreto independiente `ISSUER_SECRET` enviado en el encabezado `x-issuer-secret`. Este secreto se configura exclusivamente como secreto de Cloudflare y **nunca** debe instalarse en una GPU alquilada ni registrarse en GitHub.

Ejemplo de cuerpo: `{ "prefix": "pilot/", "methods": ["GET", "PUT"], "ttl": 300 }`. La duración máxima es de 900 segundos. El resultado incluye `token` y `expires_at`; el cliente GPU solo recibe el token temporal.

`SIGNING_SECRET` firma los tokens y permanece dentro de Cloudflare. Las rutas de objetos exigen Bearer válido, prefijo terminado en `/` y método autorizado.

**Pendiente para producción:** restringir quién puede solicitar tokens mediante Cloudflare Access o servicio de confianza, agregar rate limiting, revocación y protección contra repetición. No exponer `ISSUER_SECRET` a clientes, navegadores ni proveedores de GPU. Las cargas superiores a 20 MiB requieren un flujo multipart independiente.
