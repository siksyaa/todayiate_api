# -*- coding: utf-8 -*-
from flask import jsonify, request
from flask_api_app.core.api import api as api_bp
from todayiate.extensions import oauth


@api_bp.route('/users/self')
@oauth.require_oauth('email')
def users_self():
    """
    유저 정보 가져오기
    ---
    security:
      - oauth:
        - email
    tags:
      - User
    responses:
      200:
        description: OK
    """
    user = request.oauth.user
    return jsonify(data=dict(email=user.email, username=user.username, id=user.id))