#!/usr/bin/env bash

$DJANGO_PASSWD="test1234"

# easy_install pip
# pip install virtualenv

# update pip
# easy_install --upgrade pip

# create virtualenv and run requirements
pushd .

# If old virtual env exists, replace it
if [[ -d "virtpy" ]]; then
  rm -rf virtpy
fi

#if [[ ! -d "virtpy" ]]; then
virtualenv virtpy
#fi

if [[ -f "db.sqlite3" ]]; then
  rm db.sqlite3
fi

# Activate virtualenv
. virtpy/bin/activate

# Install requirements
pip install -r requirements.txt
# Sync DB
python manage.py migrate
# Create Super User
python manage.py createsuperuser --noinput --username admin --email admin@example.com

# Set a Password for the admin user. Expect a delay
/usr/bin/expect <<EOD
spawn python manage.py changepassword admin
expect "%"
expect "Password:"
send "$DJANGO_PASSWD\r"
expect "Password (again):"
send "$DJANGO_PASSWD\r"
expect eof
EOD


# Run Django on localhost:8000
python manage.py runserver

# TO RUN THE TRAVELING SALESMAN PROBLEM WITH SIMULATED ANNEALING
#curl -X POST -H "Content-Type: application/json" --data @data.json -u admin:test1234 http://localhost:8000/anneal