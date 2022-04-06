#!/bin/bash 

BASEDIR=$(dirname "$0")
PROPERTY_FILE=$BASEDIR/config.properties

function getProperty {
  PROP_KEY=$1
  PROP_VALUE=`cat $PROPERTY_FILE | grep "$PROP_KEY" | cut -d'=' -f2`
  echo $PROP_VALUE
}

BOTID=$(getProperty "telegram.botid")

$BASEDIR/stop_ngrok.sh
. $BASEDIR/start_ngrok.sh 5005
echo "URL"
echo $NGROK_PUBLIC_URL

JSON_BODY='{"url":"https://'$NGROK_PUBLIC_URL'/webhooks/telegram/webhook"}'

echo $JSON_BODY

curl -d $JSON_BODY -H "Content-Type: application/json" -X POST https://api.telegram.org/bot$BOTID/setWebhook 
