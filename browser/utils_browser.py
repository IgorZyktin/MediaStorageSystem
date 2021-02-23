# -*- coding: utf-8 -*-

"""Small helper functions for browser.
"""
from collections import defaultdict
from typing import List, Tuple, Set, Dict

from werkzeug.utils import redirect

from common.metarecord_class import Metainfo


def add_query(request):
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
