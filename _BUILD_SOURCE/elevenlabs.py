#!/usr/bin/env python3
"""
elevenlabs.py - ElevenLabs in the Bullets of Fury pipeline.

    python3 _BUILD_SOURCE/elevenlabs.py voices                     # who can speak, and their ids
    python3 _BUILD_SOURCE/elevenlabs.py quota                      # characters left this month
    python3 _BUILD_SOURCE/elevenlabs.py say "GET READY" --voice <id> --out announce.mp3
    python3 _BUILD_SOURCE/elevenlabs.py batch lines.json           # a whole sheet in one pass
    python3 _BUILD_SOURCE/elevenlabs.py batch lines.json --dry     # cost it first, generate nothing

⚠ THE KEY IS NEVER IN THIS FILE. It is read from _BUILD_SOURCE/.secrets.json, which .gitignore
covers by name. Anything generated here lands in assets/game/voice/ and is ordinary committed art;
the key is not.

⚠ AND IT IS BILLED PER CHARACTER, so `batch --dry` prints the character count and the file list
without spending anything. Run the dry pass first on any sheet you have not run before.

The game's own voice slots (Audio.VOICE_SET in assets/game.js) are:
    continueVO  countdown  restrictedarea  enemyunits  enemyunit
    over        goodluck   announce        selectpilot
A batch sheet is a JSON list of {"key": <slot or new name>, "text": "...", "voice": "<id>"} and
writes assets/game/voice/<key>.mp3, so a generated line drops straight onto an existing cue.
"""
import os, sys, json, io, argparse, urllib.request, urllib.error

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SECRETS = os.path.join(ROOT, '_BUILD_SOURCE', '.secrets.json')
VOICE_DIR = os.path.join(ROOT, 'assets', 'game', 'voice')
API = 'https://api.elevenlabs.io/v1'


def key():
    if not os.path.exists(SECRETS):
        sys.exit('no %s - create it with {"elevenlabs_api_key": "..."} (it is gitignored)' % SECRETS)
    k = json.load(io.open(SECRETS, encoding='utf-8')).get('elevenlabs_api_key')
    if not k:
        sys.exit('elevenlabs_api_key missing from %s' % SECRETS)
    return k


def call(path, data=None, raw=False, method=None):
    req = urllib.request.Request(
        API + path,
        data=(json.dumps(data).encode('utf-8') if data is not None else None),
        headers={'xi-api-key': key(), 'Content-Type': 'application/json'},
        method=method or ('POST' if data is not None else 'GET'))
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            body = r.read()
            return body if raw else json.loads(body.decode('utf-8'))
    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', 'replace')[:400]
        sys.exit('ElevenLabs %s on %s\n%s' % (e.code, path, detail))


# ⚠ MIKE'S KEY IS SCOPED TO SYNTHESIS ONLY. Measured: /text-to-speech works and returns real mp3
# (0xFF frame header), while /voices and /user/subscription both return 401
# "missing the permission voices_read / user_read". So the listing cannot come from the API with
# this key, and a tool that only works with a broader key is a tool that does not work. These are
# the stock public voice ids, which synthesis accepts regardless of read scope.
STOCK = [
    ('Adam',    'pNInz6obpgDQGcFmaJgB', 'deep, narration - good for the announcer'),
    ('Antoni',  'ErXwobaYiN019PkySvjV', 'warm male'),
    ('Arnold',  'VR6AewLTigWG4xSOukaG', 'crisp male, commanding'),
    ('Josh',    'TxGEqnHWrfWFTfGW9XjX', 'young male'),
    ('Sam',     'yoZ06aMxZJJ28mfd3POQ', 'raspy male'),
    ('Rachel',  '21m00Tcm4TlvDq8ikWAM', 'calm female'),
    ('Bella',   'EXAVITQu4vr4xnSDxMaL', 'soft female'),
    ('Elli',    'MF3mGyEYCl7XYWbV9V6O', 'emotional female'),
    ('Domi',    'AZnzlk1XvdvUeBnXmlld', 'strong female'),
]


def cmd_voices(a):
    try:
        v = call('/voices')
        rows = v.get('voices', [])
    except SystemExit:
        print('/voices refused (key lacks voices_read) - the stock ids below still synthesise:')
        for n, i, note in STOCK:
            print('  %-10s %-24s %s' % (n, i, note))
        return
    print('%d voices' % len(rows))
    for x in rows:
        lab = x.get('labels') or {}
        bits = ', '.join('%s=%s' % (k, lab[k]) for k in ('gender', 'age', 'accent', 'use_case') if lab.get(k))
        print('  %-22s %-24s %s' % (x.get('name'), x.get('voice_id'), bits))


def cmd_quota(a):
    u = call('/user/subscription')
    used, lim = u.get('character_count', 0), u.get('character_limit', 0)
    print('tier   : %s' % u.get('tier'))
    print('used   : %s of %s characters (%s left)' % (used, lim, max(0, lim - used)))


def synth(text, voice, model='eleven_multilingual_v2', stability=0.45, similarity=0.75, style=0.35):
    return call('/text-to-speech/' + voice, {
        'text': text, 'model_id': model,
        'voice_settings': {'stability': stability, 'similarity_boost': similarity,
                           'style': style, 'use_speaker_boost': True},
    }, raw=True)


def write(path, blob):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'wb').write(blob)
    return len(blob)


def cmd_say(a):
    if not a.voice: sys.exit('--voice <id> required; run `voices` to list them')
    out = a.out or (a.text[:24].strip().replace(' ', '_').lower() + '.mp3')
    p = out if os.path.isabs(out) else os.path.join(VOICE_DIR, out)
    n = write(p, synth(a.text, a.voice, a.model))
    print('%s  %d bytes  (%d chars billed)' % (os.path.relpath(p, ROOT), n, len(a.text)))


def cmd_batch(a):
    sheet = json.load(io.open(a.sheet, encoding='utf-8'))
    lines = sheet['lines'] if isinstance(sheet, dict) else sheet
    dv = (sheet.get('voice') if isinstance(sheet, dict) else None)
    chars = sum(len(L['text']) for L in lines)
    print('%d lines, %d characters billed' % (len(lines), chars))
    for L in lines:
        print('   %-18s %-10s %s' % (L['key'], (L.get('voice') or dv or '-')[:10], L['text'][:56]))
    if a.dry:
        print('\n--dry: nothing generated, nothing billed')
        return
    for L in lines:
        v = L.get('voice') or dv
        if not v: sys.exit('line %s has no voice and the sheet sets no default' % L['key'])
        p = os.path.join(VOICE_DIR, L['key'] + '.mp3')
        n = write(p, synth(L['text'], v, L.get('model', a.model),
                           L.get('stability', 0.45), L.get('similarity', 0.75), L.get('style', 0.35)))
        print('  wrote %-40s %d bytes' % (os.path.relpath(p, ROOT), n))


def main():
    ap = argparse.ArgumentParser(description='ElevenLabs for Bullets of Fury')
    ap.add_argument('--model', default='eleven_multilingual_v2')
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('voices').set_defaults(fn=cmd_voices)
    sub.add_parser('quota').set_defaults(fn=cmd_quota)
    s = sub.add_parser('say'); s.add_argument('text'); s.add_argument('--voice'); s.add_argument('--out')
    s.set_defaults(fn=cmd_say)
    b = sub.add_parser('batch'); b.add_argument('sheet'); b.add_argument('--dry', action='store_true')
    b.set_defaults(fn=cmd_batch)
    a = ap.parse_args(); a.fn(a)


if __name__ == '__main__':
    main()
