from datetime import datetime
from os import path

from flask import current_app
from werkzeug import secure_filename
from werkzeug.utils import secure_filename


def prefix_file_utcnow_uuid(model, file_data):
    import shortuuid

    parts = path.splitext(file_data.filename)
    return secure_filename('%s-%s%s' % (
        datetime.utcnow().strftime('%Y%m%d-%H%M%S'),
        shortuuid.uuid(),
        parts[1]))


def is_allowed_file(filename):
    if '?' in filename:
        filename, _ = filename.rsplit('?')

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']