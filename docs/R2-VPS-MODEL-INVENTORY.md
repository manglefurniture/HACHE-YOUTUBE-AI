# VPS model inventory for shared R2

Observed on 2026-11-19 from the Hache Natación VPS volume `/srv/lucia-models`.

## Shared candidate

| Source | Size (bytes) | SHA-256 | Planned R2 key | Status |
|---|---:|---|---|---|
| `/srv/lucia-models/juggernautXL_ragnarok.safetensors` | 7105350162 | `dd08fa32f98d05a2443ca1419e46df1575a0811f6e3b246d9dd47ff20f5eb66a` | `shared/checkpoints/juggernautXL_ragnarok.safetensors` | Not transferred; waiting for an authorized streaming source and R2 write/readback verification |

Juggernaut XL is a general SDXL checkpoint and the only clearly reusable shared model selected from this volume. The planned key is a proposal; no object was written.

## Excluded from shared inventory

FaceID, CLIP vision, InsightFace and face detector auxiliary weights are present, but are face-recognition-related components and are not included pending licensing and use review. No photos, personal reference material, private workflows, datasets, or Lucia-specific LoRA are listed here.

## Transfer status and constraints

- The R2 bucket is private (`hache-ai-models`; public domain disabled). Cloudflare's management API list endpoint did not return S3 objects, so it is not used here as evidence that the bucket is empty.
- GitHub Actions contains R2 credentials used by the Wan workflow. Connector access cannot reveal secret values or establish whether their R2 permissions are prefix-restricted.
- Wan transfer workflow reads remote Hugging Face sources. The Hache Natación VPS has no configured GitHub Actions runner and no installed AWS CLI, Rclone, or Wrangler available to stream this volume into that workflow.
- No transfer from the VPS, R2 write, secret change, service change, or deletion was performed.
- Before transfer, provide/confirm an authorized streaming path from this VPS and verify credentials are restricted to `shared/`. After upload, read the object back from R2 and compare byte count and SHA-256 with the source above.
- Keep the Lucia LoRA outside this repository and the shared prefix. Only consider it after a separate private-prefix permission check.
