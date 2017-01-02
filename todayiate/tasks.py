from datetime import timedelta

from haruka.app import create_celery_app

celery = create_celery_app()

celery.conf.update({
    'CELERYBEAT_SCHEDULE': {
        'generate-upload-tasks': {
            # 'task': 'tasks.add',
            'task': 'haruka.modules.instagram.tasks.generate_upload_tasks',
            'schedule': timedelta(minutes=1),
            'args': ()
        },
        'queue-upload-tasks': {
            'task': 'haruka.modules.instagram.tasks.queue_upload_tasks',
            'schedule': timedelta(minutes=1),
            'args': ()
        }
    }
})

from haruka.modules.instagram.tasks import *
