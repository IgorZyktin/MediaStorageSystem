# -*- coding: utf-8 -*-

"""Small helper functions for mss_browser.
"""
import re

from werkzeug.utils import redirect

from mss import constants, core
from mss.utils.utils_text import sep_digits

CORRECT_UUID_LENGTH = 36
UUID4_PATTERN = re.compile(
    r'^[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}$'
)


def add_query_to_path(request, directory: str):
    """Get query from form and add it to path."""
    url = f'/index/{directory}/'

    raw_query = request.form.get('query')
    if raw_query:
        url += 'search?q=' + raw_query

    return redirect(url)


def rewrite_query_for_paging(directory: str, query: str,
                             target_page: int) -> str:
    """Change query to generate different page."""
    return f'/index/{directory}/search?q=' + query + f'&page={target_page}'


def is_correct_uuid(uuid: str) -> bool:
    """Return True if this UUID is correct."""
    if len(uuid) != CORRECT_UUID_LENGTH:
        return False
    return UUID4_PATTERN.match(uuid.upper()) is not None


def get_placeholder(current_theme: core.Theme) -> str:
    """Return specific placeholder if we're not in default theme."""
    if current_theme.directory != constants.ALL_THEMES:
        return f'Search on theme "{current_theme.name}"'
    return ''


def get_group_name(record: core.Meta) -> str:
    """Return specific group name if we have one."""
    if record.group_name:
        return f'This file is from group "{record.group_name}"'
    return ''


def get_note_on_search(total: int, duration: float) -> str:
    """Return description of search duration."""
    _total = sep_digits(total)
    _duration = '{:0.4f}'.format(duration)
    return f'Found {_total} records in {_duration} seconds'
