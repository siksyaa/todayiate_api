# coding: utf-8
from __future__ import unicode_literals

from os import path

from flask_admin_s3_upload import S3ImageUploadField

from greeme.database import db
from greeme.extensions import admin
from greeme.library.admin_utils import _view_img, ProtectedModelView
from greeme.library.get_setting_value import get_setting_value
from greeme.library.upload import prefix_file_utcnow_uuid
from .models import Media


class MediaAdminView(ProtectedModelView):
    column_display_pk = True
    column_default_sort = ('id', True)
    column_list = ('id',
                   'thumbnail_url_sa',
                   'is_draft',
                   'obj_type', 'obj_id', 'created_at',)
    column_formatters = {
        'thumbnail_url_sa': _view_img(type='rounded')
    }
    column_labels = {
        'is_draft': '임시 여부',
        'thumbnail_url_sa': '이미지',
    }
    form_excluded_columns = (
        'media_storage_type',
        'media_storage_bucket_name',
        'thumbnail_storage_type',
        'thumbnail_storage_bucket_name',
    )

    form_overrides = dict(
        media=S3ImageUploadField,
        thumbnail=S3ImageUploadField,
    )

    form_args = dict(
        media=dict(
            base_path=get_setting_value('UPLOADS_FOLDER'),
            relative_path=get_setting_value('THINGY_IMAGE_RELATIVE_PATH'),
            url_relative_path=get_setting_value('UPLOADS_RELATIVE_PATH'),
            namegen=prefix_file_utcnow_uuid,
            storage_type_field='media_storage_type',
            bucket_name_field='media_storage_bucket_name',
        ),
        thumbnail=dict(
            base_path=get_setting_value('UPLOADS_FOLDER'),
            relative_path=get_setting_value('THINGY_IMAGE_RELATIVE_PATH'),
            url_relative_path=get_setting_value('UPLOADS_RELATIVE_PATH'),
            namegen=prefix_file_utcnow_uuid,
            storage_type_field='thumbnail_storage_type',
            bucket_name_field='thumbnail_storage_bucket_name',
        ),
    )

    def scaffold_form(self):
        form_class = super(MediaAdminView, self).scaffold_form()
        static_root_parent = path.abspath(
            path.join(get_setting_value('PROJECT_ROOT'), '..'))

        if get_setting_value('USE_S3'):
            form_class.media.kwargs['storage_type'] = 's3'
            form_class.thumbnail.kwargs['storage_type'] = 's3'

        form_class.media.kwargs['bucket_name'] = get_setting_value('S3_BUCKET_NAME')
        form_class.media.kwargs['access_key_id'] = get_setting_value('AWS_ACCESS_KEY_ID')
        form_class.media.kwargs['access_key_secret'] = get_setting_value('AWS_SECRET_ACCESS_KEY')
        form_class.media.kwargs['static_root_parent'] = static_root_parent

        form_class.thumbnail.kwargs['bucket_name'] = get_setting_value('S3_BUCKET_NAME')
        form_class.thumbnail.kwargs['access_key_id'] = get_setting_value('AWS_ACCESS_KEY_ID')
        form_class.thumbnail.kwargs['access_key_secret'] = get_setting_value('AWS_SECRET_ACCESS_KEY')
        form_class.thumbnail.kwargs['static_root_parent'] = static_root_parent

        return form_class


admin.add_view(MediaAdminView(Media, session=db.session, name='미디어', category='그림'))
