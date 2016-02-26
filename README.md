# Data should be in JSON format. See data.json

# Requirements:
Python 2.7
easy_install pip
pip install virtualenv

# create virtualenv and run requirements
pushd .

# Activate virtualenv
. virtpy/bin/activate

# Install requirements
pip install -r requirements.txt
# Sync DB
python manage.py migrate
# Create Super User
python manage.py createsuperuser --username admin --email admin@example.com

# Enter the following Password for username: admin
test1234

# Run Django on localhost:8000
python manage.py runserver

# Run this from the command line
curl -X POST -H "Content-Type: application/json" --data @data.json -u admin:test1234 http://localhost:8000/anneal