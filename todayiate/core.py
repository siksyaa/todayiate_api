# coding: utf-8
from __future__ import unicode_literals, print_function

import os

from flask import Blueprint
from flask_api_app.core.api import api
from marshmallow import fields

from .extensions import ma

_current_dir = os.path.dirname(__file__)
main = Blueprint('main', __name__,
                 template_folder=os.path.join(_current_dir, 'templates'))

from flask import current_app, request
from flask.json import dumps


class MetaSchema(ma.Schema):
    code = fields.Integer()
    message = fields.String()


class PaginationSchema(ma.Schema):
    next_url = fields.String()
    next_max_id = fields.String()


class EnvelopeSchema(ma.Schema):
    meta = fields.Nested(MetaSchema)
    data = fields.Dict()
    pagination = fields.Nested(PaginationSchema)


def api_response(data, message='OK', pagination=None, status_code=200):
    rv = {
        'data': data,
        'meta': {
            'message': message,
            'code': status_code
        }
    }
    if pagination:
        rv['pagination'] = pagination

    return json_or_jsonp_response(EnvelopeSchema().dump(rv).data)


def error_response(status_code=400, message=None):
    default_messages = {
        400: 'Bad request',
        404: 'Object not found',
        500: 'Internal Server Error'
    }
    if not message:
        message = default_messages.get(status_code, 'unknown error')

    response = api_response({}, message=message, status_code=status_code, pagination=None)
    response.status_code = status_code

    return response


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload


@api.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    return error_response(status_code=error.status_code, message=error.message)


def json_or_jsonp_response(*args, **kwargs):
    indent = None
    if current_app.config['JSONIFY_PRETTYPRINT_REGULAR'] \
            and not request.is_xhr:
        indent = 2

    data = dumps(dict(*args, **kwargs), indent=indent)
    mimetype = 'application/json'

    # is jsonp request?
    callback = request.args.get('callback', False)
    if callback:
        data = str(callback) + '(' + data + ')'
        mimetype = 'application/javascript'

    return current_app.response_class(data, mimetype=mimetype)


@api.errorhandler(404)
def object_not_found(e):
    return error_response(404, 'Object not found')
