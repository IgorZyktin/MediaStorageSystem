import os

from PIL import Image

from register import settings

folder = 'D:\\BGC_ARCHIVE\\root\\thumbnails'

for path, dirs, files in os.walk(folder):
    for file in files:
        full_path = os.path.join(path, file)
        image = Image.open(full_path)
        image.thumbnail(settings.THUMBNAIL_SIZE)
        image.save(full_path)
        print(file)
