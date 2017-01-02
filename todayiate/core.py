import os

from flask import Blueprint

_current_dir = os.path.dirname(__file__)
main = Blueprint('main', __name__,
                 template_folder=os.path.join(_current_dir, 'templates'))

