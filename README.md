# flask-send-mail
Web app for sending mail based on timestamp given build with flask

## Development
- create and activate new Python virtual environment

``python3 -m venv env``

``source env/bin/activate``

- install dependencies

``pip install -r requirements.txt``

- set env variables for local machine

``export FLASK_APP=flask-mail/app``

``export FLASK_ENV=development``

- initialize database

``flask init-db``

- run app

``flask run``

- testing

``pytest``