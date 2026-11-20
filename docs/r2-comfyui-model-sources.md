# ComfyUI model sources for R2

The manual workflow downloads these public source files directly from Hugging Face to the private `hache-ai-models` R2 bucket. Each source is pinned to a repository revision and checked by byte size and SHA-256 before upload, then read back from R2 and checked again.

Destination keys use `shared/comfyui-public/<ComfyUI folder>/<run id>/<filename>`.

| Model | Pinned source | Bytes | SHA-256 |
|---|---|---:|---|
| Juggernaut XL Ragnarok | [JCTN/Juggernaut](https://huggingface.co/JCTN/Juggernaut/tree/afebc79ee66301a5dc5121728573bf359a2a7b8c) | 7,105,350,162 | `dd08fa32f98d05a2443ca1419e46df1575a0811f6e3b246d9dd47ff20f5eb66a` |
| CLIP ViT-H vision encoder | [h94/IP-Adapter](https://huggingface.co/h94/IP-Adapter/tree/0859e809306db97aa2338e370587ab284e8a754f) | 2,528,373,448 | `6ca9667da1ca9e0b0f75e46bb030f7e011f44f86cbfb8d5a36590fcd7507b030` |
| IP-Adapter FaceID Plus v2 | [h94/IP-Adapter-FaceID](https://huggingface.co/h94/IP-Adapter-FaceID/tree/36ce7f96f0c76c1e8b100f10fa094a2ac48ea1c6) | 1,487,555,181 | `c6945d82b543700cc3ccbb98d363b837e9c596281607857c74b713a876daf5fb` |
| IP-Adapter FaceID Plus v2 LoRA | [h94/IP-Adapter-FaceID](https://huggingface.co/h94/IP-Adapter-FaceID/tree/6eba56f2a87a7ebb2ef5a7737fe6c74df05f1f58) | 371,842,896 | `f24b4bb2dad6638a09c00f151cde84991baf374409385bcbab53c1871a30cb7b` |
| YOLOv8m face detector | [Bingsu/adetailer](https://huggingface.co/Bingsu/adetailer/tree/103b6d3f064975e94b02715bfe5e873c1d1b5862) | 51,996,128 | `e3893a92c5c1907136b6cc75404094db767c1e0cfefe1b43e87dad72af2e4c9f` |

These five files total 11,545,117,815 bytes (about 10.75 GiB). The workflow selection `all-public-comfyui` uploads these five files only.

## Deferred model

The `buffalo_l` InsightFace package is not included in this batch. InsightFace's official terms restrict its pretrained packages to non-commercial research unless a separate commercial license is obtained. See the [official model zoo terms](https://github.com/deepinsight/insightface/blob/master/model_zoo/README.md).