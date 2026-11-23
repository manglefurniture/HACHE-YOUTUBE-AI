# Clore variant of the upstream image. SSH is installed at image-build time so
# rentals do not run a distro-wide update before SSH becomes available.
FROM yanwk/comfyui-boot:cu130-slim-v2

RUN dnf install -y openssh-server \
    && dnf clean all \
    && rm -rf /var/cache/dnf

COPY scripts/clore-entrypoint.sh /usr/local/bin/hache-clore-entrypoint.sh
COPY scripts/clore-comfyui-start.sh /usr/local/bin/hache-clore-comfyui-start.sh
RUN chmod 0755 /usr/local/bin/hache-clore-entrypoint.sh /usr/local/bin/hache-clore-comfyui-start.sh

ENTRYPOINT ["/usr/local/bin/hache-clore-entrypoint.sh"]
