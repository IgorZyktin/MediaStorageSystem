# -*- coding: utf-8 -*-

"""Script settings.
"""
import os

BASE_PATH = 'D:\\BGC_ARCHIVE_\\'
ROOT_PATH = os.path.join(BASE_PATH, 'root')
METAINFO_PATH = os.path.join(ROOT_PATH, 'metainfo')
LOCAL_CHANGES_PATH = os.path.join(ROOT_PATH, 'local_changes')
PREVIEWS_PATH = os.path.join(ROOT_PATH, 'previews')
THUMBNAILS_PATH = os.path.join(ROOT_PATH, 'thumbnails')
IMAGES_PATH = os.path.join(ROOT_PATH, 'images')
NEW_CONTENT_PATH = os.path.join(BASE_PATH, 'new_content')
TMP_PATH = 'tmp'

SUPPORTED_EXTENSIONS = [
    'jpg', 'jpeg', 'png'
]
THUMBNAIL_SIZE = (384, 384)
PREVIEW_SIZE = (1024, 1024)
TERMINAL_WIDTH = 79
