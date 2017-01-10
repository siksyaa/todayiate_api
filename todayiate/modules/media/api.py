# coding: utf-8
from __future__ import unicode_literals

from io import BytesIO
from os import path

from PIL import Image
from flask import current_app, request
from s3_saver import S3Saver

from ...core import api
from ...core import api_response, error_response
from ...database import db
from ...extensions import oauth
from ...library.get_setting_value import get_setting_value
from ...library.thumbnail import thumbnail
from ...library.upload import is_allowed_file, prefix_file_utcnow_uuid
from ...modules.media.models import Media
from .schema import MediaSchema

media_schema = MediaSchema()


@api.route('/media', methods=['POST'])
@oauth.require_oauth('email')
def media_upload():
    """
    이미지 업로드
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        description: The file to upload
        type: file
        required: true
    produces:
      - application/json
    tags:
      - Media
    description: |
      Get information about a media object.
      The returned type key will allow you to differentiate between `image`
      and `video` media.

      Note: if you authenticate with an OAuth Token, you will receive the
      `user_has_liked` key which quickly tells you whether the current user
      has liked this media item.
    security:
      - oauth:
        - email
    responses:
      200:
        description: OK
    """
    #schema:
    #$ref: '#/definitions/Media'
    current_user_id = request.oauth.user.id

    media = Media()
    media.user_id = current_user_id

    upload_file = request.files['file']
    print(upload_file)
    if upload_file and is_allowed_file(upload_file.filename):

        # Initialise s3-saver.
        image_saver = S3Saver(
            storage_type=get_setting_value('USE_S3') and 's3' or None,
            bucket_name=get_setting_value('S3_BUCKET_NAME'),
            access_key_id=get_setting_value('AWS_ACCESS_KEY_ID'),
            access_key_secret=get_setting_value('AWS_SECRET_ACCESS_KEY'),
            field_name='media',
            storage_type_field='media_storage_type',
            bucket_name_field='media_storage_bucket_name',
            base_path=get_setting_value('UPLOADS_FOLDER'),
            static_root_parent=path.abspath(
                path.join(get_setting_value('PROJECT_ROOT'), '..')))

        current_app.logger.info(upload_file)

        if upload_file.filename:
            filename = prefix_file_utcnow_uuid(media, upload_file)
            temp_file = BytesIO()
            upload_file.save(temp_file)

            image_saver.save(
                temp_file,
                get_setting_value('THINGY_IMAGE_RELATIVE_PATH') + filename,
                media)

            # width, height 계산
            image = Image.open(upload_file)
            media.width = image.width
            media.height = image.height

            # upload_file 의 thumbnail 생성하여 BytesIO() 에 저장, s3 에 업로드
            size = '300x300'
            if request.form.get('type') == 'profile':
                size = '100x100'
            temp_thumb = thumbnail(upload_file, size, crop='fit')
            for k, v in [('field_name', 'thumbnail'),
                         ('storage_type_field', 'thumbnail_storage_type'),
                         ('bucket_name_field', 'thumbnail_storage_bucket_name'),
                         ]:
                setattr(image_saver, k, v)

            thumb_filename = 'thumb_' + filename
            image_saver.save(
                temp_thumb,
                get_setting_value(
                    'THINGY_IMAGE_RELATIVE_PATH') + thumb_filename,
                media)

            db.session.add(media)
            db.session.commit()
            current_app.logger.info('Thingy saved success')

            return api_response(media_schema.dump(media).data)

    return error_response(400, 'invalid file')
