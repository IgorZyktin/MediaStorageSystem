# -*- coding: utf-8 -*-

"""Script settings.
"""
import os

VERSION = '1.2'

HOST = '192.168.1.64'
PORT = 5000

APP_CONFIG = 'development'
# APP_CONFIG = 'production'

if APP_CONFIG == 'development':
    BASE_PATH = 'D:\\BGC_ARCHIVE\\'
    DEBUG = True
else:
    BASE_PATH = '.'
    DEBUG = False

ROOT_PATH = os.path.join(BASE_PATH, 'root')
METAINFO_PATH = os.path.join(ROOT_PATH, 'metainfo')
LOCAL_CHANGES_PATH = os.path.join(ROOT_PATH, 'local_changes', 'metainfo')
PREVIEWS_PATH = os.path.join(ROOT_PATH, 'previews')
THUMBNAILS_PATH = os.path.join(ROOT_PATH, 'thumbnails')
IMAGES_PATH = os.path.join(ROOT_PATH, 'images')

# only needed during testing in development
METARECORD_LOAD_LIMIT = -1  # -1 for no limit

ITEMS_PER_PAGE = 50

BASE_CONFIG = {
    'app_config': APP_CONFIG,
    'run_on_localhost': True,
    'host': HOST,
    'port': PORT,
    'items_per_page': ITEMS_PER_PAGE,
    'new_tab_on_start': True,
}
