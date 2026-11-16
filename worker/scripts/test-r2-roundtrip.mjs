import { createHash, randomUUID } from 'node:crypto';
import { createInterface } from 'node:readline/promises';
import { stdin, stdout } from 'node:process';

const endpoint = process.env.HACHE_R2_URL || 'https://hache-youtube-media-api.hache-ai-youtube.workers.dev';
const key = 'integration-test/' + randomUUID() + '.txt';
const content = 'HACHE-YOUTUBE-AI roundtrip ' + randomUUID();
const url = endpoint + '/objects/' + key;
const rl = createInterface({ input: stdin, output: stdout });
let credential = process.env.HACHE_ISSUER_SECRET;
try {
  if (!credential && stdin.isTTY) credential = await rl.question('ISSUER_SECRET (solo en esta computadora): ');
} finally { rl.close(); }
if (!credential) {
  console.error('Falta HACHE_ISSUER_SECRET. No se ha subido ningun archivo.');
  process.exit(2);
}
const mint = await fetch(endpoint + '/mint', {
  method: 'POST',
  headers: { 'x-issuer-secret': credential, 'content-type': 'application/json' },
  body: JSON.stringify({ prefix: 'integration-test/', methods: ['GET', 'PUT'], ttl: 180 })
});
credential = undefined;
if (!mint.ok) {
  console.error('Emision fallida:', mint.status, (await mint.text()).slice(0, 150));
  process.exit(3);
}
const { token } = await mint.json();
const denied = await fetch(url);
if (denied.status !== 401) throw Error('Acceso anonimo inesperado: ' + denied.status);
const put = await fetch(url, {
  method: 'PUT', headers: { authorization: 'Bearer ' + token, 'content-type': 'text/plain' }, body: content
});
if (put.status !== 201) throw Error('Subida fallida: ' + put.status + ' ' + (await put.text()).slice(0, 150));
const get = await fetch(url, { headers: { authorization: 'Bearer ' + token } });
if (get.status !== 200) throw Error('Descarga fallida: ' + get.status);
const downloaded = await get.text();
if (createHash('sha256').update(content).digest('hex') !== createHash('sha256').update(downloaded).digest('hex')) throw Error('Integridad fallida');
console.log(JSON.stringify({ result: 'PASS', upload: 201, download: 200, anonymous: 401, key, sha256: createHash('sha256').update(content).digest('hex') }, null, 2));
