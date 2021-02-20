# -*- coding: utf-8 -*-

"""Main file.
"""
from common import utils_identity
from common import utils_filesystem
from register import settings
from register.media_type import Media


def main():
    """Entry point.
    """
    existing_uids = utils_filesystem.gen_known_uids(settings.ROOT_PATH)

    new_content_path = utils_filesystem.join(settings.ROOT_PATH, 'new_content')

    for path in utils_filesystem.iterate_over_new_content(
            new_content_path, settings.SUPPORTED_EXTENSIONS):
        uuid = utils_identity.get_new_uuid(existing_uids)

        media = Media(uuid, path)
        correct = media.analyze()
        if correct:
            media.register()
            media.delete_source_file()


if __name__ == '__main__':
    main()
