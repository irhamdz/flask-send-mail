from . import config

event_email_recipient = config.db.Table('event_email_recipients',
                                        config.db.Column('recipient_id', config.db.Integer,
                                                         config.db.ForeignKey('recipient.id'), primary_key=True),
                                        config.db.Column('event_email_id', config.db.Integer,
                                                         config.db.ForeignKey('event_email.id'), primary_key=True)
                                        )


class Recipient(config.db.Model):
    id = config.db.Column(config.db.Integer, primary_key=True)
    name = config.db.Column(config.db.String(255))
    email = config.db.Column(config.db.String(150), nullable=False)


class RecipientSchema(config.ma.SQLAlchemySchema):
    class Meta:
        fields = ('id', 'name', 'email')
        model = Recipient


class EventEmail(config.db.Model):
    __tablename__ = 'event_email'
    id = config.db.Column(config.db.Integer, primary_key=True)
    event_id = config.db.Column(config.db.Integer)
    email_subject = config.db.Column(config.db.String(150), nullable=False)
    email_content = config.db.Column(config.db.Text, nullable=False)
    timestamp = config.db.Column(config.db.DateTime, nullable=False)
    is_active = config.db.Column(config.db.Boolean, default=True)
    recipients = config.db.relationship('Recipient', secondary=event_email_recipient, lazy='subquery',
                                        backref=config.db.backref('event_emails', lazy=True))


class EventEmailSchema(config.ma.Schema):
    class Meta:
        fields = ('id', 'event_id', 'email_subject', 'email_content', 'timestamp', 'is_active', 'recipients')
        model = EventEmail

    recipients = config.ma.Nested(RecipientSchema, many=True)
