from pathlib import Path
import shutil,json,hashlib,re
R=Path(__file__).resolve().parents[1]
S=R/'_BUILD_SOURCE/furious_encounters_1102';S.mkdir(exist_ok=True)
O=R/'_shots/furious_encounters_1102';O.mkdir(exist_ok=True)
G=Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
for name,source in [('razorwake','exec-18a4ba07-dc2a-495b-9030-0d0eacad3d68.png'),('thunderhead','exec-b9f1d869-a909-4b1a-a469-02c1823b8b21.png'),('storm','exec-66737c88-3926-4fb3-852a-df7511ba5c49.png')]:
    target=S/(name+'_source.png')
    if not target.exists():shutil.copy2(G/source,target)
paths=['index.html','assets/game.js']
paths += [p.split('?')[0] for p in re.findall(r'<script src="([^"]+)"',(R/'index.html').read_text(encoding='utf-8')) if (R/p.split('?')[0]).is_file()]
before=O/'starting-runtime.json'
if not before.exists():before.write_text(json.dumps({p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in paths},indent=2))
print('Sources preserved; starting runtime fingerprint saved')
concepts=S/'concepts';concepts.mkdir(exist_ok=True)
for name,source in [('stage2-pyroclast','exec-07a150f3-73ac-49e0-86db-abe4d1709417.png'),('stage3-cryocode','exec-0516cf99-24be-42a0-8ee2-0ee0d0e0995c.png'),('stage4-aftershock','exec-d2ed2210-aeaa-45f2-a1dc-d18d630e298c.png'),('stage5-parallax','exec-7f6bc12e-6d0c-4d48-b549-5698c4785d50.png')]:
    target=concepts/(name+'.png')
    if not target.exists():shutil.copy2(G/source,target)
print('All four concept boards saved in the project')
