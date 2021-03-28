import os
from typing import Tuple

import requests


def cut_arguments(url: str) -> str:
    """Delete query arguments from the link.
    """
    mark = url.find('?')

    if mark != -1:
        url = url[:mark]

    return url


def download_file(url: str, target_folder: str) -> Tuple[str, str]:
    """Download file from given url and save it to a given folder.
    """
    response = requests.get(url)

    url = cut_arguments(url)
    filename = url.rsplit('/', 1)[1]
    content = response.content

    ext = ''
    if '.' not in filename:
        # content_type = response.headers.get('content-type')
        #
        # if content_type == ('Content-Type', 'image/jpe'):
        #     ext = '.jpe'
        #
        # elif content_type == ('Content-Type', 'image/jpeg'):
        ext = '.jpeg'

    filename += ext

    path = os.path.join(target_folder, filename)

    with open(path, mode='wb') as file:
        file.write(content)

    print('File downloaded', filename[:50])

    return path, filename
