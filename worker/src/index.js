const LIMIT = 20 * 1024 * 1024;
const json = (value, status = 200) => new Response(JSON.stringify(value), {status, headers: {'content-type':'application/json; charset=utf-8','cache-control':'no-store','x-content-type-options':'nosniff'}});
const decode = value => Uint8Array.from(atob(value.replace(/-/g,'+').replace(/_/g,'/')+'='.repeat((4-value.length%4)%4)), c=>c.charCodeAt(0));
const encode = bytes => btoa(String.fromCharCode(...bytes)).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
async function issueToken(request,env) {
 if (!env.ISSUER_SECRET || !env.SIGNING_SECRET || request.method!=='POST') return json({error:'unauthorized'},401);
 const supplied=request.headers.get('x-issuer-secret')||'';
 if (supplied.length!==env.ISSUER_SECRET.length) return json({error:'unauthorized'},401);
 const expected=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(env.ISSUER_SECRET));
 const received=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(supplied));
 if (!new Uint8Array(expected).every((b,i)=>b===new Uint8Array(received)[i])) return json({error:'unauthorized'},401);
 let input;try {input=await request.json();}catch{return json({error:'invalid_request'},400);}
 const {prefix,methods,ttl=300}=input||{};
 if (typeof prefix!=='string'||prefix.length<2||prefix.length>200||!prefix.endsWith('/')||!(/^[a-zA-Z0-9_./-]+$/).test(prefix)||prefix.includes('..')||
 !Array.isArray(methods)||methods.length<1||methods.length>2||!methods.every(x=>x==='GET'||x==='PUT')||
 !Number.isInteger(ttl)||ttl<1||ttl>900) return json({error:'invalid_scope'},400);
 const exp=Math.floor(Date.now()/1000)+ttl;
 const payload=encode(new TextEncoder().encode(JSON.stringify({prefix,methods,exp})));
 const key=await crypto.subtle.importKey('raw',new TextEncoder().encode(env.SIGNING_SECRET),{name:'HMAC',hash:'SHA-256'},false,['sign']);
 const signature=encode(new Uint8Array(await crypto.subtle.sign('HMAC',key,new TextEncoder().encode(payload))));
 return json({token:payload+'.'+signature,expires_at:exp,prefix,methods});
}
async function authorize(request, env, key) {
 const bearer = request.headers.get('authorization') || '';
 if (!bearer.startsWith('Bearer ') || !env.SIGNING_SECRET) return false;
 const parts = bearer.slice(7).split('.');
 if (parts.length !== 2 || parts[0].length > 2048 || parts[1].length > 100) return false;
 try {
  const cryptoKey = await crypto.subtle.importKey('raw',new TextEncoder().encode(env.SIGNING_SECRET),{name:'HMAC',hash:'SHA-256'},false,['verify']);
  if (!await crypto.subtle.verify('HMAC',cryptoKey,decode(parts[1]),new TextEncoder().encode(parts[0]))) return false;
  const claims = JSON.parse(new TextDecoder().decode(decode(parts[0])));
  const now = Math.floor(Date.now()/1000);
  return Number.isInteger(claims.exp) && claims.exp > now && claims.exp <= now+3600 &&
   typeof claims.prefix === 'string' && claims.prefix.length >= 1 && claims.prefix.length <= 200 && claims.prefix.endsWith('/') &&
   /^[a-zA-Z0-9_./-]+$/.test(claims.prefix) && !claims.prefix.includes('..') &&
   key.startsWith(claims.prefix) && key.length > claims.prefix.length && Array.isArray(claims.methods) &&
   claims.methods.includes(request.method) && claims.methods.every(x=>x==='GET'||x==='PUT');
 } catch {return false;}
}
async function boundedBody(stream) {
 if (!stream) return null;
 const reader = stream.getReader();
 const chunks=[]; let length=0;
 try {
  while (true) {
   const {done,value}=await reader.read();
   if (done) break;
   length += value.byteLength;
   if (length > LIMIT) {await reader.cancel().catch(()=>{});return null;}
   chunks.push(value);
  }
 } finally {reader.releaseLock();}
 if (!length) return null;
 const bytes=new Uint8Array(length);let offset=0;
 for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.byteLength;}
 return bytes;
}
export default {
 async fetch(request, env) {
  const url = new URL(request.url);
  if (url.pathname === '/health' && request.method === 'GET') return json({status:'ok'});
  if (url.pathname === '/mint') return issueToken(request,env);
  if (!url.pathname.startsWith('/objects/')) return json({error:'not_found'},404);
  const raw = url.pathname.slice('/objects/'.length);
  let key;
  try {key=decodeURIComponent(raw);} catch {return json({error:'invalid_key'},400);}
  if (!key || key.startsWith('/') || key.includes('..') || key.includes('\\') || key.length > 512 || !/^[a-zA-Z0-9_./-]+$/.test(key)) return json({error:'invalid_key'},400);
  if (!await authorize(request,env,key)) return json({error:'unauthorized'},401);
  if (request.method === 'PUT') {
   const advertised = request.headers.get('content-length');
   if (advertised !== null && (!/^\d+$/.test(advertised) || Number(advertised)>LIMIT)) return json({error:'invalid_size_or_over_20mb'},413);
   const bytes=await boundedBody(request.body);
   if (!bytes) return json({error:'invalid_size_or_over_20mb'},413);
   const result=await env.MEDIA.put(key,bytes,{httpMetadata:{contentType:request.headers.get('content-type')||'application/octet-stream'}});
   return json({key,etag:result.etag},201);
  }
  if (request.method === 'GET') {
   const object=await env.MEDIA.get(key);
   if (!object) return json({error:'not_found'},404);
   return new Response(object.body,{headers:{'content-type':object.httpMetadata?.contentType||'application/octet-stream','cache-control':'private, no-store','x-content-type-options':'nosniff'}});
  }
  return json({error:'method_not_allowed'},405);
 }
};
