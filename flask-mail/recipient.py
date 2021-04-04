from flask_restful import Resource

from . import models


class RecipientListResource(Resource):
    def get(self):
        """
        func to response to a request GET /api/recipients with the complete list of recipients
        :return: sorted list of recipients, 200 OK
        """
        recipient = models.Recipient.query.all()
        recipient_schema = models.RecipientSchema(many=True)
        return recipient_schema.dump(recipient)


class RecipientResource(Resource):
    def get(self, id):
        """
        func to response to a request GET /api/recipients/{id}
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
