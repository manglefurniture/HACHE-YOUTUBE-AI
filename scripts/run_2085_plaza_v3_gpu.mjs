#!/usr/bin/env node
// One-shot ComfyUI tester for ground-level Plaza V3 (year 2085).
// Source of truth: GitHub. No R2 credentials, VPS access or production modifications.
import {readFile,writeFile,mkdir} from "node:fs/promises";
import {join, resolve} from "node:path";
import {createHash} from "node:crypto";
import {setTimeout as sleep} from "node:timers/promises";

const api="http://127.0.0.1:18188";
const branch="docs/2085-plaza-ground-level-v3-20261122";
const base="https://raw.githubusercontent.com/manglefurniture/HACHE-YOUTUBE-AI/"+branch+"/";
const root=resolve(process.argv[2] || process.cwd());
const dir=join(root,"assets","2085","references");
await mkdir(dir,{recursive:true});
const get=async(url)=>{ const r=await fetch(url,{signal:AbortSignal.timeout(120000)}); if(!r.ok)throw Error("GET "+url+" status "+r.status+" "+(await r.text()).slice(0,350));return r; };
console.log("ComfyUI:",(await (await get(api+"/system_stats")).json()).devices?.[0]?.name);
const original=await readFile(join(dir,"HACHE_2085_PLAZA_V2E_TREE_00001_.png"));
const form=new FormData();
form.append("image",new Blob([original],{type:"image/png"}),"plaza_v2e_candidate.png");
form.append("type","input");
form.append("overwrite","true");
const up=await fetch(api+"/upload/image",{method:"POST",body:form,signal:AbortSignal.timeout(120000)});
if(!up.ok) throw Error("Upload failed "+up.status+" "+await up.text());
console.log("Uploaded input:",await up.json());
const list=[
  ["G","docs/workflows/2085/plaza_v3_g_ground_img2img_api.json"],
  ["H","docs/workflows/2085/plaza_v3_h_ground_txt2img_api.json"]
];
const records=[];
for(const [id,pathname] of list){
  const workflow=await (await get(base+pathname)).json();
  const response=await fetch(api+"/prompt",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({prompt:workflow,client_id:"hache-2085-plaza-v3"}),signal:AbortSignal.timeout(120000)});
  const submission=await response.json();
  if(!response.ok||submission.error)throw Error("Submit "+id+": "+JSON.stringify(submission));
  const promptId=submission.prompt_id;
  console.log("Submitted:",id,promptId);
  let history;
  for(let attempt=0;attempt<90;attempt++){
    await sleep(3000);
    const all=await (await get(api+"/history/"+promptId)).json();
    if(all[promptId]){history=all[promptId];break;}
  }
  if(!history)throw Error("Prompt "+id+" timed out (pending: "+promptId+")");
  if(history.status?.status_str!=="success")throw Error("Prompt "+id+" failed "+JSON.stringify(history.status));
  const outputs=Object.values(history.outputs||{}).flatMap(x=>x.images||[]);
  if(!outputs.length)throw Error("Prompt "+id+" has no images");
  const output=outputs[0];
  const query=new URLSearchParams({filename:output.filename,subfolder:output.subfolder||"",type:output.type||"output"});
  const data=Buffer.from(await (await get(api+"/view?"+query.toString())).arrayBuffer());
  const local=join(dir,"plaza_v3"+id.toLowerCase()+"_candidate.png");
  await writeFile(local,data,{flag:"wx"});
  const sha256=createHash("sha256").update(data).digest("hex");
  const record={id,workflow:pathname,seed:workflow["3"].inputs.seed,denoise:workflow["3"].inputs.denoise,prompt_id:promptId,filename:output.filename,local,size_bytes:data.length,sha256,status:"success_unreviewed"};
  records.push(record); console.log("SAVED",JSON.stringify(record));
}
const manifest=join(dir,"plaza_v3_gpu_runs.json");
await writeFile(manifest,JSON.stringify({date_local:"2026-11-22",gpu:"RTX 5090",model:"juggernautXL_ragnarok.safetensors",references:records},null,2)+"\n",{flag:"wx"});
console.log("DONE manifest:",manifest);
