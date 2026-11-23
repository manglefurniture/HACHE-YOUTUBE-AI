# Plaza 2085 — V2 candidate workflows

**Unapproved GPU experiments** based on image-to-image of the actual Plaza F; original remains unchanged.

Input: `plaza_central_ref_provisional.png` from private R2 key `refs/2085/plaza_central_ref_provisional.png` (SHA-256 `b6b4b4273cb5e99d0962f6b07cf1ab8a5c74c09fbd994cf8814e6c0d7a5cb259`). Do not substitute City V3: it is the architectural reference, not the literal img2img input here.

GPU: ComfyUI 0.46.0, RTX 5090, `juggernautXL_ragnarok.safetensors`. Both use DPM++ 2M / Karras, CFG 7, 1344x768 inherited from input.

| Variant | File | Seed | Steps | Denoise | Intent |
| --- | --- | ---: | ---: | ---: | --- |
| V2A | `plaza_v2_a_api.json` | 20853021 | 36 | 0.77 | Retain architecture and human activity while introducing a large ancient central tree and worn repaired paving |
| V2B | `plaza_v2_b_api.json` | 20853022 | 38 | 0.86 | Stronger transformation toward a lived-in historic public square; may drift from City V3 |

## Approval gates
- Big tree with a broad crown inside frame, not a cropped right-edge trunk.
- Aged public square with repaired paving, weathered benches and credible chess activity, not a pristine corporate patio or lawn.
- Continuity with City V3: white curved architecture, ribbed slim towers, golden-hour light.
- Photographic realism, valid people and chess elements, no neon/text.
- Render and visually review each output; record prompt ID, actual dimensions, SHA-256 and real GPU status. Keep outputs private on R2. No workflow/image is approved automatically.

This PR does not edit deployment, VPS, or any of Lucia's private assets.
