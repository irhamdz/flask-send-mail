from . import config


class EventEmail(config.db.Model):
    __tablename__ = 'event_email'
    id = config.db.Column(config.db.Integer, primary_key=True)
    event_id = config.db.Column(config.db.Integer)
    email_subject = config.db.Column(config.db.String(150), nullable=False)
    email_content = config.db.Column(config.db.Text, nullable=False)
    timestamp = config.db.Column(config.db.DateTime, nullable=False)
    is_active = config.db.Column(config.db.Boolean, default=True)


class EventEmailSchema(config.ma.Schema):
    class Meta:
        fields = ('id', 'event_id', 'email_subject', 'email_content', 'timestamp', 'is_active')
        model = EventEmail
