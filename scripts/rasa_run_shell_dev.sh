#!/bin/bash

BASEDIR=$(dirname "$0")
cd $BASEDIR/..
rasa shell -p 5010
