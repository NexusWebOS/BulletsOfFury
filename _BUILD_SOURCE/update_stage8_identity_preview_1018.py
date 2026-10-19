from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'docs/previews/stage8_pixellab_1018/index.html';s=p.read_text(encoding='utf-8')
if 'value="roar"' not in s:
 s=s.replace('<option value="hammer">','<option value="roar">Colossus · Roar</option><option value="speech">Dracodia · New avatar</option><option value="death">Colossus · Final death</option><option value="volcanohead">Volcano · Rotating head</option><option value="hammer">')
s=s.replace('Bullets of Fury · Stage 8 possession','Bullets of Fury · Stage 8 identities').replace('Stage 8 · PixelLab possession','Stage 8 · Native boss identities').replace('stage8-pixellab-1018','stage8-identity-1018')
s=s.replace('const options={phase1:','const options={roar:[2,0],speech:[2,0],death:[2,0],volcanohead:[2,2],phase1:')
s=s.replace("stageTimer=0;bossWarned=true;window.v18Onion=", "stageTimer=0;bossWarned=true;"+'''${scene.value==='roar'?'b._r30.v18.seq=1;v18StartAttack(b);':''}${scene.value==='speech'?'b._r30.mode="dr5Monologue";b._r30.t=0;dr5State(b).radio=null;dr5State(b).line=0;':''}${scene.value==='death'?'for(const i of V18.forms)j3State(b).hp[i]=0;j3FinalDeath(b);':''}${scene.value==='volcanohead'?'const p=gd4Create(b,2).p,F=p._fz;for(const q of b.parts)if(q.id!=="head"){q.hp=0;q.destroyed=true;F.pools[q.id==="core"?"body":q.id]=0;}furnaceEnter(p,"head");F.trans=0;b.hp=p.hp=F.pools.head;':''}window.v18Onion=''') if 'volcanohead' in s and 'gd4Create(b,2).p,F=p._fz' not in s else s
s=s.replace('p=b?.parts?.find(p=>p.id==="left")','p=b?.parts?.find(p=>["left","hammer","fanL"].includes(p.id)&&!p.destroyed)')
s=s.replace('b._lastPart=b.parts[0];hitBoss(1e8);','b.hp=0;r30Break(b);')
old='''const m=V18_ART.models[v18Model(b)];for(const i of [0,4,8,12])for(const a of Object.values(m.frames[i]))v18Cell(a,b.x,b.y,v18Size(b),.12);'''
new='''const n=b._r30.v18.form;if(v19Native(b)){ctx.save();ctx.globalAlpha=.14;if(n===8)for(const i of [1,3,6,8]){const a=HK5_ART.hammer[i];hk5Cell(a,b.x,b.y,a.w*.76*1.38,a.h*.76*1.38);}else v19Body(b);ctx.restore();}else{const bank=v19Acting(b)?V19_ART.clips[b._r30.v18.acting||"colossus_roar"]:null;if(bank)for(const i of [0,6,12,18])v18Cell(bank.frames[i],b.x,b.y,v18Size(b),.12);else{const m=V18_ART.models[v18Model(b)];for(const i of [0,4,8,12])for(const a of Object.values(m.frames[i]))v18Cell(a,b.x,b.y,v18Size(b),.12);}}'''
s=s.replace(old,new).replace('typeof V18!=="undefined"','typeof V19!=="undefined"')
p.write_text(s,encoding='utf-8',newline='\n');print('Updated native Stage8 review controls')
