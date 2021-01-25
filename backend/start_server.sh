#!/bin/bash

# turn on bash's job control
# set -m
# apply migrations
python manage.py migrate

# check deployment settings
python manage.py check --deploy

# run job queue
python manage.py process_tasks &

# start server (main process)
python manage.py runserver 0.0.0.0:8000
