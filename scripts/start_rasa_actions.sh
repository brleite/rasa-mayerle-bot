#!/bin/bash

export RASA_ACTIONS_PORT=5055

source /home/brleite/python_vens/rasa_venv/bin/activate
rasa run actions -p $RASA_ACTIONS_PORT

