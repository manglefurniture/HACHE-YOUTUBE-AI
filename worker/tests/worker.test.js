import test from 'node:test';
import assert from 'node:assert/strict';
import worker from '../src/index.js';

function setup() {
 const data = new Map();
 const env = {API_TOKEN:'local-test-token',MEDIA:{
  async put(key,body,opts){const bytes=new Uint8Array(await new Response(body).arrayBuffer());data.set(key,{bytes,contentType:opts.httpMetadata.contentType});return {etag:'test-etag'};},
  async get(key){const o=data.get(key);return o?{body:o.bytes,httpMetadata:{contentType:o.contentType}}:null;}
 }};
 const call=(path,method='GET',token,body,headers={})=>worker.fetch(new Request('https://example.test'+path,{method,headers:{...(token?{authorization:'Bearer '+token}:{}),...headers},...(body!==undefined?{body}: {})}),env);
 return {call,env,data};
}
test('health does not reveal bucket or secrets',async()=>{const {call}=setup();const r=await call('/health');assert.equal(r.status,200);assert.deepEqual(await r.json(),{status:'ok'});});
test('rejects unauthenticated and wrong tokens',async()=>{const {call}=setup();assert.equal((await call('/objects/test')).status,401);assert.equal((await call('/objects/test','GET','wrong')).status,401);});
test('rejects traversal and invalid object keys',async()=>{const {call}=setup();for(const key of ['/objects/%2e%2e%2fsecret','/objects/%5csecret','/objects/%20']){const r=await call(key,'GET','local-test-token');assert.ok([400,404].includes(r.status),key);}});
test('rejects oversized uploads and missing content length',async()=>{const {call,env}=setup();let r=await call('/objects/a','PUT','local-test-token','x',{'content-length':'20971521'});assert.equal(r.status,413);r=await worker.fetch(new Request('https://example.test/objects/a',{method:'PUT',headers:{authorization:'Bearer local-test-token'},body:'x'}),env);assert.equal(r.status,413);});
test('private upload/download roundtrip',async()=>{const {call}=setup();const r=await call('/objects/pilot/scene.txt','PUT','local-test-token','hello',{'content-length':'5','content-type':'text/plain'});assert.equal(r.status,201);const d=await call('/objects/pilot/scene.txt','GET','local-test-token');assert.equal(d.status,200);assert.equal(await d.text(),'hello');assert.equal(d.headers.get('cache-control'),'private, no-store');});
test('missing object returns 404',async()=>{const {call}=setup();assert.equal((await call('/objects/missing','GET','local-test-token')).status,404);});
