FROM python:3.12-bookworm as build

RUN useradd -Ms /bin/bash golgor

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential curl
ENV VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

ADD https://astral.sh/uv/install.sh /install.sh
RUN chmod -R 655 /install.sh && /install.sh && rm /install.sh
COPY requirements.lock .
RUN /root/.cargo/bin/uv venv /opt/venv && \
    /root/.cargo/bin/uv pip install --no-cache -r requirements.lock
# RUN pip install --no-cache-dir --upgrade -r requirements.lock

# App image
FROM python:3.12-slim-bookworm
WORKDIR /app
COPY --from=build /opt/venv /opt/venv
COPY . /app

# Activate the virtualenv in the container
# See here for more information:
# https://pythonspeed.com/articles/multi-stage-docker-python/
ENV PATH="/opt/venv/bin:$PATH"
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]