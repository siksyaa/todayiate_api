# coding: utf-8

from __future__ import unicode_literals
from marshmallow import fields
from ...extensions import ma


class MediaSchema(ma.Schema):
    class Meta:
        # fields = ('id', 'media', 'thumbnail', 'user', 'created_at',)
        fields = ('id', 'media', 'thumbnail', 'created_at',)

    # user = fields.Nested(MiniProfileSchema)
    _links = ma.Hyperlinks({
        'self': ma.URLFor('api.media_file', shortcode='<shortcode>'),
    })

    media = fields.Method('get_media_url')
    thumbnail = fields.Method('get_thumbnail_url')

    def get_media_url(self, obj):
        if obj.media_url_sa:
            return {
                'height': 0,
                'width': 0,
                'url': obj.media_url_sa
            }

    def get_thumbnail_url(self, obj):
        if obj.thumbnail_url_sa:
            return {
                'height': 0,
                'width': 0,
                'url': obj.thumbnail_url_sa
            }
