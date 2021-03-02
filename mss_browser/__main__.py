# -*- coding: utf-8 -*-

"""Main file.
"""
import time

from flask import Flask, render_template, request, send_from_directory, abort

from common import utils_filesystem, utils_text
from core import utils_core
from mss_browser import settings, search_engine, utils_browser
from mss_browser.paginator_class import Paginator

app = Flask(__name__)
jsons = utils_filesystem.load_jsons(
    settings.METAINFO_PATH,
    settings.LOCAL_CHANGES_PATH,
    limit=settings.METARECORD_LOAD_LIMIT,
)
synonyms = utils_filesystem.load_synonyms(settings.ROOT_PATH)

repository = utils_browser.make_repository(
    raw_metarecords=jsons,
    synonyms=synonyms,
)

config = utils_browser.get_local_config(
    path=settings.BASE_PATH,
    base_config=settings.BASE_CONFIG,
)


@app.context_processor
def common_names():
    """Populate context with common names.
    """
    return {
        'title': 'MediaStorageSystem',
        'note': '',
        'rewrite_query_for_paging': utils_browser.rewrite_query_for_paging,
        'byte_count_to_text': utils_text.byte_count_to_text,
    }


@app.route('/root/<path:filename>')
def serve_static(filename: str):
    """Serve static files from main storage.

    Contents of the main storage are served through this function.
    It's not about static css or js files.
    """
    return send_from_directory(settings.ROOT_PATH, filename, conditional=True)


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
        searching_machine = search_engine.make_searching_machine(query)
        chosen_metarecords = search_engine.select_images(
            repository=repository,
            searching_machine=searching_machine,
        )
    else:
        chosen_metarecords = search_engine.select_random_images(
            repository=repository,
            amount=settings.ITEMS_PER_PAGE,
        )

    paginator = Paginator(
        sequence=chosen_metarecords,
        current_page=current_page,
        items_per_page=settings.ITEMS_PER_PAGE,
    )

    records = utils_text.sep_digits(len(paginator))
    duration = '{:0.4f}'.format(time.perf_counter() - start)
    note = f'{records} records found in {duration} seconds'

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
    metarecord = repository.get(uuid)

    if metarecord is None:
        abort(404)

    note = ''
    if metarecord.group_name:
        note = f'This file seem to be part of "{metarecord.group_name}"'

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
    tags = sorted(stats['tags_stats'].items(),
                  key=lambda x: x[1], reverse=True)
    context = {
        'tags': tags,
        'stats': stats,
    }
    return render_template('tags.html', **context)


@app.route('/help')
def show_help():
    """Show description page.
    """
    context = {
        'note': f'Current version of the browser: {settings.VERSION}',
    }
    return render_template('help.html', **context)


if __name__ == '__main__':
    # if CONFIG.run_on_localhost:
    #     host = utils_interaction.get_local_ip()
    # else:
    host = settings.HOST

    port = settings.PORT

    if True:
        import threading


        def _start():
            import webbrowser
            webbrowser.open_new_tab(f'http://{host}:{port}/')


        new_thread = threading.Timer(2.0, _start)
        new_thread.start()

    app.run(
        host=host,
        port=port,
        debug=settings.DEBUG,
    )
