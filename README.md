# home-automation-hub
Django application to implement various home automation and management tasks.


## Development
docker run --rm -it $(docker build -q .) /bin/bash
uvicorn config.asgi:application