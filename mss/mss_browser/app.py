# -*- coding: utf-8 -*-

"""Main file.
"""
import time

from flask import Flask, render_template, request, send_from_directory, abort, \
    redirect, url_for

import mss.core.configuration
from mss import constants
from mss.core import utils_core
from mss.core.class_repository import Repository
from mss.core.configuration import Config
from mss.core.file_handling import load_all_themes, update_one_theme, \
    make_default_theme
from mss.core.helper_types.class_filesystem import Filesystem
from mss.mss_browser import search_engine, utils_browser
from mss.mss_browser.class_paginator import Paginator
from mss.mss_browser.class_search_request import SearchRequest
from mss.utils import utils_text

config = Config(root_path='', title='', injection='', version='', themes=[])
repository = Repository()

app = Flask(__name__)


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
    """Entry page."""
    return redirect(url_for('index_all', directory='all_themes'))


@app.route('/index/<directory>/', methods=['GET', 'POST'])
@app.route('/index/<directory>/search', methods=['GET', 'POST'])
def index_all(directory: str):
    """Main page of the script."""
    if request.method == 'POST':
        return utils_browser.add_query_to_path(request, directory)

    query = request.args.get('q', '')
    current_page = int(request.args.get('page', 1))
    start = time.perf_counter()

    if query:
        search_request = SearchRequest.from_query(query)
        if directory != 'all_themes':
            search_request.only_theme = directory

        chosen_metarecords = search_engine.select_records(
            repository=repository,
            search_request=search_request,
        )
    else:
        chosen_metarecords = utils_core.select_random_records(
            repository=repository,
            directory=directory,
            amount=int(user_config.items_per_page),
        )

    paginator = Paginator(
        sequence=chosen_metarecords,
        current_page=current_page,
        items_per_page=int(user_config.items_per_page),
    )

    total = utils_text.sep_digits(len(paginator))
    duration = '{:0.4f}'.format(time.perf_counter() - start)
    note = f'{total} records found in {duration} seconds'

    context = {
        'paginator': paginator,
        'query': query,
        'note': note,
        'directory': directory,
    }
    return render_template('content.html', **context)


@app.route('/preview/<directory>/<uuid>')
def preview(directory: str, uuid: str):
    """Show description for a single record.
    """
    if not utils_browser.is_correct_uuid(uuid):
        abort(400)

    metarecord = repository.get_record(uuid)

    if metarecord is None:
        abort(404)

    if metarecord.group_name:
        note = f'This file seem to be part of "{metarecord.group_name}"'
    else:
        note = ''

    query = request.args.get('q', '')

    context = {
        'record': metarecord,
        'query': query,
        'note': note,
        'directory': directory,
    }
    return render_template('preview.html', **context)


@app.route('/tags/<directory>/')
def show_tags(directory: str):
    """Enlist all available tags with their frequencies."""
    # FIXME
    theme_inst = config.themes[0]
    for theme_inst in config.themes:
        if theme_inst.directory == directory:
            break
    else:
        abort(404)

    context = {
        'directory': directory,
        'current_theme': theme_inst,
        'statistics': theme_inst.statistics,
        'all_themes': config.themes,
    }
    return render_template('tags.html', **context)


@app.route('/help/<directory>/')
def show_help(directory: str):
    """Show description page."""
    return render_template('help.html',
                           note=f'Current version: {config.version}',
                           directory=directory)


if __name__ == '__main__':
    print(constants.START_MESSAGE)

    user_config = mss.core.configuration.get_user_config('config.ini')
    config.title = user_config.title
    config.version = constants.__version__

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
