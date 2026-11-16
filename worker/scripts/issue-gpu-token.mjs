// Run only on a trusted controller, never on a rented GPU.
import { writeFile } from 'node:fs/promises';
const [prefix, methodsText = 'PUT', ttlText = '300', output] = process.argv.slice(2);
const issuer = process.env.HACHE_ISSUER_SECRET;
const base = process.env.HACHE_R2_URL || 'https://hache-youtube-media-api.hache-ai-youtube.workers.dev';
const methods = methodsText.split(',');
const ttl = Number(ttlText);
if (!issuer || !prefix || !/^[a-zA-Z0-9_./-]+$/.test(prefix) || !prefix.endsWith('/') || prefix.includes('..') || prefix.startsWith('/') ||
    !methods.length || methods.some(x => !['GET','PUT'].includes(x)) || !Number.isInteger(ttl) || ttl < 1 || ttl > 900 || !output) {
 console.error('Usage: HACHE_ISSUER_SECRET=... node issue-gpu-token.mjs <prefix/> <GET|PUT|GET,PUT> <ttl<=900> <output-file>');
 process.exit(2);
}
const response = await fetch(base + '/mint', {method:'POST', headers:{'x-issuer-secret':issuer,'content-type':'application/json'},body:JSON.stringify({prefix,methods,ttl})});
if (!response.ok) {console.error('Token request failed:',response.status);process.exit(1);}
const data = await response.json();
await writeFile(output, data.token, {mode:0o600,flag:'wx'});
console.log('Token issued for',prefix,'methods',methods.join(','),'expires',new Date(data.expires_at*1000).toISOString(),'saved to',output);
