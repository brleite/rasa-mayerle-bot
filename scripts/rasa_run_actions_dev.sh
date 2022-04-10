#!/bin/bash

export RASA_ACTIONS_PORT=5060

BASEDIR=$(dirname "$0")
cd $BASEDIR/..
rasa run actions -p $RASA_ACTIONS_PORT
