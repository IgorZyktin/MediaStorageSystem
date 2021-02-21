# -*- coding: utf-8 -*-

"""Main file.
"""
from flask import Flask, render_template, request, redirect, \
    send_from_directory

from browser import settings, search_engine
from common import utils_filesystem

app = Flask(__name__)
metainfo = utils_filesystem.get_all_metainfo(settings.ROOT_PATH)


@app.route('/root/<path:filename>')
def wellKnownRoute(filename):
    return send_from_directory(settings.ROOT_PATH, filename, conditional=True)


@app.route('/', methods=['GET', 'POST'])
@app.route('/search', methods=['GET', 'POST'])
def index():
    """Main page of the script.
    """
    if request.method == 'POST':
        raw_query = request.form.get('query')
        if raw_query:
            url = '/search?q=' + raw_query
        else:
            url = '/'
        return redirect(url)

    query = request.args.get('q', '')
    finder = search_engine.build_query(query)
    found, images = search_engine.select_images(metainfo, finder,
                                         settings.IMAGES_AT_ONCE)

    context = {
        'title': 'Index',
        'images': images,
        'total': len(metainfo),
        'found': found,
        # 'query': finder.get_query(),
        'query': query,

    }
    return render_template('content.html', **context)


@app.route('/preview/<uuid>')
def preview(uuid: str):
    context = {
        'title': 'Index',
        'total': len(metainfo),
        'uuid': uuid,
        'preview': metainfo[uuid].content_info.preview_path.replace('\\', '/'),
        'content': metainfo[uuid].content_info.content_path.replace('\\', '/'),
    }
    return render_template('preview.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
