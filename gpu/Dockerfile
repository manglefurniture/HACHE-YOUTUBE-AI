# Reuse the existing Lucia GPU runtime without copying Lucia's private assets.
# Pin to the user-confirmed published tag. Pin by digest after an image provenance review.
FROM ghcr.io/manglefurniture/lucia-gpu:clore-55b19cce89ee3eb3d3b0ee92010d52136e09ef70

LABEL org.opencontainers.image.title="HACHE-YOUTUBE-AI GPU"
LABEL org.opencontainers.image.description="Isolated YouTube GPU tooling layered on the existing Lucia GPU runtime"
LABEL org.opencontainers.image.source="https://github.com/manglefurniture/HACHE-YOUTUBE-AI"

COPY gpu/verify-shared-models.py /opt/hache-youtube/bin/verify-shared-models.py
COPY gpu/README.md /opt/hache-youtube/README.md

# Preserve the base image's ENTRYPOINT/CMD, USER and GPU/runtime configuration.
# YouTube inputs/outputs must be mounted separately; no Lucia secrets or data are copied.
