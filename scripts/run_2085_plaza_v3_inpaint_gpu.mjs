#!/usr/bin/env node
// Reproducible mask-based plaza comparison via private ComfyUI loopback on laptop Hache.
import {readFile,writeFile,mkdir} from "node:fs/promises";
import {join,resolve} from "node:path";
import {createHash} from "node:crypto";
import {setTimeout as sleep} from "node:timers/promises";
const api="http://127.0.0.1:18188";
// Guard against duplicating the already-submitted V3I job on tunnel recovery.
if(process.env.HACHE_ACK_RESUBMIT!=="1") throw Error("V3I prompt was submitted before SSH dropped. Inspect /history/50d1ae10-6e40-4282-965e-bbb812443a5d and the queue before intentional resubmission; set HACHE_ACK_RESUBMIT=1 only if needed.");
const base="https://raw.githubusercontent.com/manglefurniture/HACHE-YOUTUBE-AI/main/";
const dir=join(resolve(process.argv[2]||process.cwd()),"assets","2085","references");
await mkdir(dir,{recursive:true});
const get=async(url)=>{let r=await fetch(url,{signal:AbortSignal.timeout(120000)}); if(!r.ok)throw Error("GET "+r.status+" "+url);return r;};
console.log("ComfyUI GPU:",(await (await get(api+"/system_stats")).json()).devices?.[0]?.name);
for(const [local,remote] of [["HACHE_2085_PLAZA_V2E_TREE_00001_.png","plaza_v2e_candidate.png"],["plaza_v3ij_ground_mask.png","plaza_v3ij_ground_mask.png"]]){
  const b=await readFile(join(dir,local)); const form=new FormData();
  form.append("image",new Blob([b],{type:"image/png"}),remote);
  form.append("type","input");form.append("overwrite","true");
  const r=await fetch(api+"/upload/image",{method:"POST",body:form,signal:AbortSignal.timeout(120000)});
  if(!r.ok)throw Error("Upload failed "+remote+" "+r.status+" "+await r.text());
  console.log("Uploaded",await r.json());
}
const results=[];
for(const id of ["i","j"]){
 const path="docs/workflows/2085/plaza_v3_"+id+"_ground_inpaint_api.json";
 const workflow=await (await get(base+path)).json();
 const response=await fetch(api+"/prompt",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({prompt:workflow,client_id:"hache-2085-plaza-v3-inpaint"}),signal:AbortSignal.timeout(120000)});
 const submission=await response.json();
 if(!response.ok||submission.error) throw Error("Prompt "+id+" "+JSON.stringify(submission));
 console.log("Submitted",id,submission.prompt_id);
 let h;
 for(let i=0;i<120;i++){await sleep(3000);const hist=await (await get(api+"/history/"+submission.prompt_id)).json();if(hist[submission.prompt_id]){h=hist[submission.prompt_id];break;}}
 if(!h||h.status?.status_str!=="success")throw Error("Failed "+id+" "+JSON.stringify(h?.status||"timeout"));
 const output=Object.values(h.outputs||{}).flatMap(x=>x.images||[])[0];
 if(!output)throw Error("Missing output for "+id);
 const q=new URLSearchParams({filename:output.filename,subfolder:output.subfolder||"",type:output.type||"output"});
 const bytes=Buffer.from(await (await get(api+"/view?"+q.toString())).arrayBuffer());
 const dst=join(dir,"plaza_v3"+id+"_candidate.png");
 await writeFile(dst,bytes,{flag:"wx"});
 const record={id,workflow:path,seed:workflow["3"].inputs.seed,cfg:workflow["3"].inputs.cfg,prompt_id:submission.prompt_id,filename:output.filename,local:dst,bytes:bytes.length,sha256:createHash("sha256").update(bytes).digest("hex"),status:"success_unreviewed"};
 results.push(record);console.log("SAVED",JSON.stringify(record));
}
const manifest=join(dir,"plaza_v3_inpaint_gpu_runs.json");
await writeFile(manifest,JSON.stringify({input:"Plaza V2E",mask:"plaza_v3ij_ground_mask.png",references:results},null,2)+"\n",{flag:"wx"});
console.log("DONE",manifest);
