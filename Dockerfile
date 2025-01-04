FROM alpine:3.21

LABEL org.opencontainers.image.authors="Alessandro Sbarbati"
LABEL org.opencontainers.image.description="Uptainer is a Python CLI that automates tool updates, ensuring consistency and reliability in your GitOps-driven infrastructure."
LABEL org.opencontainers.image.documentation="https://uptainer.readthedocs.io"
LABEL org.opencontainers.image.licenses="GPL-3.0"
LABEL org.opencontainers.image.url="https://github.com/asbarbati/uptainer"

ENV USER_UID="1000"
ENV USER_GID="1000"
ENV USER_NAME="app"

RUN adduser -u "${USER_UID}" -D -h /app "${USER_NAME}" \
    && apk --no-cache upgrade && apk add --no-cache git=2.47.1-r0 py3-pip=24.3.1-r0 openssh-client-default=9.9_p1-r2

USER app
WORKDIR /app
ENV UPTAINER_VERSION="0.1.7"

ENV PATH="/app/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

RUN pip install --break-system-packages --user --no-cache-dir "uptainer==${UPTAINER_VERSION}" \
    && mkdir /app/.ssh && printf 'Host *\n    StrictHostKeyChecking no\n' > /app/.ssh/config

# Set an empty volume
VOLUME ["/tmp", "/etc/uptainer", "/app/.ssh/id_rsa"]
CMD ["/app/.local/bin/uptainer", "--config", "/etc/uptainer/config.yaml"]
