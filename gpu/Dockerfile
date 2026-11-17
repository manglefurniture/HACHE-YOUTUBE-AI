# Derived from the verified published Lucia runtime; no private Lucia assets are copied.
FROM ghcr.io/manglefurniture/lucia-gpu:clore-55b19cce89ee3eb3d3b0ee92010d52136e09ef70

LABEL org.opencontainers.image.title="HACHE-YOUTUBE-AI GPU"
LABEL org.opencontainers.image.description="Isolated YouTube GPU runtime derived from public Lucia ComfyUI base"
LABEL org.opencontainers.image.source="https://github.com/manglefurniture/HACHE-YOUTUBE-AI"

COPY gpu/verify-shared-models.py /opt/hache-youtube/bin/verify-shared-models.py
COPY gpu/README.md /opt/hache-youtube/README.md
COPY gpu/start-youtube.sh /usr/local/bin/start-youtube.sh

# The Lucia entrypoint requires private assets; never invoke it for YouTube.
ENTRYPOINT ["/bin/bash", "/usr/local/bin/start-youtube.sh"]
