// Rented GPU receives ONLY a short-lived scoped token, never issuer/signing secrets.
import { readFile, writeFile, stat } from 'node:fs/promises';
import { basename } from 'node:path';
const [operation, key, file] = process.argv.slice(2);
const base = process.env.HACHE_R2_URL || 'https://hache-youtube-media-api.hache-ai-youtube.workers.dev';
const token = process.env.HACHE_R2_TOKEN || (process.env.HACHE_R2_TOKEN_FILE ? (await readFile(process.env.HACHE_R2_TOKEN_FILE,'utf8')).trim() : '');
if (!['GET','PUT'].includes(operation) || !key || !/^[a-zA-Z0-9_./-]+$/.test(key) || key.includes('..') || key.startsWith('/') || !file || !token) {
 console.error('Usage: HACHE_R2_TOKEN_FILE=<file> node gpu-r2-transfer.mjs <GET|PUT> <object-key> <local-file>');
 process.exit(2);
}
if (operation==='PUT' && (await stat(file)).size > 20*1024*1024) {
 console.error('File exceeds Worker 20 MiB limit; large-video multipart is not yet implemented.');
 process.exit(3);
}
const response = await fetch(base+'/objects/'+key,{
 method:operation,headers:{authorization:'Bearer '+token,...(operation==='PUT'?{'content-type':'application/octet-stream'}:{})},
 ...(operation==='PUT'?{body:await readFile(file)}:{})
});
if (!response.ok) {console.error('Transfer failed:',response.status);process.exit(1);}
if (operation==='GET') await writeFile(file,new Uint8Array(await response.arrayBuffer()),{flag:'wx'});
else await response.arrayBuffer();
console.log(operation,'completed for',key,'local file',basename(file));
