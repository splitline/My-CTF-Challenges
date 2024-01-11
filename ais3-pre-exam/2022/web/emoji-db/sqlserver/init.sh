#!/bin/bash

echo 'Attempting to run script (10 times max)'
PORT="${1:-1433}"
SLEEP="3"

sleep "${SLEEP}"
for i in $(seq 1 10); do
  echo "Attempt #$i ..."
  SQLCMDPASSWORD="$SA_PASSWORD" sqlcmd -S localhost,"${PORT}" -U SA -i init.sql && break || sleep "${SLEEP}";
done

echo 'Initialization script finished'
