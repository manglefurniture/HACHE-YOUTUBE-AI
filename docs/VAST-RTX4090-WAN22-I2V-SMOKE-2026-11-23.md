# Vast.ai RTX 4090 — Wan 2.2 image-to-video: verified smoke test (2026-11-23, Cancún)

**Project:** HACHE-YOUTUBE-AI. **Scope:** rented Vast.ai test instance only; never the Hache Natación VPS. **Status:** one real MP4 generated, downloaded and visually inspected. **Creative approval (23 November 2026):** user approved this video test as a reference to continue the retrofuturist illustrated animation experiments. Final publishing quality, the full channel aesthetic, and the automated video production pipeline remain unapproved.

## Runtime examined

- Vast.ai instance: `62262161`; NVIDIA RTX 4090 with 24 GB VRAM, 60 GB overlay disk.
- ComfyUI packaged image `vastai/comfy_v0.43.0-cuda-13.2-py312/jupyter`, API bound privately to `127.0.0.1:18188`. Supervisor programs `comfyui` and `api-wrapper` were running.
- The official operating guide `/etc/vast-agents-guide.md` was read first. The workspace is **not a mounted persistent volume**: stop/start preserves data, recycle/destroy does not.
- GPU usage during the first render: approximately 21,968 MiB and 100% utilization; ~14 GB free disk after model installation. No CUDA or OOM error was observed.

## Installed video models

All four files downloaded directly from Comfy-Org's public Hugging Face repositories and **verified by SHA-256 against `gpu/model-inventory.json`**. The repeatable installer is [`scripts/provision_wan22_public.py`](../scripts/provision_wan22_public.py); it resumes partial downloads, checks the pinned sizes and SHA-256, and requires at least 6 GB of free space after provisioning. R2 already retains the same model versions in `hache-ai-models`; no private R2 credentials were put on the rented GPU.

| ComfyUI location (under `models/`) | Exact size (bytes) | SHA-256 |
| --- | ---: | --- |
| `diffusion_models/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors` | 14,294,742,832 | `6122e79d55e0f235698d11d657f3b196c5273c830da00b2b013c5a048d5e6a42` |
| `diffusion_models/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors` | 14,294,742,832 | `5471a457b6ac404202a5fbe6c11595a3d5641fc766b00f38763f72303fffc21e` |
| `text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors` | 6,735,906,897 | `c3355d30191f1f066b26d93fba017ae9809dce6c627dda5f6a66eaa651204f68` |
| `vae/wan_2.1_vae.safetensors` | 253,815,318 | `2fc39d31359a4b0a64f55876d8ff7fa8d780956ae2cb13463b0223e15148976b` |

Official ComfyUI workflow reference: `Comfy-Org/workflow_templates/templates/video_wan2_2_14B_i2v.json`. The test used the existing **native** ComfyUI nodes only, without additional custom nodes, drivers or LoRAs.

## Reproduce the verified test

Use `scripts/vast_wan22_i2v_smoke.py` on an authorized GPU container **after** checking the four model hashes, queue, free disk, VRAM, and that no conflicting generation is running.

- Put the original reference image at `/workspace/ComfyUI/output/HACHE_RETRO_D_PULP_ROBOT_00001_.png` or adjust the `SRC` path in the smoke script. This illustration is **not stored in GitHub**; the original PNG exists on the Hache laptop, under `Pictures/HacheYouTube/RetroFuturismo_20261123/`.
- The script copies the image into ComfyUI's `input/`, validates the `/object_info/<node>` schemas, POSTs to private `/prompt`, polls `/history/<prompt_id>`, and saves its graph JSON in ComfyUI output.
- Important template compatibility note: **SaveVideo requires the `format` input** on this ComfyUI version. The initial submission was rejected locally by our preflight check; adding `"format":"auto"` fixed it. No GPU render was started by the failed submission.
- Parameters: 640 × 384, 33 frames, 16 fps, FP8 high noise (steps 0–10) then low noise (steps 10–20), Euler/simple, CFG 3.5, seed `20852026`, `ModelSamplingSD3` shift 5.0.
- Actual completed prompt ID: `935d0f3f-0643-4aad-9ff5-650225ba5153`. The terminal process finished in approximately **65.8 seconds** including load and workflow/API overhead.

## Verified output and review

- MP4 from native `SaveVideo`: `/workspace/ComfyUI/output/HACHE_RETRO_WAN22_ROBOT_TEST_00001_.mp4`.
- Verified with `ffprobe`: **H.264, 640×384, 16 fps, 2.0625 seconds, 492,943 bytes**.
- Downloaded to the laptop Hache: `Pictures/HacheYouTube/RetroFuturismo_20261123/HACHE_RETRO_WAN22_ROBOT_TEST_00001_.mp4`.
- Four review frames and `WAN22_ROBOT_FRAME_CONTACT_SHEET.jpg` were copied/generated in the same laptop folder.
- **Visual review:** robot moves head and arms and handles a cloth; recognizable character, warm teal/orange palette and illustrated room remain consistent. Hands and cloth movement show mild artifacts. It is a technical proof of generation, **not final-quality footage**.
- Neither the resulting MP4 nor the GPU image was published or deployed. Hache Natación VPS and Lucía's private models were not touched.

## Cost and next steps

This on-demand instance was advertised at about **US$0.423/hour plus additional charges**; actual provider billing was not separately reconciled. Stop the instance when finished if GPU usage is no longer needed; storage can still be billed. Do **not** destroy or recycle this no-volume instance before backing up any irreplaceable results.

The next experiment should compare 2–3 styles at a fixed image prompt and the same 33-frame budget, improve hand/action continuity, and only then consider official LightX2V LoRAs for more throughput. Do not infer sustained longer-form performance from a single 2-second clip.
