# ComfyUI model sources for R2

The manual workflow downloads these public source files directly from Hugging Face to the private `hache-ai-models` R2 bucket. Each source is pinned to a repository revision and checked by byte size and SHA-256 before upload, then read back from R2 and checked again. The provisioning allowlist and exact R2 keys are in [`gpu/model-inventory.json`](../gpu/model-inventory.json); the keys below were captured from successful GitHub Actions readback logs.

| Model | Exact R2 key | Bytes | SHA-256 |
|---|---|---:|---|
| Wan 2.2 I2V high noise | `shared/wan22/88c2da5cb7414127960b0e9122a50608/wan2.2_i2v_high_noise_14B_fp8_scaled.safetensors` | 14,294,742,832 | `6122e79d55e0f235698d11d657f3b196c5273c830da00b2b013c5a048d5e6a42` |
| Wan 2.2 I2V low noise | `shared/wan22/42d8177486574a208652a40fc8ef2c91/wan2.2_i2v_low_noise_14B_fp8_scaled.safetensors` | 14,294,742,832 | `5471a457b6ac404202a5fbe6c11595a3d5641fc766b00f38763f72303fffc21e` |
| UMT5 XXL encoder | `shared/wan22/13f35e0808a84f84b7620e8119f105ae/umt5_xxl_fp8_e4m3fn_scaled.safetensors` | 6,735,906,897 | `c3355d30191f1f066b26d93fba017ae9809dce6c627dda5f6a66eaa651204f68` |
| Wan VAE 2.1 | `shared/wan22/f104e897187d4f68ac9c1a7f91047f52/wan_2.1_vae.safetensors` | 253,815,318 | `2fc39d31359a4b0a64f55876d8ff7fa8d780956ae2cb13463b0223e15148976b` |
| Juggernaut XL Ragnarok | `shared/comfyui-public/checkpoints/cd815a8f4b714eb5a8fa7f5a69faa46d/juggernautXL_ragnarok.safetensors` | 7,105,350,162 | `dd08fa32f98d05a2443ca1419e46df1575a0811f6e3b246d9dd47ff20f5eb66a` |
| CLIP ViT-H vision encoder | `shared/comfyui-public/clip_vision/cd815a8f4b714eb5a8fa7f5a69faa46d/CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors` | 2,528,373,448 | `6ca9667da1ca9e0b0f75e46bb030f7e011f44f86cbfb8d5a36590fcd7507b030` |
| IP-Adapter FaceID Plus v2 | `shared/comfyui-public/ipadapter/cd815a8f4b714eb5a8fa7f5a69faa46d/ip-adapter-faceid-plusv2_sdxl.bin` | 1,487,555,181 | `c6945d82b543700cc3ccbb98d363b837e9c596281607857c74b713a876daf5fb` |
| IP-Adapter FaceID Plus v2 LoRA | `shared/comfyui-public/loras/ipadapter/cd815a8f4b714eb5a8fa7f5a69faa46d/ip-adapter-faceid-plusv2_sdxl_lora.safetensors` | 371,842,896 | `f24b4bb2dad6638a09c00f151cde84991baf374409385bcbab53c1871a30cb7b` |
| YOLOv8m face detector | `shared/comfyui-public/ultralytics/bbox/cd815a8f4b714eb5a8fa7f5a69faa46d/face_yolov8m.pt` | 51,996,128 | `e3893a92c5c1907136b6cc75404094db767c1e0cfefe1b43e87dad72af2e4c9f` |

The nine files total 47,124,325,694 bytes (about 43.88 GiB). Provisioning flattens only the generated run UUID portion into ComfyUI's expected model paths; it does not create duplicate local copies. `buffalo_l` is excluded.

## Deferred model

The `buffalo_l` InsightFace package is not included in this batch. InsightFace's official terms restrict its pretrained packages to non-commercial research unless a separate commercial license is obtained. See the [official model zoo terms](https://github.com/deepinsight/insightface/blob/master/model_zoo/README.md).
