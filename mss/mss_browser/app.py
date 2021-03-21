# -*- coding: utf-8 -*-

"""Main file.
"""
import time

from flask import (
    Flask, render_template, request, send_from_directory, abort,
    redirect, url_for,
)

import mss.core.configuration
from mss import constants
from mss.core import utils_core
from mss.core.class_repository import Repository
from mss.core.configuration import Config
from mss.core.file_handling import (
    load_all_themes, update_one_theme, make_default_theme,
)
from mss.core.helper_types.class_filesystem import Filesystem
from mss.mss_browser import search_engine, utils_browser
from mss.mss_browser.class_paginator import Paginator
from mss.mss_browser.class_search_request import SearchRequest
from mss.utils import utils_text

config = Config(root_path='', title='', injection='', themes=[])
repository = Repository()

app = Flask(__name__)


def _get_theme(directory: str):
    for theme in config.themes:
        if theme.directory == directory:
            return theme
    else:
        abort(404)


@app.context_processor
def common_names():
    """Populate context with common names."""
    return {
        'title': config.title,
        'note': '',
        'injection': config.injection,
        'rewrite_query_for_paging': utils_browser.rewrite_query_for_paging,
        'byte_count_to_text': utils_text.byte_count_to_text,
    }


@app.route('/content/<path:filename>')
def serve_content(filename: str):
    """Serve files from main storage.

    Contents of the main storage are served through this function.
    It's not about static css or js files.
    """
    return send_from_directory(config.root_path, filename, conditional=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    """Entry page.

    Redirects user to path with default directory.
    """
    return redirect(url_for('index_all', directory=constants.ALL_THEMES))


@app.route('/index/<directory>/', methods=['GET', 'POST'])
@app.route('/index/<directory>/search', methods=['GET', 'POST'])
def index_all(directory: str):
    """Main page of the script."""
    if request.method == 'POST':
        return utils_browser.add_query_to_path(request, directory)

    query = request.args.get('q', '')
    current_page = int(request.args.get('page', 1))
    start = time.perf_counter()
    theme = _get_theme(directory)

    if query:
        search_request = SearchRequest.from_query(query, directory)
        chosen_metarecords = search_engine.select_records(
            theme=theme,
            repository=repository,
            search_request=search_request,
        )
        prefix = ''
    else:
        chosen_metarecords = utils_core.select_random_records(
            theme=theme,
            repository=repository,
            amount=int(user_config.items_per_page),
        )
        prefix = 'Random'

    paginator = Paginator(
        sequence=chosen_metarecords,
        current_page=current_page,
        items_per_page=int(user_config.items_per_page),
    )

    total = utils_text.sep_digits(len(paginator))
    duration = '{:0.4f}'.format(time.perf_counter() - start)
    note = f'{prefix} {total} records found in {duration} seconds'

    if theme.directory == constants.ALL_THEMES:
        placeholder = ''
    else:
        placeholder = f'Search on theme "{theme.name}"'

    context = {
        'paginator': paginator,
        'query': query,
        'note': note,
        'directory': directory,
        'placeholder': placeholder,
    }
    return render_template('content.html', **context)


@app.route('/preview/<directory>/<uuid>')
def preview(directory: str, uuid: str):
    """Show description for a single record.
    """
    if not utils_browser.is_correct_uuid(uuid):
        abort(404)

    record = repository.get_record(uuid)

    if record is None:
        abort(404)

    if record.group_name:
        note = f'This file seem to be part of "{record.group_name}"'
    else:
        note = ''

    query = request.args.get('q', '')

    theme = _get_theme(directory)
    if theme.directory == constants.ALL_THEMES:
        placeholder = ''
    else:
        placeholder = f'Search on theme "{theme.name}"'

    context = {
        'record': record,
        'query': query,
        'note': note,
        'directory': directory,
        'placeholder': placeholder,
    }
    return render_template('preview.html', **context)


@app.route('/tags/<directory>/')
def show_tags(directory: str):
    """Enlist all available tags with their frequencies."""
    # FIXME
    theme = _get_theme(directory)
    if theme.directory == constants.ALL_THEMES:
        placeholder = ''
    else:
        placeholder = f'Search on theme "{theme.name}"'

    context = {
        'directory': directory,
        'current_theme': theme,
        'statistics': theme.statistics,
        'all_themes': config.themes,
        'placeholder': placeholder,
    }
    return render_template('tags.html', **context)


@app.route('/help/<directory>/')
def show_help(directory: str):
    """Show help page."""
    # FIXME
    theme = _get_theme(directory)
    if theme.directory == constants.ALL_THEMES:
        placeholder = ''
    else:
        placeholder = f'Search on theme "{theme.name}"'

    context = {
        'note': f'Current version: {constants.__version__}',
        'directory': directory,
        'placeholder': placeholder,
    }
    return render_template('help.html', **context)


@app.errorhandler(404)
def page_not_found(e):
    """Return not found page."""
    context = {
        'directory': constants.ALL_THEMES,
    }
    return render_template('404.html', **context), 404


if __name__ == '__main__':
    print(constants.START_MESSAGE)

    user_config = mss.core.configuration.get_user_config('config.ini')
    config.title = user_config.title

    filesystem = Filesystem()
    config.root_path = filesystem.absolute(user_config.root_path)

    if user_config.inject_code == 'yes':
        config.injection = filesystem.read_file('injection.html')

    themes = load_all_themes(config.root_path, filesystem)

    for _theme in themes:
        update_one_theme(config.root_path, _theme, repository, filesystem)

    make_default_theme(themes)
    config.themes = themes
    utils_browser.run_local_server(app, user_config)
