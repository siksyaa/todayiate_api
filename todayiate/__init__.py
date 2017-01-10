from __future__ import absolute_import

import os

import yaml
from flask_debugtoolbar import DebugToolbarExtension
from flask_uploads import configure_uploads

from todayiate.modules.user.models import User, Role
from .app import TodayiateApp, create_app_min
from .core import main
from .extensions import config, ma, bootstrap, thumbnail, swagger_ui, cors, reggie
from .middleware import MethodRewriteMiddleware


def create_app(config_name=None):
    if config_name:
        os.environ['FLASK_ENV'] = config_name

    app = create_app_min()
    app.wsgi_app = MethodRewriteMiddleware(app.wsgi_app)
    app.init_extensions(user_model=User, role_model=Role)

    swagger_spec = {}
    with open(
            os.path.join(
                os.path.dirname(__file__),
                'swagger',
                'SPEC.yaml'
            )
    ) as f:
        swagger_spec.update(yaml.load(f.read()))
    swagger_ui.init_app(app,
                        spec=swagger_spec,
                        params={},
                        oauth_access_token='api.oauth_access_token',
                        oauth_authorize='api.oauth_authorize')

    debug_toolbar = DebugToolbarExtension()
    debug_toolbar.init_app(app)
    thumbnail.init_app(app)
    cors.init_app(app, resources={r"/api/v1.0/*": {"origin": "*"}})
    bootstrap.init_app(app)
    reggie.init_app(app)

    from todayiate.modules.main.uploads import upload_sets

    configure_uploads(app, upload_sets)

    # views
    from .modules.main import views
    # from .modules.instagram import views

    # api

    from flask_api_app.core.api import api
    import todayiate.modules.user.api
    import todayiate.modules.media.api
    # import todayiate.modules.instagram.api

    # admin
    # from .modules.instagram import admin

    app.register_core_blueprint(api=api, main=main, api_url_prefix='/api/v1.0')

    # celery tasks

    return app
