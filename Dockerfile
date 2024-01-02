FROM python:3.12-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_VERSION=1.7.1

RUN apt-get update && apt-get install -y build-essential unzip wget python3-dev libldap-2.5-0 && \
  pip install poetry==${POETRY_VERSION} && \
  poetry self add poetry-plugin-export

WORKDIR /src

COPY pyproject.toml poetry.lock /src/

# Export all dependencies, including 'prod', to an requirements.txt-file and install them in /runtime using pip.
RUN poetry export --with prod --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt && \
  pip install --prefix=/runtime --force-reinstall -r requirements.txt

FROM python:3.12-slim-bookworm AS runtime

# Need to install supervisor, this is only used by celery-controller-service in the docker-compose.yml. procps is used for liveness probes in prod.
RUN apt-get update && apt-get install -y supervisor procps

# Copy all python packages installed in /runtime in the build, to the runtime image.
COPY --from=builder /runtime /usr/local

# Copy important libraries from the build image to the runtime image. These are necessary for the psycopg package.
COPY --from=builder /usr/lib/x86_64-linux-gnu/libpq.so.5 lib/
COPY --from=builder /usr/lib/x86_64-linux-gnu/liblber-2.5.so.0 lib/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libsasl2.so.2 lib/
COPY --from=builder /usr/lib/x86_64-linux-gnu/libldap-2.5.so.0 lib/

COPY . /app
WORKDIR /app

# EXPOSE 8000
# ENTRYPOINT ["/bin/bash"]
