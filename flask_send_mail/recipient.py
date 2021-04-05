from flask_restful import Resource
from flask import request

from flask_send_mail import models, config


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
        recipient = models.EventEmail.query.get_or_404(id, description=f"Recipient with id {id} not found")
        recipient_schema = models.RecipientSchema()
        return recipient_schema.dump(recipient)

    def patch(self, id):
        """
        func to response to a request PATCH /api/recipients/{id}
        :return: detail of event email given id, 200 OK, or 404 NOT FOUND
        """
        recipient = models.Recipient.query.get_or_404(id, description=f"Recipient with id {id} not found")
        recipient_schema = models.RecipientSchema()

        if 'name' in request.json:
            recipient.name = request.json['name']
        if 'email' in request.json:
            recipient.email = request.json['email']

        config.db.session.commit()
        return recipient_schema.dump(recipient)

    def delete(self, id):
        """
        func to response to a request DELETE /api/recipients/{id}
        :return: 204 No Content
        """
        recipient = models.Recipient.query.get_or_404(id)
        config.db.session.delete(recipient)
        config.db.session.commit()
        return '', 204
