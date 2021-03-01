# -*- coding: utf-8 -*-

"""Main file.
"""
import time

from flask import Flask, render_template, request, send_from_directory, abort

from common import utils_filesystem, utils_text, utils_interaction
from mss_browser import settings, search_engine, utils_browser
from mss_browser.paginator_class import Paginator

app = Flask(__name__)
jsons = utils_filesystem.load_jsons(
    settings.METAINFO_PATH,
    settings.LOCAL_CHANGES_PATH,
    limit=settings.METARECORD_LOAD_LIMIT,
)
SYNONYMS = utils_filesystem.load_synonyms(settings.ROOT_PATH)

REPO = utils_browser.make_repository(
    raw_metarecords=jsons,
    synonyms=SYNONYMS,
)

# TAG_STATS = utils_browser.calculate_stats_for_tags(metainfo)
# TOTAL = utils_text.sep_digits(len(metainfo))
# TOTAL_TAGS = utils_text.sep_digits(len(TAG_STATS))
# TOTAL_BYTES = sum(x.parameters.size for x in metainfo.values())
# TOTAL_SIZE = utils_text.byte_count_to_text(TOTAL_BYTES)
# MAX_DATE = max(x.registration.registered_at for x in metainfo.values())

CONFIG = utils_browser.get_local_config(
    path=settings.BASE_PATH,
    base_config=settings.BASE_CONFIG,
)

# for record in metainfo.values():
#     new_tags = utils_browser.extend_tags_with_synonyms(
#         given_tags=record.extended_tags_set,
#         given_synonyms=SYNONYMS,
#     )
#     record.extended_tags_with_synonyms = new_tags


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
            metainfo=metainfo,
            searching_machine=searching_machine,
        )
    else:
        chosen_metarecords = search_engine.select_random_images(
            metainfo=metainfo,
            items_per_page=settings.ITEMS_PER_PAGE,
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
        'title': 'MSS',
        'paginator': paginator,
        'query': query,
        'note': note,
        'rewrite_query_for_paging': utils_browser.rewrite_query_for_paging,
    }
    return render_template('content.html', **context)


@app.route('/preview/<uuid>')
def preview(uuid: str):
    """Show description for a single record.
    """
    metarecord = metainfo.get(uuid)

    if metarecord is None:
        abort(404)

    group_id = metarecord.meta.group_id
    if group_id:
        note = f'This file seem to be part of something called "{group_id}"'
    else:
        note = ''

    context = {
        'title': 'MSS',
        'metarecord': metarecord,
        'query': uuid,
        'note': note,
        'byte_count_to_text': utils_text.byte_count_to_text
    }
    return render_template('preview.html', **context)


@app.route('/tags')
def show_tags():
    """Enlist all available tags with their frequencies.
    """
    context = {
        'title': 'MSS',
        'tags': TAG_STATS,
        'note': f'Total records in catalogue: {TOTAL}',
        'total_tags_num': TOTAL_TAGS,
        'total_size': TOTAL_SIZE,
    }
    return render_template('tags.html', **context)


@app.route('/help')
def show_help():
    """Show description page.
    """
    context = {
        'title': 'MSS',
        'note': f'Current version of the browser: {settings.VERSION}',
    }
    return render_template('help.html', **context)


if __name__ == '__main__':
    if CONFIG.run_on_localhost:
        host = utils_interaction.get_local_ip()
    else:
        host = settings.HOST

    port = settings.PORT

    if CONFIG.app_config == 'production' and CONFIG.new_tab_on_start:
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
