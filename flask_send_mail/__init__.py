import os
from flask import render_template, Flask
from flask_restful import Api


def create_app():
    from flask_send_mail.models import db, ma
    from flask_send_mail.event_email import (EventEmailListResource, EventEmailCreateResource, EventEmailResource)
    from flask_send_mail.init_database import init_db_command
    from flask_send_mail.recipient import RecipientListResource

    basedir = os.path.abspath(os.path.dirname(__file__))
    api_dir = '/api'

    # Build the Sqlite ULR for SqlAlchemy
    sqlite_url = "sqlite:///" + os.path.join(basedir, "event.db")

    app = Flask(__name__, template_folder="templates")

    # Configure the SqlAlchemy part of the app instance
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["CELERY_BROKER_URL"] = "amqp://myuser:mypassword@localhost:5672/myvhost"
    app.config["CELERY_RESULT_BACKEND"] = "amqp://myuser:mypassword@localhost:5672/myvhost"

    db.init_app(app)
    ma.init_app(app)

    # Initialize Flask-restful resource
    api = Api(app)

    api.add_resource(EventEmailListResource, f'{api_dir}/event_emails')
    api.add_resource(EventEmailCreateResource, f'{api_dir}/save_emails')
    api.add_resource(EventEmailResource, f'{api_dir}/event_emails/<int:id>')
    api.add_resource(RecipientListResource, f'{api_dir}/recipients')

    # api.add_resource(recipient.RecipientResource, f'{api_dir}/recipients/<int:id>')

    @app.route('/')
    def home():
        """
        home page of this app, respond for localhost:5000/
        :return: the rendered template 'home.html'
        """
        return render_template('home.html')

    # add command
    app.cli.add_command(init_db_command)

    return app
