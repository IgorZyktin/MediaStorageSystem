# -*- coding: utf-8 -*-

"""Small helper functions for mss_browser.
"""
import configparser
import re
from argparse import Namespace
from collections import defaultdict
from typing import List, Dict

from colorama import Fore
from werkzeug.utils import redirect

from common import utils_filesystem, utils_common
from core.class_meta import Meta
from core.class_repository import Repository
from core.class_search_enhancer import SearchEnhancer
from core.class_serializer import DictSerializer

UUID4_PATTERN = re.compile(
    r'^[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}$'
)


def add_query_to_path(request):
    """Get query from form and add it to path.
    """
    url = '/'

    raw_query = request.form.get('query')
    if raw_query:
        url += 'search?q=' + raw_query

    return redirect(url)


def rewrite_query_for_paging(query: str, target_page: int) -> str:
    """Change query to generate different page.
    """
    return '/search?q=' + query + f'&page={target_page}'


def get_user_config(path: str) -> Namespace:
    """Get specific user settings.
    """
    config = configparser.ConfigParser()
    config.read(path)
    return Namespace(**dict(config['browser']))


def make_repository(user_config, settings) -> Repository:
    """Build repository instance.
    """
    raw_metarecords = utils_filesystem.load_jsons(
        user_config.metainfo_path,
        limit=settings.METARECORD_LOAD_LIMIT,
    )
    synonyms = get_synonyms(user_config.root_path)

    as_jsons = defaultdict(dict)
    for raw_record in raw_metarecords:
        uuid = raw_record['uuid']
        as_jsons[uuid].update(raw_record)

    repo = Repository()
    serializer = DictSerializer(target_type=Meta)
    enhancer = SearchEnhancer(synonyms=synonyms)

    for record in as_jsons.values():
        instance = serializer.from_source(**record)
        tags = enhancer.get_extended_tags(instance)
        repo.add_record(instance, tags)

    return repo


def run_local_server(app, user_config, settings) -> None:
    """Run server on local machine.
    """
    if settings.START_MESSAGE:
        utils_common.output(settings.START_MESSAGE, color=Fore.YELLOW)

    if user_config.new_tab_on_start:
        import threading
        import webbrowser
        tab_delay_sec = 2.0

        def _start():
            webbrowser.open_new_tab(
                f'http://{user_config.host}:{user_config.port}/'
            )

        new_thread = threading.Timer(tab_delay_sec, _start)
        new_thread.start()

    app.run(host=user_config.host, port=user_config.port, debug=settings.DEBUG)


def get_injection(path: str) -> str:
    """Get code that must be included into HTML rendering.

    Added for google analytics etc.
    """
    return utils_filesystem.load_textual_file(path)


def get_synonyms(folder: str,
                 filename: str = 'synonyms.json') -> Dict[str, List[str]]:
    """Get synonyms for the search machine.
    """
    return utils_filesystem.load_json(folder, filename)


def is_correct_uuid(uuid: str) -> bool:
    """Return True if this UUID is correct.
    """
    return UUID4_PATTERN.match(uuid.upper()) is not None
