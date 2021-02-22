# -*- coding: utf-8 -*-

"""Small helper functions for browser.
"""
from werkzeug.utils import redirect


def add_query(request):
    """Get query from form and add it to path.
    """
    url = '/'

    if 'clear' in request.form:
        return redirect(url)

    if 'tags' in request.form:
        return redirect('/tags')

    raw_query = request.form.get('query')
    if raw_query:
        url += 'search?q=' + raw_query

    return redirect(url)


def rewrite_query_for_paging(query: str, target_page: int) -> str:
    """Change query to generate different page.
    """
    return '/search?q=' + query + f'&page={target_page}'
