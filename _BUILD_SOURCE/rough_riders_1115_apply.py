from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parents[1]
O=R/'_shots/rough_riders_1115';O.mkdir(parents=True,exist_ok=True)
receipt=O/'rename-changes.json'
changes=json.loads(receipt.read_text(encoding='utf8'))['files']if receipt.exists()else{}
def edit(name,pairs):
    p=R/name;before=p.read_bytes();data=before;edits=[]
    for old,new in pairs:
        oldb=old.encode('utf8');newb=new.encode('utf8');count=data.count(oldb)
        if count:data=data.replace(oldb,newb);edits.append({'before':old,'after':new,'count':count})
        else:assert newb in data,(name,old)
    if data!=before:
        p.write_bytes(data)
        q=changes.setdefault(name,{'beforeSha256':hashlib.sha256(before).hexdigest(),'edits':[]})
        q['edits']+=edits;q['afterSha256']=hashlib.sha256(data).hexdigest()
        assert data.count(b'\r\n')==before.count(b'\r\n'),name
        receipt.write_text(json.dumps({'files':changes,'testRunnerUnchanged':True,'gameLF':True},indent=2),encoding='utf8',newline='\n')
edit('assets/game.js',[
 ('FIVE-SHIP WING, TAKE THE REBELS TOGETHER!','FIVE-SHIP WING, TAKE THE ROUGH RIDERS TOGETHER!'),
 ('RIGHT: REBELS','RIGHT: ROUGH RIDERS'),("b.name='REBEL SQUAD'","b.name='ROUGH RIDERS'")])
edit('assets/cinematic_director_0930.js',[
 ('The Harrier is finished. What happened to the rebel squad?','The Harrier is finished. What happened to the Rough Riders?'),
 ('Rebel Fury is down. I wish they had listened.','The Rough Riders are down. I wish they had listened.'),
 ('All five rebel signals are gone.','All five Rough Rider signals are gone.'),
 ('I am taking the carrier. Keep the rebels on radar.','I am taking the carrier. Keep the Rough Riders on radar.'),
 ('Right side: Voss and his old unit. They took the gear from our forward depot.','Right side: the Rough Riders. Voss and his unit took the gear from our forward depot.')])
reports=[
 ('The Harrier is down. The remaining rebel contacts are marked.','The Harrier is down. The remaining Rough Rider contacts are marked.'),
 ('The rebel formation is down. The remaining Harrier threat is marked.','The Rough Riders are down. The remaining Harrier threat is marked.')]
edit('assets/cinema_bridges_1110.js',reports)
edit('assets/cinema_direction_1110.js',reports+[
 ('Harrier to the left. Rebel formation to the right.','Harrier to the left. Rough Riders to the right.'),
 ('RIGHT: REBEL FORMATION','RIGHT: ROUGH RIDERS')])
edit('assets/story_campaign_1103.js',[
 ('The Rebel Fighters have reached the city.','The Rough Riders have reached the city.')])
edit('assets/crossed_fate_1115.js',[
 ('Rebel Fighters','Rough Riders'),
 ('Keep the Harrier and the Rebels on radar.','Keep the Harrier and the Rough Riders on radar.'),
 ("left=q.crash?'the Harrier and the Rough Riders':FATE15_NAMES[q.target]","left=q.crash?'the Harrier and the Rough Riders':'the '+FATE15_NAMES[q.target]"),
 ("FATE15_NAMES[q.defeated]+' is down. '+FATE15_NAMES[q.target]+' is still heading for the city.'","fate15SkyReport(q)")])
p=R/'assets/crossed_fate_1115.js';s=p.read_bytes();anchor=b'const fate15Ease=';helper=b"function fate15SkyReport(q){const down=q.defeated==='rebels'?'The Rough Riders are down.':FATE15_NAMES[q.defeated]+' is down.',incoming=q.target==='rebels'?'The Rough Riders are still heading for the city.':'The Harrier is still heading for the city.';return down+' '+incoming;}\n"
if b'function fate15SkyReport('not in s:
    assert s.count(anchor)==1;edit('assets/crossed_fate_1115.js',[(anchor.decode(),helper.decode()+anchor.decode())])
edit('assets/part2_combat_1010.js',[('REBEL FURY SQUADRON','ROUGH RIDERS')])
edit('assets/password_catalog_1005.js',[('STAGE 6 REBELS','STAGE 6 ROUGH RIDERS'),('STAGE X REBELS','STAGE X ROUGH RIDERS')])
edit('assets/storyboard_1024.js',[('Rebel route','Rough Riders route'),('Rebel squad','Rough Riders')])
edit('assets/enemy_atlas_1013.js',[('Rebel fighters','Rough Riders')])
edit('assets/data/enemy_atlas_1013.json',[('Rebel Fighters','Rough Riders'),('rebel pilot','Rough Rider pilot')])
# The current preview packagers should also use the approved name on new reels.
# Keep existing clips, frozen source snapshots and historical receipts intact.
for name in ['city_rescue_1115_package.py','crossed_fate_1115_package.py']:
    edit('_BUILD_SOURCE/'+name,[('Rebel Fighters','Rough Riders'),('Rebel interception','Rough Riders interception')])
assert b'\r\n'not in (R/'assets/game.js').read_bytes()
test=R/'_BUILD_SOURCE/test_fl.js';assert hashlib.sha256(test.read_bytes()).hexdigest()=='8d6f8332cec791f9e3b1b2e15b856458cb080abe2a40d44c3378bca221d9a72f'
for name in ['AGENTS.md','HANDOFF_CODEX.md']:
    p=R/name;b=p.read_bytes();nl=b'\r\n'if b.count(b'\r\n')>b.count(b'\n')/2 else b'\n'
    if name=='AGENTS.md':
        note='- November15 canonical dialogue name: **the Rough Riders**. Use Rough Rider for one member and Rough Riders for the squad in all new dialogue, route reports, UI labels and descriptions. Legacy rebel/rebelsquad asset keys, saves, passwords, encounter IDs and individual pilot names remain stable. See docs/ROUGH_RIDERS_SELECTION_1115.md.'
        mark=b'## Creative constraints\r\n'if b'## Creative constraints\r\n'in b else b'## Creative constraints\n'
        if b'November15 canonical dialogue name'not in b:
            assert mark in b;p.write_bytes(b.replace(mark,mark+nl+note.encode('utf8')+nl,1))
    else:
        note='## November15 - Rough Riders naming and pursuit highlight GIFs\n\nAll current in-game squad references now say Rough Riders, including native radio/fallback dialogue, Stage6 reports, route briefings, achievement description, password labels and dossier text. Internal asset/encounter/save/password IDs and individual pilots remain stable. Existing native generated-menu selection is captured with real left/right input in Hard/Furious GIFs. See docs/ROUGH_RIDERS_SELECTION_1115.md and docs/qa/rough_riders_1115.json. The album remains Bulletalica. game.js has exactly three visible-label changes and remains LF; tests remain unchanged CRLF. No commit/push.\n\n'
        if not b.startswith(b'## November15 - Rough Riders naming'):p.write_bytes(note.replace('\n',nl.decode()).encode('utf8')+b)
if changes:
    (O/'rename-changes.json').write_text(json.dumps({'files':changes,'testRunnerUnchanged':True,'gameLF':True},indent=2),encoding='utf8',newline='\n')
    print(json.dumps({k:sum(e['count']for e in v['edits'])for k,v in changes.items()},indent=2))
else:print('Naming is already current.')
