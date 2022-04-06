#!/bin/bash 


function escapeString {
  PARAM=$1
  echo $PARAM | sed 's/\//\\\//g' | sed 's/\"/\\\"/g'
}

BASEDIR=$(dirname "$0")
$BASEDIR/stop_ngrok.sh
. $BASEDIR/start_ngrok.sh 5005

ARQUIVO_CREDENTIALS="/home/brleite/projetos/rasa-mayerle-bot/credentials.yml"

WEBHOOK_CONFIG_FROM=`cat $ARQUIVO_CREDENTIALS  | grep -v '^$\|^\s*#' | grep -i "webhook_url"`
WEBHOOK_CONFIG_FROM=$(escapeString "$WEBHOOK_CONFIG_FROM")
WEBHOOK_CONFIG_TO='webhook_url: "https://'$NGROK_PUBLIC_URL'/webhooks/telegram/webhook"'
WEBHOOK_CONFIG_TO=$(escapeString "$WEBHOOK_CONFIG_TO")

# cat $ARQUIVO_CREDENTIALS  | sed 's/'"$WEBHOOK_CONFIG_FROM"'/'"$WEBHOOK_CONFIG_TO"'/g'
sed -i 's/'"$WEBHOOK_CONFIG_FROM"'/'"$WEBHOOK_CONFIG_TO"'/g' $ARQUIVO_CREDENTIALS

source /home/brleite/python_vens/rasa_venv/bin/activate

rasa run

