"""Serve a local BOF checkout without flooding the terminal with asset requests."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
import sys


class AssetHandler(SimpleHTTPRequestHandler):
    def log_request(self, code='-', size='-'):
        # Cold loads fetch hundreds of atlas/audio files. Keep real HTTP errors
        # visible, while avoiding terminal backpressure on successful requests.
        if isinstance(code, int) and code >= 400:
            super().log_request(code, size)


class AssetServer(ThreadingHTTPServer):
    # Browser tabs can request several asset banks at once. The stdlib default
    # backlog of five may reject a new connection before a worker accepts it.
    request_queue_size = 128
    daemon_threads = True

    def handle_error(self, request, client_address):
        # Closing/reloading a tab cancels image and audio transfers normally.
        if isinstance(sys.exc_info()[1], (BrokenPipeError, ConnectionResetError, ConnectionAbortedError)):
            return
        super().handle_error(request, client_address)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('port', type=int, nargs='?', default=8767)
    parser.add_argument('--directory', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error('port must be between 1 and 65535')
    root = args.directory.resolve()
    if not (root / 'index.html').is_file():
        parser.error('directory must contain the BOF index.html')
    handler = partial(AssetHandler, directory=str(root))
    with AssetServer(('127.0.0.1', args.port), handler) as server:
        print(f'BOF local server: http://127.0.0.1:{args.port}/  ({root})', flush=True)
        try:
            server.serve_forever(poll_interval=.1)
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
