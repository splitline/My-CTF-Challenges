#!/bin/sh

nginx

while true; do
  # 10 minutes
  timeout 600 gunicorn \
    --workers 8 \
    --access-logfile - \
    --error-logfile - \
    --bind 127.0.0.1:8000 \
    --user 1000 \
    --group 1000 \
    --chdir /sup3rrrrr/secret/server/ \
    main_server:app
  echo "Restarting server..."
done
