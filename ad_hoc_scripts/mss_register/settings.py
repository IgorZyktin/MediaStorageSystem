# -*- coding: utf-8 -*-

"""Script settings.
"""
import os

APP_CONFIG = 'development'
# APP_CONFIG = 'production'

if APP_CONFIG == 'development':
    BASE_PATH = 'D:\\BGC_ARCHIVE_\\'
    DEBUG = True
else:
    BASE_PATH = ''
    DEBUG = False


SUPPORTED_EXTENSIONS = [
    'jpg', 'jpeg', 'png'
]
THUMBNAIL_SIZE = (384, 384)
PREVIEW_SIZE = (1024, 1024)
