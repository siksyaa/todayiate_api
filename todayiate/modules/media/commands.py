# coding: utf-8

from __future__ import unicode_literals, print_function

import os
from io import BytesIO
from os import path

import requests
from flask import current_app
from s3_saver import S3Saver

from greeme.core.manage import Manager
from greeme.database import db
from greeme.library.get_setting_value import get_setting_value
from greeme.library.thumbnail import thumbnail
from greeme.modules.media.models import Media


from PIL import Image, ImageOps

manager = Manager(current_app)


@manager.command
@manager.option('-i', '--id', help='obj id')
@manager.option('-o', '--obj_type', help='obj type')
def update_width_height(id=None, obj_type=None):
    if not id:
        raise Exception('no index')
    if not obj_type:
        raise Exception('no obj_type')
    media = Media.query.filter(
        (Media.obj_type == obj_type),
        (Media.obj_id == id)
    ).first()
    if not media:
        raise Exception('no such object')

    r = requests.get(media.media_url_sa, stream=True)
    if r.status_code != 200:
        raise Exception('cannot connect to such url')

    # make byte buffer
    upload_file = BytesIO()
    for chunk in r:
        upload_file.write(chunk)

    try:
        image = Image.open(upload_file)
    except IOError:
        return None

    media.width = image.width
    media.height = image.height
    image.close()

    # commit
    db.session.add(media)
    db.session.commit()


@manager.command
@manager.option('-i', '--id', help='obj id')
@manager.option('-o', '--obj_type', help='obj type')
def create_thumbnail(id=None, obj_type=None):
    if not id:
        raise Exception('no index')
    if not obj_type:
        raise Exception('no obj_type')
    media = Media.query.filter(
        (Media.obj_type == obj_type),
        (Media.obj_id == id)
    ).first()
    if not media:
        raise Exception('no such object')

    r = requests.get(media.media_url_sa, stream=True)
    if r.status_code != 200:
        raise Exception('cannot connect to such url')

    # make byte buffer
    upload_file = BytesIO()
    for chunk in r:
        upload_file.write(chunk)

    image_saver = S3Saver(
        storage_type=get_setting_value('USE_S3') and 's3' or None,
        bucket_name=get_setting_value('S3_BUCKET_NAME'),
        access_key_id=get_setting_value('AWS_ACCESS_KEY_ID'),
        access_key_secret=get_setting_value(
            'AWS_SECRET_ACCESS_KEY'),
        field_name='thumbnail',
        storage_type_field='thumbnail_storage_type',
        bucket_name_field='thumbnail_storage_bucket_name',
        base_path=get_setting_value('UPLOADS_FOLDER'),
        static_root_parent=path.abspath(
            path.join(get_setting_value('PROJECT_ROOT'), '..')))

    # make thumbnail
    temp_thumb = thumbnail(upload_file, '300x300', crop='fit')

    # update record
    media.thumbnail = '%s%s%s' % (
        get_setting_value('THINGY_IMAGE_RELATIVE_PATH'), 'thumb_',
        os.path.basename(media.media))
    media.thumbnail_storage_type = 's3'

    # save thumbnail to s3
    image_saver.save(temp_thumb, media.thumbnail, media)

    # commit
    db.session.add(media)
    db.session.commit()

