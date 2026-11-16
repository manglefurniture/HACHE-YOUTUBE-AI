import test from 'node:test';
import assert from 'node:assert/strict';
import {webcrypto} from 'node:crypto';
import worker from '../src/index.js';
globalThis.crypto ??= webcrypto;
const secret='local-test-secret-long-enough';
const b64=bytes=>Buffer.from(bytes).toString('base64url');
async function token({prefix='pilot/',methods=['GET','PUT'],exp=Math.floor(Date.now()/1000)+300}={}){
 const payload=b64(Buffer.from(JSON.stringify({prefix,methods,exp})));
 const key=await crypto.subtle.importKey('raw',new TextEncoder().encode(secret),{name:'HMAC',hash:'SHA-256'},false,['sign']);
 return payload+'.'+b64(new Uint8Array(await crypto.subtle.sign('HMAC',key,new TextEncoder().encode(payload))));
}
function setup(){
 const data=new Map();
 const env={SIGNING_SECRET:secret,MEDIA:{
  async put(key,body,opts){const bytes=new Uint8Array(await new Response(body).arrayBuffer());data.set(key,{bytes,contentType:opts.httpMetadata.contentType});return {etag:'test-etag'};},
  async get(key){const o=data.get(key);return o?{body:o.bytes,httpMetadata:{contentType:o.contentType}}:null;}
 }};
 const call=(path,method='GET',auth,body,headers={})=>worker.fetch(new Request('https://example.test'+path,{method,headers:{...(auth?{authorization:'Bearer '+auth}:{}),...headers},...(body!==undefined?{body}: {})}),env);
 return {call,env,data};
}
test('health and unauthorized access',async()=>{const {call}=setup();assert.deepEqual(await (await call('/health')).json(),{status:'ok'});assert.equal((await call('/objects/pilot/a')).status,401);assert.equal((await call('/objects/pilot/a','GET','bad')).status,401);});
test('expired, wrong prefix and wrong method are denied',async()=>{const {call}=setup();assert.equal((await call('/objects/pilot/a','GET',await token({exp:1}))).status,401);assert.equal((await call('/objects/other/a','GET',await token())).status,401);assert.equal((await call('/objects/pilot/a','PUT',await token({methods:['GET']}),'x')).status,401);});
test('tampering is denied',async()=>{const {call}=setup();const t=await token();assert.equal((await call('/objects/pilot/a','GET',t.slice(0,-2)+'xx')).status,401);});
test('invalid object keys are denied',async()=>{const {call}=setup();const t=await token();for(const key of ['/objects/%2e%2e%2fsecret','/objects/%5csecret','/objects/%20'])assert.ok([400,404].includes((await call(key,'GET',t)).status));});
test('advertised oversized body rejected',async()=>{const {call}=setup();assert.equal((await call('/objects/pilot/a','PUT',await token(),'x',{'content-length':'20971521'})).status,413);});
test('actual oversized body rejected even with forged length',async()=>{const {call,data}=setup();const huge=new Uint8Array(20*1024*1024+1);const r=await call('/objects/pilot/huge','PUT',await token(),huge,{'content-length':'1'});assert.equal(r.status,413);assert.equal(data.size,0);});
test('private upload/download roundtrip',async()=>{const {call}=setup();const t=await token();const r=await call('/objects/pilot/scene.txt','PUT',t,'hello',{'content-type':'text/plain'});assert.equal(r.status,201);const d=await call('/objects/pilot/scene.txt','GET',t);assert.equal(d.status,200);assert.equal(await d.text(),'hello');assert.equal(d.headers.get('cache-control'),'private, no-store');});
test('missing object returns 404',async()=>{const {call}=setup();assert.equal((await call('/objects/pilot/missing','GET',await token())).status,404);});

test('token prefix must end in slash and never match sibling keys',async()=>{const {call}=setup();assert.equal((await call('/objects/pilotx/a','GET',await token({prefix:'pilot'}))).status,401);assert.equal((await call('/objects/pilot/a','GET',await token({prefix:'pilot'}))).status,401);assert.equal((await call('/objects/pilot/a','GET',await token({prefix:'pilot/'}))).status,404);});
