"""Authenticated PixelLab MCP client for reproducible local art workflows.

Credentials stay in the user's Codex configuration. Full tool results remain
in the chosen local output file; stdout contains only redacted summaries.
"""
import argparse
import atexit
import json
import os
from pathlib import Path
import sys
import tomllib
import urllib.error
import urllib.request


class PixelLab:
    def __init__(self):
        config = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'config.toml'
        server = tomllib.loads(config.read_text(encoding='utf-8-sig'))['mcp_servers']['pixellab']
        self.url = server['url']
        if self.url != 'https://api.pixellab.ai/mcp':
            raise ValueError('Unexpected PixelLab MCP endpoint')
        self.headers = dict(server.get('http_headers', {}))
        if server.get('bearer_token_env_var'):
            self.headers['Authorization'] = 'Bearer ' + os.environ[server['bearer_token_env_var']]
        self.headers.update({'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream'})
        self.session = None
        self.counter = 0
        result = self.rpc('initialize', {'protocolVersion': '2025-03-26', 'capabilities': {},
                         'clientInfo': {'name': 'bullets-of-fury-art-pipeline', 'version': '1.0'}})
        self.headers['MCP-Protocol-Version'] = result.get('protocolVersion', '2025-03-26')
        self.rpc('notifications/initialized', notify=True)
        atexit.register(self.close)

    def close(self):
        if not self.session:
            return
        headers = dict(self.headers)
        headers['Mcp-Session-Id'] = self.session
        self.session = None
        try:
            request = urllib.request.Request(self.url, headers=headers, method='DELETE')
            with urllib.request.urlopen(request, timeout=10):
                pass
        except Exception:
            pass  # Stateless servers may not implement session termination.

    def rpc(self, method, params=None, notify=False):
        payload = {'jsonrpc': '2.0', 'method': method}
        if not notify:
            self.counter += 1
            payload['id'] = self.counter
        if params is not None:
            payload['params'] = params
        headers = dict(self.headers)
        if self.session:
            headers['Mcp-Session-Id'] = self.session
        request = urllib.request.Request(self.url, data=json.dumps(payload).encode(), headers=headers, method='POST')
        with urllib.request.urlopen(request, timeout=55) as response:
            self.session = response.headers.get('Mcp-Session-Id') or self.session
            raw = response.read().decode('utf-8')
        if notify:
            return None
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            candidates = [json.loads(line[5:].strip()) for line in raw.splitlines() if line.startswith('data:') and line[5:].strip()]
            obj = next(q for q in candidates if q.get('id') == self.counter)
        if 'error' in obj:
            raise RuntimeError('PixelLab MCP returned RPC error ' + str(obj['error'].get('code')))
        return obj['result']

    def call(self, name, arguments):
        return self.rpc('tools/call', {'name': name, 'arguments': arguments})


def unpack(result):
    if result.get('structuredContent'):
        return result['structuredContent']
    for content in result.get('content', []):
        if content.get('type') == 'text':
            try:
                return json.loads(content['text'])
            except json.JSONDecodeError:
                continue
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['catalog', 'call'])
    parser.add_argument('--tool')
    parser.add_argument('--args', type=Path)
    parser.add_argument('--out', required=True, type=Path)
    options = parser.parse_args()
    client = PixelLab()
    result = client.rpc('tools/list', {}) if options.mode == 'catalog' else client.call(options.tool, json.loads(options.args.read_text(encoding='utf-8')))
    options.out.parent.mkdir(parents=True, exist_ok=True)
    options.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    info = unpack(result)
    print(json.dumps({'saved': str(options.out), 'isError': bool(result.get('isError')), 'result_fields': list(info) if isinstance(info, dict) else type(info).__name__,
                      'tool_count': len(result.get('tools', [])) if options.mode == 'catalog' else None}))
    return 1 if result.get('isError') else 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except urllib.error.HTTPError as exc:
        print(json.dumps({'error': 'PixelLab HTTP failure', 'status': exc.code, 'details_suppressed': True}))
        raise SystemExit(2)
    except Exception as exc:
        print(json.dumps({'error': type(exc).__name__, 'details_suppressed': True}))
        raise SystemExit(2)
