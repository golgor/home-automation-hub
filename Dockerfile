FROM python:3.12-bookworm

RUN useradd -Ms /bin/bash golgor

WORKDIR /app

COPY requirements.lock .
RUN pip install --no-cache-dir --upgrade -r requirements.lock

# Can be used to deploy the app, but not necessary if using docker-compose
# COPY . /app

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--max-requests", "1", "config.wsgi"]