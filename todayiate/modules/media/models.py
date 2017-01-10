# coding: utf-8

from __future__ import unicode_literals

from flask import url_for
from flask_api_app.database import BaseMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from url_for_s3 import url_for_s3

from ...database import db


class Media(db.Model, BaseMixin):
    __tablename__ = 'media'

    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False, )
    user = relationship('User', backref='media')

    obj_id = db.Column(db.Integer)
    obj_type = db.Column(db.Unicode)

    media = db.Column(db.String(255), default='')
    media_storage_type = db.Column(db.String(255), default='')
    media_storage_bucket_name = db.Column(db.String(255), default='')

    width = db.Column(db.Integer, default=0)
    height = db.Column(db.Integer, default=0)

    thumbnail = db.Column(db.String(255), default='')
    thumbnail_storage_type = db.Column(db.String(255), default='')
    thumbnail_storage_bucket_name = db.Column(db.String(255), default='')

    @property
    def is_draft(self):
        return self.obj_id is None and self.obj_type is None

    @property
    def media_url(self):
        from flask import current_app as app
        return (self.media
                and '%s%s' % (
                    app.config['UPLOADS_RELATIVE_PATH'],
                    self.media)
                or None)

    @property
    def media_url_sa(self):
        """image_url_storageaware"""
        if not self.media:
            return None

        if not (
                    self.media_storage_type
                and self.media_storage_bucket_name):
            return url_for(
                'static',
                filename=self.media_url,
                _external=True)

        if self.media_storage_type != 's3':
            raise ValueError(
                ('Storage type "%s" is invalid, the only supported ' +
                 'storage type (apart from default local storage) ' +
                 'is s3.') % self.media_storage_type)

        return url_for_s3(
            'static',
            bucket_name=self.media_storage_bucket_name,
            filename=self.media_url,
            scheme='http',
        )

    @property
    def thumbnail_url(self):
        from flask import current_app as app
        return (self.thumbnail
                and '%s%s' % (
                    app.config['UPLOADS_RELATIVE_PATH'],
                    self.thumbnail)
                or None)

    @property
    def thumbnail_url_sa(self):
        """image_url_storageaware"""
        if not self.thumbnail:
            return None

        if not (
                    self.thumbnail_storage_type
                and self.thumbnail_storage_bucket_name):
            return url_for(
                'static',
                filename=self.thumbnail_url,
                _external=True)

        if self.thumbnail_storage_type != 's3':
            raise ValueError(
                ('Storage type "%s" is invalid, the only supported ' +
                 'storage type (apart from default local storage) ' +
                 'is s3.') % self.thumbnail_storage_type)

        return url_for_s3(
            'static',
            bucket_name=self.thumbnail_storage_bucket_name,
            filename=self.thumbnail_url,
            scheme='http',
        )

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)
