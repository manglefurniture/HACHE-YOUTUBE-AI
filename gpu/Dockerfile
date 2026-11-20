# Derived from the verified published Lucia runtime; no private Lucia assets are copied.
FROM ghcr.io/manglefurniture/lucia-gpu:clore-55b19cce89ee3eb3d3b0ee92010d52136e09ef70

LABEL org.opencontainers.image.title="HACHE-YOUTUBE-AI GPU"
LABEL org.opencontainers.image.description="Isolated YouTube GPU runtime derived from public Lucia ComfyUI base"
LABEL org.opencontainers.image.source="https://github.com/manglefurniture/HACHE-YOUTUBE-AI"

COPY gpu/verify-shared-models.py /opt/hache-youtube/bin/verify-shared-models.py
COPY gpu/provision_models.py /opt/hache-youtube/bin/provision_models.py
COPY gpu/model-inventory.json /opt/hache-youtube/bin/model-inventory.json
COPY gpu/README.md /opt/hache-youtube/README.md
COPY gpu/start-youtube.sh /usr/local/bin/start-youtube.sh

# The Lucia entrypoint requires private assets; never invoke it for YouTube.
ENTRYPOINT ["/bin/bash", "/usr/local/bin/start-youtube.sh"]

RUN python -m pip install --no-cache-dir boto3==1.35.99

HEALTHCHECK --interval=30s --timeout=5s --start-period=5m --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8188/system_stats', timeout=3)" || exit 1
