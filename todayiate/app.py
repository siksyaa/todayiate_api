import os
from os import path

from celery import Celery
from flask_api_app import FlaskApiApp

from .database import db
from .extensions import config, ma, mail


class TodayiateApp(FlaskApiApp):
    pass


def create_app_min():
    app = TodayiateApp(__name__)
    ROOT_PATH = app.root_path

    config.init_app(app)
    app.config.from_yaml(
        file_name='app.yaml',
        search_paths=['/etc/todayiate', path.dirname(ROOT_PATH)]
    )
    UPLOADS_RELATIVE_PATH = app.config['UPLOADS_RELATIVE_PATH']

    app.config['PROJECT_ROOT'] = ROOT_PATH
    app.config['UPLOADS_FOLDER'] = os.path.abspath(
        os.path.join(ROOT_PATH, 'static', UPLOADS_RELATIVE_PATH)
    )
    app.config['MEDIA_FOLDER'] = os.path.abspath(
        os.path.join(ROOT_PATH, 'static', UPLOADS_RELATIVE_PATH.replace('/', ''))
    )
    app.config['MEDIA_URL'] = '/static/%s' % UPLOADS_RELATIVE_PATH
    app.config['MEDIA_THUMBNAIL_FOLDER'] = os.path.abspath(
        os.path.join(ROOT_PATH, 'static', 'cache/thumbnails')
    )
    app.config['MEDIA_THUMBNAIL_URL'] = 'cache/thumbnails/'

    ma.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    return app


def create_celery_app(app=None):
    app = app or create_app_min()
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery
