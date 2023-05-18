FROM python:3.11.3-slim

RUN groupadd -g 10001 python && \
    useradd -r -u 10001 -g python python

RUN mkdir -p /usr/app/export && chown -R python:python /usr/app

WORKDIR /usr/app

COPY --chown=python:python requirements.txt .
COPY --chown=python:python gh_dependabot_export.py app.py
COPY --chown=python:python scripts/docker-entrypoint.sh .

RUN set euxo pipefail && \
    chmod +x docker-entrypoint.sh && \
    pip install -r requirements.txt

USER 10001

ENV PATH="/usr/app:$PATH"

ENTRYPOINT [ "/usr/app/docker-entrypoint.sh" ]
