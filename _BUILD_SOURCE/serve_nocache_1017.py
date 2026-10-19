#!/usr/bin/env python3
"""serve_nocache_1017.py PORT - the PLAY launcher's local server, with caching switched off.

`python -m http.server` sends no Cache-Control, so a browser may keep serving yesterday's index.html and
scripts from its heuristic cache after the game is updated - the update then looks like it did nothing.
Every response here says no-store. Same directory, same bind address as before."""
import sys, functools, http.server
class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache'); self.send_header('Expires', '0')
        super().end_headers()
    def log_message(self, *a): pass
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
http.server.ThreadingHTTPServer(('127.0.0.1', port), functools.partial(NoCache, directory='.')).serve_forever()
