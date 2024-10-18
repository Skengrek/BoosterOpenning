#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
done

# run a worker :)
poetry run celery -A backend worker --loglevel=info --concurrency 1 -E