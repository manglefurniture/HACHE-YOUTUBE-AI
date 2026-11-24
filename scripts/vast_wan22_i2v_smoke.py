#!/usr/bin/env python3
"""Wan2.2 I2V smoke test. Uses only installed checkpoints and native ComfyUI nodes."""
import json, shutil, time, urllib.request, urllib.error
from pathlib import Path
HOST="http://127.0.0.1:18188"
ROOT=Path("/workspace/ComfyUI")
OUTPUT=ROOT/"output"
INPUT=ROOT/"input"
SRC=OUTPUT/"HACHE_RETRO_D_PULP_ROBOT_00001_.png"
NAME="HACHE_RETRO_ROBOT_VIDEO_INPUT.png"
ASSETS=[
 ROOT/"models/diffusion_models/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors",
 ROOT/"models/diffusion_models/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors",
 ROOT/"models/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors",
 ROOT/"models/vae/wan_2.1_vae.safetensors",
]
def get(path):
 with urllib.request.urlopen(HOST+path,timeout=10) as r:return json.load(r)
def post(path,data):
 req=urllib.request.Request(HOST+path,data=json.dumps(data).encode(),
     headers={"Content-Type":"application/json"})
 with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
for model in ASSETS:
 if not model.exists() or model.stat().st_size<100_000_000:
  raise RuntimeError("Missing model: "+str(model))
for name in ["UNETLoader","CLIPLoader","VAELoader","LoadImage","WanImageToVideo",
             "ModelSamplingSD3","CLIPTextEncode","KSamplerAdvanced",
             "VAEDecode","CreateVideo","SaveVideo"]:
 info=get("/object_info/"+name).get(name)
 if not info:raise RuntimeError("Missing native ComfyUI node: "+name)
 print("NODE",name,"REQUIRED",list(info["input"].get("required",{})),flush=True)
if not SRC.is_file():raise RuntimeError("Missing input image")
shutil.copyfile(SRC,INPUT/NAME)
prompt="The single domestic humanoid robot in front of the camera gently moves its mechanical hands and folds the towel on the counter, natural deliberate joint movement, the human woman standing in the doorway watches quietly, no new characters, no camera shake, consistent original illustrated vintage retrofuturistic science magazine art, halftone texture, 1960s warm teal rust-orange palette, restrained slow cinematic push-in"
negative="still image, motionless, sudden movement, camera whip, deformed hands, additional limbs, multiplied robots, characters entering scene, material morphing, flicker, blurry faces, subtitles, overlays, text, logo, watermark, cyberpunk, photorealistic"
graph={
 "1":{"class_type":"UNETLoader","inputs":{"unet_name":ASSETS[0].name,"weight_dtype":"default"}},
 "2":{"class_type":"UNETLoader","inputs":{"unet_name":ASSETS[1].name,"weight_dtype":"default"}},
 "3":{"class_type":"ModelSamplingSD3","inputs":{"model":["1",0],"shift":5.0}},
 "4":{"class_type":"ModelSamplingSD3","inputs":{"model":["2",0],"shift":5.0}},
 "5":{"class_type":"CLIPLoader","inputs":{"clip_name":ASSETS[2].name,"type":"wan","device":"default"}},
 "6":{"class_type":"VAELoader","inputs":{"vae_name":ASSETS[3].name}},
 "7":{"class_type":"LoadImage","inputs":{"image":NAME}},
 "8":{"class_type":"CLIPTextEncode","inputs":{"clip":["5",0],"text":prompt}},
 "9":{"class_type":"CLIPTextEncode","inputs":{"clip":["5",0],"text":negative}},
 "10":{"class_type":"WanImageToVideo","inputs":{"positive":["8",0],"negative":["9",0],"vae":["6",0],"width":640,"height":384,"length":33,"batch_size":1,"start_image":["7",0]}},
 "11":{"class_type":"KSamplerAdvanced","inputs":{"model":["3",0],"positive":["10",0],"negative":["10",1],"latent_image":["10",2],"add_noise":"enable","noise_seed":20852026,"steps":20,"cfg":3.5,"sampler_name":"euler","scheduler":"simple","start_at_step":0,"end_at_step":10,"return_with_leftover_noise":"enable"}},
 "12":{"class_type":"KSamplerAdvanced","inputs":{"model":["4",0],"positive":["10",0],"negative":["10",1],"latent_image":["11",0],"add_noise":"disable","noise_seed":20852026,"steps":20,"cfg":3.5,"sampler_name":"euler","scheduler":"simple","start_at_step":10,"end_at_step":20,"return_with_leftover_noise":"disable"}},
 "13":{"class_type":"VAEDecode","inputs":{"samples":["12",0],"vae":["6",0]}},
 "14":{"class_type":"CreateVideo","inputs":{"images":["13",0],"fps":16}},
 "15":{"class_type":"SaveVideo","inputs":{"video":["14",0],"filename_prefix":"HACHE_RETRO_WAN22_ROBOT_TEST","format":"auto"}},
}
# Include only settings accepted by this exact installed ComfyUI build.
for node in graph.values():
 spec=get("/object_info/"+node["class_type"])[node["class_type"]]["input"]
 allowed=set(spec.get("required",{}))|set(spec.get("optional",{}))
 required=set(spec.get("required",{}))
 given=set(node["inputs"])
 unknown=given-allowed
 missing=required-given
 if unknown or missing:
  raise RuntimeError(node["class_type"]+" invalid inputs unknown="+str(unknown)+" missing="+str(missing))
print("SUBMIT_VIDEO_TEST",flush=True)
try:
 res=post("/prompt",{"prompt":graph,"client_id":"hache-wan22-video"})
except urllib.error.HTTPError as e:
 print("COMFYUI_VALIDATION_ERROR",e.read().decode()[:4000],flush=True)
 raise
pid=res["prompt_id"]
print("PROMPT_ID",pid,flush=True)
(OUTPUT/"hache_wan22_video_test_graph.json").write_text(json.dumps(graph,indent=2),encoding="utf-8")
for i in range(900):
 time.sleep(2)
 record=get("/history/"+pid).get(pid,{})
 status=record.get("status",{})
 if status.get("status_str")=="error":raise RuntimeError("COMFYUI_GENERATION_ERROR "+str(status))
 if status.get("completed") or status.get("status_str")=="success":
  print("GENERATED_HISTORY",json.dumps(record.get("outputs",{}))[:5000],flush=True)
  break
 if i%15==0:print("RENDERING",i*2,"seconds",flush=True)
else:raise TimeoutError("Generation did not finish during test window")
