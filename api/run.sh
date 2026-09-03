#!/bin/bash

source ./bin/activate # this is the path only for linux Python venvs; for Windows, use ./Scripts/activate (.bat or .ps1)

python ./main.py &
pid=$!

echo -e "Starting Flask server with pid $pid..."
echo ""

source ./.env

echo -e "Starting NGrok agent for ${NGROK_URL}..."
echo ""

ngrok http --log stdout --config ./ngrok.yml --authtoken "${NGROK_TOKEN}" --url "${NGROK_URL}" 5000

echo ""
echo "Stopping..."

sudo kill $pid
