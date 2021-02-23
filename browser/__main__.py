# -*- coding: utf-8 -*-

"""Main file.
"""
import time

from flask import Flask, render_template, request, send_from_directory, abort

from browser import settings, search_engine, utils_browser
from browser.paginator_class import Paginator
from common import utils_filesystem, utils_text

app = Flask(__name__)
metainfo = utils_filesystem.get_metarecords(
    settings.METAINFO_PATH,
    settings.LOCAL_CHANGES_PATH,
    limit=settings.METARECORD_LOAD_LIMIT,
)
SYNONYMS = utils_filesystem.load_synonyms(settings.ROOT_PATH)
TAG_STATS = utils_browser.calculate_stats_for_tags(metainfo)
TOTAL = utils_text.sep_digits(len(metainfo))
TOTAL_TAGS = utils_text.sep_digits(len(TAG_STATS))
TOTAL_BYTES = sum(x.parameters.size for x in metainfo.values())
TOTAL_SIZE = utils_text.byte_count_to_text(TOTAL_BYTES)


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
        return utils_browser.add_query(request)

    query = request.args.get('q', '')
    current_page = int(request.args.get('page', 1))
    start = time.perf_counter()

    if query:
        searching_machine = search_engine.make_searching_machine(query)
        chosen_metarecords = search_engine.select_images(
            metainfo=metainfo,
            searching_machine=searching_machine,
            synonyms=SYNONYMS,
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

    context = {
        'title': 'Index',
        'paginator': paginator,
        'found_records_num': utils_text.sep_digits(len(paginator)),
        'duration': '{:0.4f}'.format(time.perf_counter() - start),
        'query': query,
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

    context = {
        'title': f'Preview for {uuid}',
        'metarecord': metarecord,
        'byte_count_to_text': utils_text.byte_count_to_text
    }
    return render_template('preview.html', **context)


@app.route('/tags')
def show_tags():
    """Enlist all available tags with their frequencies.
    """
    context = {
        'title': 'All tags',
        'tags': TAG_STATS,
        'total_records_num': TOTAL,
        'total_tags_num': TOTAL_TAGS,
        'total_size': TOTAL_SIZE,
    }
    return render_template('tags.html', **context)


@app.route('/help')
def show_help():
    """Show description page.
    """
    context = {
        'title': 'Help',
        'version': settings.VERSION,
    }
    return render_template('help.html', **context)


if __name__ == '__main__':
    app.run(debug=settings.DEBUG)
