# from celery import Celery
# from flask import current_app
#
#
# def make_celery(app):
#     celery = Celery(
#         app.import_name,
#         backend=app.config['CELERY_RESULT_BACKEND'],
#         broker=app.config['CELERY_BROKER_URL']
#     )
#     celery.conf.update(app.config)
#
#     class ContextTask(celery.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)
#
#     celery.Task = ContextTask
#     return celery
#
#
# # celery = make_celery(current_app)
#
#
# # celery_beat_schedule = {
# #     "time_scheduler": {
# #         "task": "tasks.number_adding",
# #         "schedule": 5.0,
# #     }
# # }
# #
# # celery.conf.update(
# #     result_backend=current_app.config["CELERY_RESULT_BACKEND"],
# #     broker_url=current_app.config["CELERY_BROKER_URL"],
# #     timezone="UTC",
# #     beat_schedule=celery_beat_schedule,
# # )
