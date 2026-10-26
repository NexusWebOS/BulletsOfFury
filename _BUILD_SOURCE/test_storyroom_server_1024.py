from pathlib import Path
import importlib.util,json,threading,urllib.request,urllib.error,time,sys
R=Path(__file__).resolve().parents[1];O=R/'_shots/storyroom_1024';O.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('storyserver',R/'_BUILD_SOURCE/storyboard_server_1024.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
T=(O/('server-fixture-'+str(time.time_ns()))).resolve();assert T.is_relative_to(O.resolve());T.mkdir();m.ROOT=T;m.DATA=T/'assets/data/storyboard_1024.json';m.SCRIPT=T/'assets/storyboard_data_1024.js'
server=m.StoryroomHTTPServer(('127.0.0.1',0),m.Handler);threading.Thread(target=server.serve_forever,daemon=True).start();url='http://127.0.0.1:'+str(server.server_port);checks=[]
def ck(n,ok):checks.append(dict(name=n,passed=bool(ok)));print(('PASS 'if ok else'FAIL ')+n)
def post(obj,origin=None):
 req=urllib.request.Request(url+'/api/storyboard/save',data=json.dumps(obj).encode(),headers={'Content-Type':'application/json','Origin':origin or url},method='POST')
 try:
  with urllib.request.urlopen(req)as r:return r.status,json.load(r)
 except urllib.error.HTTPError as e:return e.code,json.load(e)
try:
 blocked=False
 try:duplicate=m.StoryroomHTTPServer(('127.0.0.1',server.server_port),m.Handler);duplicate.server_close()
 except OSError:blocked=True
 ck('Exclusive port prevents duplicate editor servers',blocked)
 old_args=sys.argv
 try:
  sys.argv=['storyroom','--port',str(server.server_port),'--no-open'];m.main();ck('Reopening the launcher reuses the running editor',True)
 finally:sys.argv=old_args
 data=json.load(urllib.request.urlopen(url+'/api/storyboard'));ck('New project reads as empty native overrides',data['project']==m.EMPTY)
 doc={'version':1,'overrides':{'post-3':{'yuri':[{'source':0,'edited':['text'],'fields':{'text':'</script><script>not executable</script>'},'enabled':True}]}},'triggers':{},'order':[]}
 ck('Foreign origin cannot write',post(doc,'https://unrelated.invalid')[0]==403 and not m.DATA.exists())
 ck('Valid project writes canonical JSON and runtime script',post(doc)[0]==200 and json.loads(m.DATA.read_text())==doc and 'JSON.parse(' in m.SCRIPT.read_text())
 before=m.DATA.read_bytes();bad=json.loads(json.dumps(doc));bad['overrides']['post-3']['yuri'][0]['fields']['code']='alert(1)'
 ck('Unknown executable fields are rejected without mutation',post(bad)[0]==400 and m.DATA.read_bytes()==before)
 bad=json.loads(json.dumps(doc));bad['overrides']['post-3']['yuri'][0]['fields']['duration']=-1
 ck('Invalid duration is rejected',post(bad)[0]==400 and m.DATA.read_bytes()==before)
 bad=json.loads(json.dumps(doc));bad['overrides']['post-3']['yuri'][0]['fields']['text']=None
 ck('Null dialogue is rejected',post(bad)[0]==400)
 post(m.EMPTY);backups=list((T/'_ART_SOURCES/storyboard_1024/backups').glob('*.json'))
 ck('Apply preserves a backup of the previous saved project',len(backups)==1 and json.loads(backups[0].read_text())==doc)
 ck('Atomic writes leave no temporary files',not list(T.rglob('*.storyroom-tmp')))
finally:server.shutdown();server.server_close()
out=dict(passed=sum(c['passed']for c in checks),failed=sum(not c['passed']for c in checks),checks=checks);(O/'server.json').write_text(json.dumps(out,indent=2)+'\n');print('SUMMARY',out['passed'],out['failed']);raise SystemExit(bool(out['failed']))
