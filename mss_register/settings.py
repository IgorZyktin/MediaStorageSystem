# -*- coding: utf-8 -*-

"""Script settings.
"""
import os

APP_CONFIG = 'development'
# APP_CONFIG = 'production'

if APP_CONFIG == 'development':
    BASE_PATH = 'D:\\BGC_ARCHIVE_\\'
    BASE_PATH = 'D:\\_1\\'
    DEBUG = True
else:
    BASE_PATH = '.'
    DEBUG = False

ROOT_PATH = os.path.join(BASE_PATH, 'root')
METAINFO_PATH = os.path.join(ROOT_PATH, 'metainfo')
LOCAL_CHANGES_PATH = os.path.join(ROOT_PATH, 'local_changes')
PREVIEWS_PATH = os.path.join(ROOT_PATH, 'previews')
THUMBNAILS_PATH = os.path.join(ROOT_PATH, 'thumbnails')
IMAGES_PATH = os.path.join(ROOT_PATH, 'images')
NEW_CONTENT_PATH = os.path.join(BASE_PATH, 'new_content')


SUPPORTED_EXTENSIONS = [
    'jpg',
]
THUMBNAIL_SIZE = (384, 384)
PREVIEW_SIZE = (1024, 1024)
