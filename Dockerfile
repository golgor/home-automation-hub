FROM python:3.12-bookworm AS builder

RUN apt-get update && apt-get install -y build-essential && \
  pip install poetry

WORKDIR /src

COPY pyproject.toml poetry.lock /src/

# Export all dependencies, including 'prod', to an requirements.txt-file and install them in /runtime using pip.
RUN poetry export --with prod --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt && \
  pip install --prefix=/runtime --force-reinstall -r requirements.txt

FROM python:3.12-slim-bookworm AS runtime

# Install libpq-dev for psycopg3. Alternatively, we could have copied the libpq.so.5 file from the builder image, but this would create an issue to build the image on a different architecture.
# The libpq-dev package is about 15MB and available for all architectures, so this is the better solution.
RUN apt update && apt install -y libpq-dev iputils-ping

# Adding a user to avoid running everything as root.
RUN useradd -Ms /bin/bash golgor

# Copy all python packages installed in /runtime in the build, to the runtime image.
COPY --from=builder /runtime /usr/local

# USER golgor
COPY . /app
WORKDIR /app

CMD ["uvicorn", "--host", "0.0.0.0", "config.asgi:application"]