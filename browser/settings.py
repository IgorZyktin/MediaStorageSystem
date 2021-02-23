# -*- coding: utf-8 -*-

"""Script settings.
"""
import os

VERSION = '1.1'

# paths
# BASE_PATH = '.'
BASE_PATH = 'D:\\BGC_ARCHIVE\\'
ROOT_PATH = os.path.join(BASE_PATH, 'root')
METAINFO_PATH = os.path.join(ROOT_PATH, 'metainfo')
LOCAL_CHANGES_PATH = os.path.join(ROOT_PATH, 'local_changes')
PREVIEWS_PATH = os.path.join(ROOT_PATH, 'previews')
THUMBNAILS_PATH = os.path.join(ROOT_PATH, 'thumbnails')
IMAGES_PATH = os.path.join(ROOT_PATH, 'images')

# only needed during testing in development
METARECORD_LOAD_LIMIT = -1  # -1 for no limit

ITEMS_PER_PAGE = 50
DEBUG = True
