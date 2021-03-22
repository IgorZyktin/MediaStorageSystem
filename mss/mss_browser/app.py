# -*- coding: utf-8 -*-

"""Main file.
"""
import time

from flask import (
    Flask, render_template, request, send_from_directory, abort,
    redirect, url_for,
)

import mss.core.utils_core
from mss import constants
from mss.core import utils_core, configuration, simple_types, concrete_types
from mss.core.file_handling import update_repositories
from mss.core.helper_types.class_filesystem import Filesystem
from mss.mss_browser import utils_browser
from mss.mss_browser.class_paginator import Paginator
from mss.utils import utils_text

filesystem = Filesystem()
config = configuration.get_config(filesystem)
query_builder = concrete_types.QueryBuilder(target_type=simple_types.Query)
repository = concrete_types.Repository()
theme_repository = simple_types.ThemeRepository()
update_repositories(theme_repository, repository, config.root_path, filesystem)

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

    start = time.perf_counter()
    query_text = request.args.get('q', '')
    current_page = int(request.args.get('page', 1))
    current_theme = theme_repository.get(directory) or abort(404)
    query = query_builder.from_query(query_text, directory)

    if query:
        chosen_metarecords = mss.core.utils_core.select_records(
            theme=current_theme,
            repository=repository,
            query=query,
        )
    else:
        chosen_metarecords = utils_core.select_random_records(
            theme=current_theme,
            repository=repository,
            amount=config.items_per_page,
        )

    paginator = Paginator(
        sequence=chosen_metarecords,
        current_page=current_page,
        items_per_page=config.items_per_page,
    )

    note = utils_browser.get_note_on_search(len(paginator),
                                            time.perf_counter() - start)
    context = {
        'paginator': paginator,
        'query': query_text,
        'note': note,
        'directory': directory,
        'placeholder': utils_browser.get_placeholder(current_theme),
    }
    return render_template('content.html', **context)


@app.route('/preview/<directory>/<uuid>')
def preview(directory: str, uuid: str):
    """Show description for a single record."""
    _ = utils_browser.is_correct_uuid(uuid) or abort(404)
    meta = repository.get_record(uuid) or abort(404)
    current_theme = theme_repository.get(directory) or abort(404)
    query_text = request.args.get('q', '')

    context = {
        'meta': meta,
        'query': query_text,
        'note': utils_browser.get_group_name(meta),
        'directory': directory,
        'placeholder': utils_browser.get_placeholder(current_theme),
    }
    return render_template('preview.html', **context)


@app.route('/tags/<directory>/')
def show_tags(directory: str):
    """Enlist all available tags with their frequencies."""
    current_theme = theme_repository.get(directory) or abort(404)

    context = {
        'directory': directory,
        'current_theme': current_theme,
        'statistics': current_theme.statistics,
        'theme_repository': theme_repository,
        'placeholder': utils_browser.get_placeholder(current_theme),
    }
    return render_template('tags.html', **context)


@app.route('/help/<directory>/')
def show_help(directory: str):
    """Show help page."""
    current_theme = theme_repository.get(directory) or abort(404)

    context = {
        'note': f'Current version: {constants.__version__}',
        'directory': directory,
        'placeholder': utils_browser.get_placeholder(current_theme),
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
    app.run(host=config.host, port=config.port, debug=config.debug)
