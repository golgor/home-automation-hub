FROM python:3.13-bookworm AS builder

RUN useradd -Ms /bin/bash golgor

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.5 /uv /bin/uv

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# App image
FROM python:3.13-slim-bookworm AS runtime
WORKDIR /app
COPY . /app

# Copy Python packages from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Activate the virtualenv in the container
# See here for more information:
# https://pythonspeed.com/articles/multi-stage-docker-python/
ENV PATH="/app/.venv/bin:$PATH"
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]