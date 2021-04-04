from flask_restful import Resource
from flask import request, abort

from . import models, config, helper


class EventEmailListResource(Resource):
    def get(self):
        """
        func to response to a request GET /api/event_emails with the complete list of event emails
        :return: sorted list of event emails, 200 OK
        """
        event_email = models.EventEmail.query.all()
        # query string for get soft deleted data
        include_deleted = request.args.get('include_deleted', '')
        if not helper.convert_env_boolean(include_deleted):
            event_email = models.EventEmail.query.filter_by(is_active=True).all()
        event_email_schema = models.EventEmailSchema(many=True)

        return event_email_schema.dump(event_email)


class EventEmailCreateResource(Resource):
    def post(self):
        """
        func to response a request POST /api/save_emails
        :return: detail created event email, 201 created
        """

        new_event_email = models.EventEmail(
            event_id=request.json['event_id'],
            email_subject=request.json['email_subject'],
            email_content=request.json['email_content'],
            timestamp=helper.construct_timestamp(request.json['timestamp'])
        )

        if 'recipients' in request.json:
            for id in request.json['recipients']:
                recipient = models.Recipient.query.filter_by(id=id).one_or_none()

                if recipient is not None:
                    new_event_email.recipients.append(recipient)

        config.db.session.add(new_event_email)
        config.db.session.commit()
        event_email_schema = models.EventEmailSchema()
        return event_email_schema.dump(new_event_email), 201


class EventEmailResource(Resource):
    def get(self, id):
        """
        func to response to a request GET /api/event_emails/{id}
        :return: detail of event email given id, 200 OK, or 404 NOT FOUND
        """
        event_email = models.EventEmail.query.filter_by(id=id, is_active=True).one_or_none()
        description = f"Event email with id {id} not found or not active"
        if event_email is None:
            return abort(404, description=description)

        event_email_schema = models.EventEmailSchema()
        return event_email_schema.dump(event_email)

    def patch(self, id):
        """
        func to response to a request PATCH /api/event_emails/{id}
        :return: detail of event email given id, 200 OK, or 404 NOT FOUND
        """
        event_email = models.EventEmail.query.get_or_404(id, description=f"Event email with id {id} not found")
        event_email_schema = models.EventEmailSchema()

        if 'event_id' in request.json:
            event_email.event_id = request.json['event_id']
        if 'email_subject' in request.json:
            event_email.email_subject = request.json['email_subject']
        if 'email_content' in request.json:
            event_email.email_content = request.json['email_content']
        if 'timestamp' in request.json:
            event_email.timestamp = helper.construct_timestamp(request.json['timestamp'])

        if 'recipients' in request.json:
            # clear all recipient first
            event_email.recipients = []
            for id in request.json['recipients']:
                recipient = models.Recipient.query.filter_by(id=id).one_or_none()

                if recipient is not None:
                    event_email.recipients.append(recipient)

        config.db.session.commit()
        return event_email_schema.dump(event_email)

    def delete(self, id):
        """
        func to response to a request DELETE /api/event_emails/{id}
        :return: 204 No Content
        """
        event_email = models.EventEmail.query.get_or_404(id)

        # soft delete
        event_email.is_active = False
        config.db.session.commit()
        return '', 204
