#!/bin/bash

source /home/brleite/python_vens/rasa_venv/bin/activate

export RASA_ACTIONS_PORT=5060

BASEDIR=$(dirname "$0")
cd $BASEDIR/..
rasa run actions -p $RASA_ACTIONS_PORT
