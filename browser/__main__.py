# -*- coding: utf-8 -*-

"""Main file.
"""

from flask import Flask, render_template, request, send_from_directory, abort

from browser import settings, search_engine, utils_browser
from browser.paginator_class import Paginator
from common import utils_filesystem

app = Flask(__name__)
metainfo = utils_filesystem.get_metarecords(
    settings.METAINFO_PATH,
    settings.LOCAL_CHANGES_PATH,
    limit=settings.METARECORD_LOAD_LIMIT,
)
TOTAL = len(metainfo)


@app.route('/root/<path:filename>')
def serve_static(filename: str):
    """Serve static files from main storage.
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
    page = int(request.args.get('page', 1))

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
        current_page=page,
        items_per_page=settings.ITEMS_PER_PAGE,
    )

    context = {
        'version': settings.VERSION,
        'title': 'Starting page',
        'paginator': paginator,
        'total_records_num': TOTAL,
        'found_records_num': len(paginator),
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
        'version': settings.VERSION,
        'title': f'Preview for {uuid}',
        'metarecord': metarecord,
    }
    return render_template('preview.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
