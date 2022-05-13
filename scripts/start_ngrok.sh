#!/bin/sh

# Set local port from command line arg or default to 8080
LOCAL_PORT=${1-8080}

echo "Start ngrok in background on port [ $LOCAL_PORT ]"
nohup /snap/bin/ngrok http ${LOCAL_PORT} & > /tmp/start_ngrok.out 2>&1

echo "Extracting ngrok public url ."
contador=1
NGROK_PUBLIC_URL=""
while [ -z "$NGROK_PUBLIC_URL" ]; do
  echo "Tentativa: $contador"

  # Run 'curl' against ngrok API and extract public (using 'sed' command)
  export NGROK_PUBLIC_URL=$(curl --silent --max-time 10 --connect-timeout 5 \
                            --show-error http://127.0.0.1:4040/api/tunnels | \
                            sed -nE 's/.*public_url":"https:..([^"]*).*/\1/p')
  sleep 5
  #echo -n "."
  contador=$(($contador+1))
done

echo
echo "NGROK_PUBLIC_URL => [ $NGROK_PUBLIC_URL ]"
