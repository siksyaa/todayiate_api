from flask_uploads import UploadSet

upload_sets = []
IMAGES = tuple('jpg jpeg png'.split())

thingy_image = UploadSet(
    'image',
    IMAGES,
    default_dest=lambda app: '%s%s' % (
        app.config['UPLOADS_FOLDER'],
        app.config['THINGY_IMAGE_RELATIVE_PATH']))

upload_sets.append(thingy_image)
