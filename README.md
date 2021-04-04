# flask-send-mail
Web app for sending mail based on timestamp given build with flask

## Development
- create and activate new Python virtual environment

```bash
python3 -m venv env
```

```bash
source env/bin/activate
```

- install dependencies

```bash
pip install -r requirements.txt
```

- set env variables for local machine

```bash
export FLASK_APP=flask-mail/app
```

```bash
export FLASK_ENV=development
```

- initialize database

```bash
flask init-db
```

- run app

```bash
flask run
```

- testing

```bash
pytest
```