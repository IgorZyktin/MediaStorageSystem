# -*- coding: utf-8 -*-

"""Small helper functions for mss_browser.
"""
import re

from werkzeug.utils import redirect

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


def run_local_server(app, config) -> None:
    """Run server on local machine.
    """
    if config.new_tab_on_start == 'yes':
        import threading
        import webbrowser
        tab_delay_sec = 2.0

        def _start():
            webbrowser.open_new_tab(
                f'http://{config.host}:{config.port}/'
            )

        new_thread = threading.Timer(tab_delay_sec, _start)
        new_thread.start()

    app.run(host=config.host, port=config.port, debug=config.debug == 'yes')


def is_correct_uuid(uuid: str) -> bool:
    """Return True if this UUID is correct.
    """
    if len(uuid) != CORRECT_UUID_LENGTH:
        return False
    return UUID4_PATTERN.match(uuid.upper()) is not None
