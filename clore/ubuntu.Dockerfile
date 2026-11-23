# Independent Ubuntu/Clore variant. Unlike the Rocky image, it follows the
# proven PRL mining pattern: Clore owns SSH (autossh/S6), and /root/onstart.sh
# owns ComfyUI. No apt/pip/model download during a rental's startup.
FROM nvidia/cuda:13.0.2-cudnn-runtime-ubuntu24.04

LABEL org.opencontainers.image.source="https://github.com/manglefurniture/HACHE-YOUTUBE-AI"
LABEL org.opencontainers.image.title="HACHE Clore ComfyUI Ubuntu"
LABEL org.opencontainers.image.description="ComfyUI CUDA 13, Ubuntu 24.04, Clore autossh /root/onstart.sh"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ARG DEBIAN_FRONTEND=noninteractive
ARG COMFYUI_COMMIT=720e923631e685e9cb28b9e2cc7b43f82b44033f
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    PYTHONUNBUFFERED=1 \
    HACHE_COMFY_DIR=/opt/ComfyUI \
    HACHE_COMFY_PYTHON=/opt/hache-venv/bin/python \
    PATH="/opt/hache-venv/bin:$PATH"

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      ca-certificates curl git python3 python3-venv python3-pip \
      libgl1 libglib2.0-0 libgomp1 ffmpeg procps \
 && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/hache-venv \
 && /opt/hache-venv/bin/python -m pip install --no-cache-dir --upgrade pip

# Explicit CUDA 13 wheels, so the build cannot silently install CPU-only torch.
RUN /opt/hache-venv/bin/pip install --no-cache-dir \
      torch==2.13.0 torchvision==0.28.0 \
      --index-url https://download.pytorch.org/whl/cu130

# Pin the ComfyUI source to a real upstream commit; never clone HEAD at rental time.
RUN mkdir -p /opt/ComfyUI \
 && curl --fail --location --retry 3 --silent --show-error \
      "https://codeload.github.com/Comfy-Org/ComfyUI/tar.gz/${COMFYUI_COMMIT}" \
      | tar -xz --strip-components=1 -C /opt/ComfyUI \
 && test -f /opt/ComfyUI/main.py
RUN /opt/hache-venv/bin/pip install --no-cache-dir \
      -r /opt/ComfyUI/requirements.txt boto3==1.35.99 \
 && /opt/hache-venv/bin/python -c \
      'import torch, torchvision; assert torch.version.cuda and torch.version.cuda.startswith("13."), torch.version.cuda; print("CUDA torch:", torch.__version__, torch.version.cuda)'

COPY scripts/clore-ubuntu-onstart.sh /root/onstart.sh
COPY gpu/provision_models.py /opt/hache-youtube/provision_models.py
COPY gpu/model-inventory.json /opt/hache-youtube/model-inventory.json
RUN chmod 0755 /root/onstart.sh \
 && chmod 0644 /opt/hache-youtube/model-inventory.json

WORKDIR /opt/ComfyUI
# SSH port 22 is managed by Clore's autossh entrypoint, never by this image.
# The ComfyUI API remains loopback-only; do not expose port 8188.
EXPOSE 22
ENTRYPOINT ["/root/onstart.sh"]
