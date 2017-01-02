from flask_api_app.extensions import admin, oauth, mail
from flask_bootstrap import Bootstrap
from flask_config_helper import Config
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_reggie import Reggie
from flask_swagger_ui import SwaggerUI
from flask_thumbnails_s3 import Thumbnail

bootstrap = Bootstrap()
config = Config()
cors = CORS()
ma = Marshmallow()
reggie = Reggie()
swagger_ui = SwaggerUI()
thumbnail = Thumbnail()
