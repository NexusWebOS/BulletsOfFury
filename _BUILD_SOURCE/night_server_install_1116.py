from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'_BUILD_SOURCE/serve_nocache_1017.py';raw=p.read_bytes();S=R/'_ART_SOURCES/cinema_overnight_1116';backup=S/'serve_nocache_1017.py.before'
if not backup.exists():backup.write_bytes(raw)
nl='\r\n'if b'\r\n'in raw else'\n';s=raw.decode('utf8').replace('\r\n','\n')
if 'class BofNoCacheServer'not in s:
 s=s.replace('class NoCache(http.server.SimpleHTTPRequestHandler):','class NoCache(http.server.SimpleHTTPRequestHandler):\n    protocol_version = "HTTP/1.1"')
 at=s.index('port = int(sys.argv[1])')
 s=s[:at]+'''class BofNoCacheServer(http.server.ThreadingHTTPServer):
    # A campaign cold-load queues hundreds of authored sheets/scripts. The
    # default five-connection backlog can refuse speculative browser requests.
    request_queue_size = 256
    daemon_threads = True
    allow_reuse_address = True

    def get_request(self):
        connection, address = super().get_request()
        connection.settimeout(30)
        return connection, address

    def handle_error(self, request, client_address):
        if isinstance(sys.exc_info()[1], (BrokenPipeError, ConnectionResetError, ConnectionAbortedError)):
            return  # normal browser navigation / canceled audio preloading
        return super().handle_error(request, client_address)

'''+s[at:]
 s=s.replace("http.server.ThreadingHTTPServer(('127.0.0.1', port),", "BofNoCacheServer(('127.0.0.1', port),")
 p.write_bytes(s.replace('\n',nl).encode('utf8'))
print('Installed queued keep-alive no-cache serving; restart required. Original source preserved.')
