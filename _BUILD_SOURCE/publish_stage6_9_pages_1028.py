"""Fast-forward the existing Pages gallery without switching the game checkout.

Uses a private temporary Git index; the real index, branch and unrelated Pages
files are preserved. Run only after the release media is uploaded and public.
"""
from pathlib import Path
import json, os, subprocess

R = Path(__file__).resolve().parents[1]
B = R / '_shots/stage6_9_refresh_1028'
O = R / json.loads((B/'latest.json').read_text())['folder']
source = R / 'docs/previews/stage6_9_github_1028'
catalog = json.loads((source/'manifest.json').read_text(encoding='utf-8'))
assert len([c for c in catalog if not c.get('parent')]) == 9
paths = ['index.html','manifest.json','README.md','.nojekyll'] + sorted({c['poster'] for c in catalog})
environment = {**os.environ, 'GIT_INDEX_FILE':str(O.resolve()/'gh-pages.index')}


def git(*args, data=None):
    return subprocess.run(['git',*args],cwd=R,env=environment,input=data,capture_output=True,check=True).stdout.decode().strip()


head = git('rev-parse','HEAD')
branch = git('branch','--show-current')
parent = git('rev-parse','origin/gh-pages')
git('read-tree',parent)
for name in paths:
    p = (source/name).resolve()
    assert p.is_relative_to(source.resolve()) and p.is_file()
    blob = git('hash-object','-w','--stdin',data=p.read_bytes())
    git('update-index','--add','--cacheinfo','100644,'+blob+','+name)
tree = git('write-tree')
if tree == git('rev-parse',parent+'^{tree}'):
    commit = parent
else:
    message = b'Publish fresh Stage 6-9 complete fights and native chapters\n'
    commit = git('commit-tree',tree,'-p',parent,data=message)
    print(git('diff','--stat',parent,commit))
    # Git rejects a non-fast-forward if someone else updated Pages meanwhile.
    result = subprocess.run(['git','push','origin',commit+':refs/heads/gh-pages'],cwd=R,capture_output=True,text=True,check=True)
    print(result.stdout+result.stderr)
assert git('rev-parse','HEAD') == head and git('branch','--show-current') == branch
result = dict(sourceCommit=head,sourceBranch=branch,parent=parent,pagesCommit=commit,
              gallery='https://nexuswebos.github.io/BulletsOfFury/',files=paths)
(O/'pages-publication.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
