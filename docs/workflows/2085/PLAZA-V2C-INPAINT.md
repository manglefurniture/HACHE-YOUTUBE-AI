# Plaza V2C — selective inpainting test (not approved)

The earlier V2A/B img2img renders were successfully executed on RTX 5090 but rejected as masters: they lost the distinctive futuristic 2085 skyline. This new experiment starts from **approved City V3** instead of Plaza F and protects the sky, curved building and most upper skyline with an inpainting mask. Only the lower civic park and a central-right tree area are regenerated. The original City V3 file is never modified.

- Source: `ciudad_v3_ref.png`, SHA-256 `471966b3ec158fb56ab324421318327dfee614228bb555a2a6357d6cd7b2100f`, 1344×768.
- Build mask locally: `python scripts/build_2085_plaza_mask.py --image <original-city-v3.png> --output plaza_city_v3_inpaint_mask.png`.
- Upload both original and mask to private ComfyUI input via authenticated localhost tunnel. Load mask's **red channel**.
- Workflow `plaza_v2_c_inpaint_api.json`, seed 20853023, 40 steps, CFG 6.5, denoise 1, `VAEEncodeForInpaint` with growth 6, Juggernaut XL Ragnarok.
- The source skyline and architecture must stay visually continuous with City V3; verify tree, chess and plaza geometry in resulting image. Do not approve by default.
- No model downloads, server configuration changes, Lucía assets or public access.
