from flask import current_app

from haruka import create_app_min
from haruka.database import db

app = None


def get_setting_value(key, default=None):
    try:
        return current_app.config.get(key, default)
    except RuntimeError as e:
        # logger.warning('current_app is inaccessible: %s' % e)
        pass

    global app
    if not app:
        app = create_app_min()

    try:
        db.init_app(app)
        with app.app_context():
            return app.config.get(key, default)
    except:
        return default
