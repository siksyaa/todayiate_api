from datetime import datetime
from os import path

from flask import current_app
from werkzeug import secure_filename


def prefix_file_utcnow(model, file_data):
    print 'file_data', file_data
    parts = path.splitext(file_data.filename)
    return secure_filename('%s%s' % (datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S'), parts[1]))


def is_allowed_file(filename):
    if '?' in filename:
        filename, _ = filename.rsplit('?')

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']
