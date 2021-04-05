from datetime import datetime

from celery import Celery
from celery.schedules import crontab

from flask_send_mail import create_app
from flask_send_mail.models import Recipient, RecipientSchema, EventEmail, EventEmailSchema

app = create_app()
app.app_context().push()
celery = Celery(__name__)

celery.conf.update(
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    broker_url=app.config["CELERY_BROKER_URL"],
    timezone="UTC",
)


@celery.on_after_finalize.connect
def setup_subscription_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='*/1'),
        number_adding.s()
    )


@celery.task(name='add_number')
def number_adding():
    with app.app_context():
        event_email = EventEmail.query.all()
        event_email_schema = EventEmailSchema(many=True)
        event_email_data = event_email_schema.dump(event_email)
        for data_event in event_email_data:
            data_timestamp = datetime.strptime(data_event.get('timestamp'), "%Y-%m-%dT%H:%M:%S")
            now = datetime.now()
            if data_timestamp == now:
                # send event email
                return 'send email'
