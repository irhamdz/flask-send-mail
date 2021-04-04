from datetime import datetime

from flask_restful import Resource
from flask import abort, request

from . import models, config


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


def construct_timestamp(param: str):
    return datetime.strptime(param, "%Y-%m-%d %H:%M:%S")


EVENT_EMAIl = {
    1: {
        "event_id": 1,
        "email_subject": "Future AI Event",
        "email_content": "Lorem ipsum dolor sir amet praesent sapien massa, convallis a pellentesque nec",
        "timestamp": get_timestamp()
    },
    2: {
        "event_id": 2,
        "email_subject": "Jakarta Fair Event",
        "email_content": "Lorem ipsum dolor sir amet praesent sapien massa, convallis a pellentesque nec",
        "timestamp": get_timestamp()
    },

}


class EventEmailListResource(Resource):
    def get(self):
        """
        func to response to a request GET /api/event_emails with the complete list of event emails
        :return: sorted list of event emails, 200 OK
        """
        event_email = models.EventEmail.query.all()
        event_email_schema = models.EventEmailSchema(many=True)

        return event_email_schema.dump(event_email)

    def post(self):
        """
        func to response a request POST /api/event_emails
        :return: 201 created
        """

        new_event_email = models.EventEmail(
            event_id=request.json['event_id'],
            email_subject=request.json['email_subject'],
            email_content=request.json['email_content'],
            timestamp=construct_timestamp(request.json['timestamp'])
        )
        config.db.session.add(new_event_email)
        config.db.session.commit()
        event_email_schema = models.EventEmailSchema()
        return event_email_schema.dump(new_event_email), 201


class EventEmailResource(Resource):
    def get(self, event_id):
        """
        func to response to a request GET /api/event_emails/{event_id}
        :return: detail of event email given id, 200 OK, or 404 NOT FOUND
        """

        event_email = models.EventEmail.query.filter(models.EventEmail.event_id == event_id).one_or_none()

        if event_email is not None:
            event_email_schema = models.EventEmailSchema()
            return event_email_schema.dump(event_email)
        else:
            abort(404, f"Event email with event id {event_id} not found")

    # def patch(self, post_id):
    #     post = Post.query.get_or_404(post_id)
    #
    #     if 'title' in request.json:
    #         post.title = request.json['title']
    #     if 'content' in request.json:
    #         post.content = request.json['content']
    #
    #     db.session.commit()
    #     return post_schema.dump(post)
    #
    # def delete(self, post_id):
    #     post = Post.query.get_or_404(post_id)
    #     db.session.delete(post)
    #     db.session.commit()
    #     return '', 204
