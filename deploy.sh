#!/usr/bin/env bash

# create virtualenv and run requirements
#pushd .

# If old virtual env exists, replace it
if [[ -d "virtpy" ]]; then
  rm -rf virtpy
fi

#if [[ ! -d "virtpy" ]]; then
virtualenv virtpy
#fi

if [[ -f "db.sqlite3" ]]; then
  rm -f tmp.db db.sqlite3
fi

# Activate virtualenv
. virtpy/bin/activate

# Install requirements
pip install -r requirements.txt

# Delete migrations
if [[ -d "simulated_annealing/migrations" ]]; then
  rm -rf simulated_annealing//migrations
fi


python manage.py makemigrations simulated_annealing

# Sync DB
python manage.py migrate

# Load DB
python manage.py load_data

deactivate

# Run Django on localhost:8000
#python manage.py runserver

# TO RUN THE TRAVELING SALESMAN PROBLEM WITH SIMULATED ANNEALING
#curl -X POST -H "Content-Type: application/json" --data @data.json -u admin:test1234 http://localhost:8000/anneal