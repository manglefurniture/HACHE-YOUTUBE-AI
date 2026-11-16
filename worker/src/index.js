const json = (value, status = 200) => new Response(JSON.stringify(value), {status, headers: {'content-type':'application/json; charset=utf-8','cache-control':'no-store','x-content-type-options':'nosniff'}});
export default {
 async fetch(request, env) {
  const url = new URL(request.url);
  if (url.pathname === '/health' && request.method === 'GET') return json({status:'ok'});
  const expected = env.API_TOKEN;
  const supplied = request.headers.get('authorization');
  if (!expected || !supplied || supplied !== 'Bearer ' + expected) return json({error:'unauthorized'},401);
  if (!url.pathname.startsWith('/objects/')) return json({error:'not_found'},404);
  const key = decodeURIComponent(url.pathname.slice('/objects/'.length));
  if (!key || key.startsWith('/') || key.includes('..') || key.includes('\\') || key.length > 512 || !/^[a-zA-Z0-9_./-]+$/.test(key)) return json({error:'invalid_key'},400);
  if (request.method === 'PUT') {
   const size = Number(request.headers.get('content-length'));
   if (!Number.isSafeInteger(size) || size < 1 || size > 20*1024*1024) return json({error:'invalid_size_or_over_20mb'},413);
   const result = await env.MEDIA.put(key, request.body, {httpMetadata:{contentType:request.headers.get('content-type') || 'application/octet-stream'}});
   return json({key,etag:result.etag},201);
  }
  if (request.method === 'GET') {
   const object = await env.MEDIA.get(key);
   if (!object) return json({error:'not_found'},404);
   return new Response(object.body,{headers:{'content-type':object.httpMetadata?.contentType || 'application/octet-stream','cache-control':'private, no-store','x-content-type-options':'nosniff'}});
  }
  return json({error:'method_not_allowed'},405);
 }
};