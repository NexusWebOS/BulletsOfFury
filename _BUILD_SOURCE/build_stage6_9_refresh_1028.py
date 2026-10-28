"""Build the updated watch gallery from verified, continuous native recordings.

MP4 release names are NTFS hard links to the captures, avoiding duplicate media.
Chapter cards seek inside the complete films; they do not invent phase takes.
"""
from pathlib import Path
import argparse, hashlib, json, os, re, shutil
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / '_shots/stage6_9_refresh_1028'
GALLERY = ROOT / 'docs/previews/stage6_9_github_1028'
TAG = 'bof-stage6-9-updated-2026-10-28'
DOWNLOAD = f'https://github.com/NexusWebOS/BulletsOfFury/releases/download/{TAG}/'
TITLES = {
    'stage6-miniboss': 'Warhive Siege Fortress',
    'stage6-carrier-nightwing': 'Harrier Carrier → Nightwing · complete fight',
    'stage6-rough-riders': 'The Rough Riders · complete squad fight',
    'stage7-miniboss': 'Caustic Dredger',
    'stage7-boss': 'Toxic Portal Warden',
    'stage8-miniboss': 'Herald of Death',
    'stage8-final': 'Dracodia · first host through final victory',
    'stage9-miniboss': 'Event Horizon',
    'stage9-boss': 'Warp Sentinels → Tidal Sovereign',
}
NOTES = {
    'stage6-miniboss': 'Native six-battery encounter and exposed reactor.',
    'stage6-carrier-nightwing': 'Continuous Carrier destruction and Nightwing arrival, current aircraft frames and wind attacks.',
    'stage6-rough-riders': 'Current airshow entrance, team locks, individual attacks and native squad defeat.',
    'stage7-miniboss': 'Fast ram and reverse recovery, moving tracks, twin toxic machine guns and charged top cannon.',
    'stage7-boss': 'Connected rear-leg lunge, airborne shadow, portal explosions and native wreck departure.',
    'stage8-miniboss': 'Current warned flights, bomber passes and complete native ending.',
    'stage8-final': 'Uncut first-host fight, rebirth/download, copied forms, protected final life and ending.',
    'stage9-miniboss': 'Current directional flight, fast spin and charged eye attack.',
    'stage9-boss': 'Native sentinel gate, convergence, current water arsenal and final defeat.',
}
POSTER_TIME = {'stage6-miniboss':12, 'stage6-carrier-nightwing':20,
               'stage6-rough-riders':40, 'stage7-miniboss':12, 'stage7-boss':30,
               'stage8-miniboss':20, 'stage8-final':27, 'stage9-miniboss':20, 'stage9-boss':45}


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run')
    parser.add_argument('--partial', action='store_true')
    args = parser.parse_args()
    run = ROOT / (args.run or json.loads((BASE / 'latest.json').read_text())['folder'])
    state = json.loads((run / 'batch.json').read_text())
    if not args.partial:
        assert all(state['jobs'].get(k, {}).get('passed') for k in TITLES), 'Resolve failed or missing recordings before publication'
    release = run / 'release'
    release.mkdir(exist_ok=True)
    GALLERY.mkdir(parents=True, exist_ok=True)
    (GALLERY / 'posters').mkdir(exist_ok=True)
    entries, audits, reports = [], [], {}
    poster_sources = {}

    def poster(key, parent, at):
        folder, rows = reports[parent]
        choices = []
        for p in folder.glob('*.png'):
            m = re.fullmatch(r'frame-(\d+)', p.stem)
            n = re.fullmatch(r'phase-(\d+)', p.stem)
            t = float(m[1]) if m else rows[min(int(n[1]) - 1, len(rows) - 1)]['seconds'] if n else None
            if t is not None:
                choices.append((abs(t - at), p, t))
        assert choices, 'No native pixel evidence for ' + parent
        _, source, moment = min(choices)
        target = GALLERY / 'posters' / (key + '.jpg')
        with Image.open(source) as image:
            image.convert('RGB').resize((480, 300), Image.Resampling.LANCZOS).save(target, quality=85)
        poster_sources[key] = {'source': source.relative_to(ROOT).as_posix(), 'seconds': moment}
        return 'posters/' + target.name

    def chapter(key, parent, title, start, end, note=''):
        source = next((x for x in entries if x['id'] == parent), None)
        if source is None:
            return
        start, end = max(0, round(start, 2)), min(source['seconds'], round(end, 2))
        if end - start < 1:
            return
        entries.append(dict(id=key, parent=parent, stage=source['stage'], title=title,
                            start=start, end=end, seconds=round(end-start, 2),
                            src=source['src'], localSrc=source['localSrc'],
                            poster=poster(key, parent, start + min(8, (end-start)/2)),
                            note=note or 'Chapter from the same continuous native full-fight recording.'))

    for key, title in TITLES.items():
        job = state['jobs'].get(key, {})
        if not job.get('passed'):
            continue
        folder, video = ROOT / job['folder'], ROOT / job['video']
        proof = json.loads((folder / 'proof.json').read_text())
        report = proof['report']
        rows = report['timeline']
        assert report['completed'] and all(proof['checks'].values())
        reports[key] = folder, rows
        asset = release / (key + '.mp4')
        if asset.exists():
            assert os.path.samefile(asset, video), 'Existing release media belongs to another recording'
        else:
            os.link(video, asset)
        digest = sha(asset)
        entries.append(dict(id=key, stage=proof['job']['stage'], title=title,
                            seconds=round(job['seconds'], 2), src=DOWNLOAD + asset.name,
                            localSrc='/' + video.relative_to(ROOT).as_posix(),
                            poster=poster(key, key, POSTER_TIME[key]), note=NOTES[key],
                            sha256=digest, bytes=asset.stat().st_size))
        audits.append(dict(id=key, nativeName=rows[0].get('name'), seconds=job['seconds'],
                           nativeFPS=job['fps'], encodedFPS=30, width=1280, height=800,
                           audioPeakDb=proof['decodedPeakDb'], checks=proof['checks'],
                           nativeDefeatSeconds=report.get('defeatSeconds'),
                           expectedMediaCancellations=len(proof['expectedRequestCancellations']),
                           pageErrors=report['pageErrors'], consoleErrors=report['consoleErrors'],
                           assetErrors=report['assetErrors'], failedRequests=proof['failedRequests'],
                           sha256=digest, bytes=asset.stat().st_size,
                           runtimeHashes=proof['sourceHashes']))

    if 'stage6-carrier-nightwing' in reports:
        rows = reports['stage6-carrier-nightwing'][1]
        ace = next(q['seconds'] for q in rows if (q.get('carrierState') or {}).get('mode') == 'ace')
        length = next(x['seconds'] for x in entries if x['id'] == 'stage6-carrier-nightwing')
        chapter('stage6-carrier', 'stage6-carrier-nightwing', 'Carrier · hull, turbulence and destruction', 0, ace)
        chapter('stage6-nightwing', 'stage6-carrier-nightwing', 'Nightwing · arrival through defeat', ace, length)
        chapter('stage6-nightwing-shadow-turn', 'stage6-carrier-nightwing', 'Nightwing · current turns and wind attacks', ace+5, min(ace+40, length))
        chapter('stage6-nightwing-flight', 'stage6-carrier-nightwing', 'Nightwing · arrival and flight', ace, min(ace+20, length))
        winds = [q['seconds'] for q in rows if ((q.get('carrierState') or {}).get('ace') or {}).get('wind')]
        if winds:
            chapter('stage6-nightwing-wind', 'stage6-carrier-nightwing', 'Nightwing · wind arsenal', winds[0]-2, min(winds[0]+25, length))

    if 'stage6-rough-riders' in reports:
        rows = reports['stage6-rough-riders'][1]
        chapter('rough-riders-formations', 'stage6-rough-riders', 'Rough Riders · airshow entrance', 0, 40)
        tells = [q['seconds'] for q in rows if (q.get('rebelState') or {}).get('fleet') == 'tell']
        if tells:
            chapter('rough-riders-team-locks', 'stage6-rough-riders', 'Rough Riders · team lock and missile volley', tells[0]-2, tells[0]+15)
        stunts = [q['seconds'] for q in rows if (q.get('rebelState') or {}).get('fleet') == 'stunt']
        if stunts:
            chapter('rough-riders-evasion', 'stage6-rough-riders', 'Rough Riders · formation stunt flight', stunts[0]-2, stunts[0]+10)
        for pilot in ['kaia', 'jace', 'nyx', 'rook', 'voss']:
            moments = [q['seconds'] for q in rows for a in (q.get('rebelState') or {}).get('attacks', [])
                       if a['key'] == pilot and a.get('kind')]
            if moments:
                chapter('rough-riders-'+pilot, 'stage6-rough-riders', pilot.title()+' · live squad attack', moments[0]-2, moments[0]+24,
                        'A continuous chapter of the full squad fight; other pilots and allies remain active.')

    if 'stage8-final' in reports:
        rows = reports['stage8-final'][1]
        length = next(x['seconds'] for x in entries if x['id'] == 'stage8-final')
        final = next((q['seconds'] for q in rows if q.get('phase') == 2 and q.get('mode') == 'fight'), None)
        host_end = next((q['seconds'] for q in rows if q.get('mode') == 'dr5er23rebirth'), final)
        if host_end:
            chapter('s8-phase1', 'stage8-final', 'Dracodia · infused first host', 0, host_end)
        if final:
            chapter('s8-formation', 'stage8-final', 'Dracodia · rebirth and final-form download', host_end or max(0, final-90), final)
            chapter('s8-phase2', 'stage8-final', 'Dracodia · complete final-form battle', final, length)
            for form, key, label in [(0,'s8-dracodia','Dracodia base'), (8,'s8-code-hammer','Code Hammer'),
                                     (1,'s8-helicopter','Helicopter'), (6,'s8-neural-archon','Neural Archon'),
                                     (2,'s8-phoenix-volcano','Phoenix / Volcano')]:
                moments = [q for q in rows if q.get('phase') == 2 and q.get('form') == form and q.get('mode') == 'fight']
                if moments:
                    at = moments[0]['seconds']
                    stop = next((q['seconds'] for q in rows if q['seconds'] > at+1 and q.get('phase') == 2 and q.get('form') != form), length)
                    chapter(key, 'stage8-final', label+' · first native visit', max(final, at-1), stop)
            unlocked = next((q['seconds'] for q in rows if (q.get('dracodia') or {}).get('unlocked')), None)
            if unlocked:
                chapter('s8-final-life', 'stage8-final', 'Dracodia · final life and ending', unlocked, length)

    if 'stage9-boss' in reports:
        rows = reports['stage9-boss'][1]
        tidal = next((q['seconds'] for q in rows if q.get('mode') == 'tidal'), None)
        if tidal:
            length = next(x['seconds'] for x in entries if x['id'] == 'stage9-boss')
            chapter('stage9-sentinels', 'stage9-boss', 'Warp Sentinels · native gate and convergence', 0, tidal)
            chapter('stage9-tidal', 'stage9-boss', 'Tidal Sovereign · water arsenal and defeat', tidal, length)

    entries.sort(key=lambda c: (c['stage'], bool(c.get('parent')), list(TITLES).index(c.get('parent', c['id']))))
    manifest = json.dumps(entries, ensure_ascii=False, indent=2) + '\n'
    (GALLERY / 'manifest.json').write_text(manifest, encoding='utf-8')
    (release / 'manifest.json').write_text(manifest, encoding='utf-8')
    shutil.copyfile(ROOT / '_BUILD_SOURCE/stage6_9_gallery_1028.html', GALLERY / 'index.html')
    (GALLERY / '.nojekyll').touch()
    audit = dict(recorded='2026-10-28', release=TAG, method='Native encounter spawn; Furious, Cole level5 Laser/40 missiles, invulnerable input-only bot. No enemy health, phase or timer writes after spawn.',
                 recordings=audits, chapterCount=sum(bool(c.get('parent')) for c in entries), posterSources=poster_sources,
                 regressionSuite='node _BUILD_SOURCE/test_fl.js exits 1 before assertions: missing ignored UNUSED_ASSETS/retired_art_1022/manifest.json. No harness bypass or fabricated archive.',
                 gameJSChanged=False, testHarnessChanged=False)
    playback = run / 'gallery-playback.json'
    if playback.exists():
        audit['galleryPlayback'] = json.loads(playback.read_text(encoding='utf-8'))
    dispatch = ROOT / 'docs/qa/rebel_dispatch_1028.json'
    if dispatch.exists():
        q = json.loads(dispatch.read_text(encoding='utf-8'))
        audit['squadChecks'] = {key: q[key].get('checks',{}) if key != 'checks' else q[key]
                               for key in ['checks','sharedSquadRegression','rookRegression']}
    (release / 'recording-audit.json').write_text(json.dumps(audit, indent=2), encoding='utf-8')
    compact = {**audit, 'recordings': [{k:v for k,v in a.items() if k != 'runtimeHashes'} for a in audits]}
    (ROOT / 'docs/qa/stage6_9_refresh_1028.json').write_text(json.dumps(compact, indent=2), encoding='utf-8')
    sums = ''.join(sha(p)+'  '+p.name+'\n' for p in sorted(release.iterdir()) if p.is_file() and p.name != 'SHA256SUMS.txt')
    (release / 'SHA256SUMS.txt').write_text(sums, encoding='utf-8')
    readme = '# Updated Stage 6–9 recordings — October 28\n\n'
    readme += '[Watch the updated gallery](https://nexuswebos.github.io/BulletsOfFury/) · '
    readme += f'[Download all recordings](https://github.com/NexusWebOS/BulletsOfFury/releases/tag/{TAG})\n\n'
    readme += 'Nine continuous native Furious recordings with game audio. Cole uses level5 Laser,40 missiles and an invulnerable input bot; enemy health, transformations and defeats retain their native owners. Chapters seek inside these uncut recordings.\n\n'
    for stage in [6,7,8,9]:
        readme += '## Stage '+str(stage)+'\n\n'
        for c in entries:
            if c['stage'] == stage and not c.get('parent'):
                seconds = int(c['seconds'])
                readme += f'- [{c["title"]}]({c["src"]}) — {seconds//60}:{seconds%60:02}\n'
        readme += '\n'
    readme += 'Validation: each published film reaches native defeat, decodes fully, contains audible unclipped audio and has no game, bot, missing-asset or non-cancellation network errors. The complete core suite remains blocked before its summary by the missing ignored retired-art archive; see docs/qa/stage6_9_refresh_1028.json. Historical release videos are preserved.\n'
    (GALLERY / 'README.md').write_text(readme, encoding='utf-8')
    # Preserve the user's existing local review URL and old media; update only its gallery/catalog/posters.
    local = ROOT / '_shots/github_review_1028'
    local.mkdir(exist_ok=True)
    for name in ['index.html', 'manifest.json']:
        backup = local / (name + '.before-full-refresh-1028')
        if (local / name).exists() and not backup.exists():
            shutil.copyfile(local / name, backup)
        shutil.copyfile(GALLERY / name, local / name)
    (local / 'posters').mkdir(exist_ok=True)
    for c in entries:
        shutil.copyfile(GALLERY / c['poster'], local / c['poster'])
    print(json.dumps(dict(fullFights=len(audits), chapters=audit['chapterCount'], release=release.relative_to(ROOT).as_posix(), bytes=sum(a['bytes'] for a in audits))))


if __name__ == '__main__':
    main()
