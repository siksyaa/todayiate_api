# coding: utf-8

from __future__ import unicode_literals

from io import BytesIO

from PIL import Image, ImageOps


def thumbnail(image, size, crop=None, bg=None, quality=85):
    """
    :param image: 이미지 파일 객체
    :param size: size return thumb - '100x100'
    :param crop: crop return thumb - 'fit' or None
    :param bg: tuple color or None - (255, 255, 255, 0)
    :param quality: JPEG quality 1-100
    :return: :thumbnail 이미지가 저장된 file buffer:
    """
    width, height = [int(x) for x in size.split('x')]
    thumb_size = (width, height)
    try:
        image = Image.open(image)
    except IOError:
        return None

    if crop == 'fit':
        img = ImageOps.fit(image, thumb_size, Image.ANTIALIAS)
    else:
        img = image.copy()
        img.thumbnail((width, height), Image.ANTIALIAS)

    if bg:
        img = _bg_square(img, bg)

    thumb_buffer = BytesIO()
    img.save(thumb_buffer, image.format, quality=quality)
    thumb_buffer.seek(0)

    return thumb_buffer


def _bg_square(img, color=0xff):
    size = (max(img.size),) * 2
    layer = Image.new('L', size, color)
    layer.paste(img, tuple(map(lambda x: (x[0] - x[1]) / 2, zip(size, img.size))))
    return layer
