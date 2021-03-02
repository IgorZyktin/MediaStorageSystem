# -*- coding: utf-8 -*-

"""Small helper functions for mss_browser.
"""
from argparse import Namespace
from collections import defaultdict
from typing import List, Tuple, Set, Dict

from werkzeug.utils import redirect

from common import utils_filesystem
from common.metarecord_class import Metainfo
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


def calculate_stats_for_tags(metainfo: Metainfo,
                             reverse: bool = True) -> List[Tuple[str, int]]:
    """Calculate statistics on tags usage.

    Example output:
        [('magazine', 398), ('artbook', 254), ('artwork', 123)]
    """
    raw_tags = defaultdict(int)

    for metarecord in metainfo.values():
        for tag in metarecord.tags_set:
            raw_tags[tag.lower()] += 1

    stats = list(raw_tags.items())
    stats.sort(key=lambda x: x[1], reverse=reverse)

    return stats


def extend_tags_with_synonyms(given_tags: Set[str],
                              given_synonyms: Dict[str, List[str]]
                              ) -> Set[str]:
    """Mutate given tags by adding synonyms to them.
    """
    sets = [set(x) for x in given_synonyms.values()]

    resulting_tags = set()

    for tag in list(given_tags):
        resulting_tags.add(tag)

        for entry in sets:
            if tag in entry:
                resulting_tags.update(entry)

    return resulting_tags


def get_local_config(path: str, base_config: dict,
                     filename: str = 'config.json') -> Namespace:
    """Make configuration for the browser.
    """
    local_config = utils_filesystem.load_synonyms(path, filename)

    config = {
        **base_config,
        **local_config,
    }
    return Namespace(**config)


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
