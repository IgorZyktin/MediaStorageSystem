# -*- coding: utf-8 -*-

"""Main file.
"""
import time

from colorama import init
from flask import Flask, render_template, request, send_from_directory, abort

from common import utils_text
from core import utils_core
from mss_browser import settings, search_engine, utils_browser
from mss_browser.class_paginator import Paginator
from mss_browser.class_search_request import SearchRequest

init()
user_config = utils_browser.get_user_config(settings.CONFIG_FILENAME)
injection = utils_browser.get_injection(settings.INJECTION_FILENAME)
repository = utils_browser.make_repository(user_config, settings)

app = Flask(__name__)


@app.context_processor
def common_names():
    """Populate context with common names.
    """
    return {
        'title': user_config.title,
        'note': '',
        'injection': injection,
        'rewrite_query_for_paging': utils_browser.rewrite_query_for_paging,
        'byte_count_to_text': utils_text.byte_count_to_text,
    }


@app.route('/root/<path:filename>')
def serve_content(filename: str):
    """Serve files from main storage.

    Contents of the main storage are served through this function.
    It's not about static css or js files.
    """
    return send_from_directory(user_config.root_path,
                               filename, conditional=True)


@app.route('/', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
def index():
    """Main page of the script.
    """
    if request.method == 'POST':
        return utils_browser.add_query_to_path(request)

    query = request.args.get('q', '')
    current_page = int(request.args.get('page', 1))
    start = time.perf_counter()

    if query:
        search_request = SearchRequest.from_query(query)
        chosen_metarecords = search_engine.select_images(
            repository=repository,
            search_request=search_request,
        )
    else:
        chosen_metarecords = search_engine.select_random_images(
            repository=repository,
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
    }
    return render_template('content.html', **context)


@app.route('/preview/<uuid>')
def preview(uuid: str):
    """Show description for a single record.
    """
    if not utils_browser.is_correct_uuid(uuid):
        abort(500)

    metarecord = repository.get(uuid)

    if metarecord is None:
        abort(404)

    if metarecord.group_name:
        note = f'This file seem to be part of "{metarecord.group_name}"'
    else:
        note = ''

    context = {
        'record': metarecord,
        'query': uuid,
        'note': note,
    }
    return render_template('preview.html', **context)


@app.route('/tags')
def show_tags():
    """Enlist all available tags with their frequencies.
    """
    stats = utils_core.calculate_statistics(repository)
    context = {
        'stats': stats,
        'tags': utils_core.sort_tags(stats['tags_stats']),
    }
    return render_template('tags.html', **context)


@app.route('/help')
def show_help():
    """Show description page.
    """
    context = {
        'note': f'Current version of the MSS browser: {settings.VERSION}',
    }
    return render_template('help.html', **context)


if __name__ == '__main__':
    utils_browser.run_local_server(app, user_config, settings)
