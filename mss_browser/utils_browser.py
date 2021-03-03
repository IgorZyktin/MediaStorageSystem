# -*- coding: utf-8 -*-

"""Small helper functions for mss_browser.
"""
import configparser
from argparse import Namespace
from collections import defaultdict
from typing import List

from werkzeug.utils import redirect

from core.class_meta import Meta
from core.class_repository import Repository
from core.class_search_enhancer import SearchEnhancer
from core.class_serializer import DictSerializer


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
    # TODO - this will stop working when search filtering will be introduced :(
    if not query and target_page:
        return '/new?q=' + query + f'&page={target_page}'
    return '/search?q=' + query + f'&page={target_page}'


def get_user_config(path: str) -> Namespace:
    """Get specific user settings.
    """
    config = configparser.ConfigParser()
    config.read(path)
    return Namespace(**dict(config['browser']))


def make_repository(raw_metarecords: List[dict],
                    synonyms: dict) -> Repository:
    """Build repository instance.
    """
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


def run_local_server(app, user_config, debug: bool) -> None:
    """Run server on local machine.
    """
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

    app.run(host=user_config.host, port=user_config.port, debug=debug)


def get_injection(path: str) -> str:
    """Get code that must be included into HTML rendering.

    Added for google analytics etc.
    """
    try:
        with open(path, mode='r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        content = ''
    return content
