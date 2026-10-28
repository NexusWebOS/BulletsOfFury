'use strict';
/* PixelLab-authored map services, and Decker's whole-build Re-Spec.
   Two points per DISTINCT cleared stage; visits and retries never mint points.
   Fee is profile FP. Upgrade points and the score are separate balances. */
const HF23={fee:300,modal:null,layout:[],base:{}};
UC22_ROWS[2]='RE-SPEC ALL UPGRADES';
UC22.size=256;
function hf23Warm(){for(const k of Object.keys(HF23_ART.assets))XART.rdy(k);}
function hf23Stage(n){return Number.isInteger(Number(n))&&Number(n)>=1&&Number(n)<=10;}
function hf23RankStages(){return run.mode==='campaign'?Object.keys(campaign.rank||{}).filter(k=>hf23Stage(k)&&campaign.rank[k]).map(Number):[];}
function hf23Budget(){
 if(!run._forgeBudget23){
  const cleared=hf23RankStages();
  // Older campaign slots recorded only their unlocked destination. Password/debug stage alone is not proof.
  if(!cleared.length&&run.mode==='campaign')for(let n=1;n<Math.min(9,campaign.unlockedMax|0);n++)cleared.push(n);
  const owned={};for(const [w,forms] of Object.entries(run.forgeForms||{}))owned[w]=new Set(Object.keys(forms||{}));
  for(const [w,f] of Object.entries(run.forge||{}))if(f&&INFUSIONS[f.elem]){if(!owned[w])owned[w]=new Set();owned[w].add(f.elem);}
  let spent=0;for(const forms of Object.values(owned))spent+=forms.size;
  run._forgeBudget23={v:1,cleared,spent,reset:0};run.forgeCombos=Math.max(0,cleared.length*2-spent);
 }
 const B=run._forgeBudget23;
 for(const n of hf23RankStages())if(!B.cleared.includes(n)){B.cleared.push(n);run.forgeCombos=Math.max(0,run.forgeCombos|0)+2;}
 return B;
}
function hf23Earned(){return hf23Budget().cleared.length*2;}
function hf23Grant(n){const B=hf23Budget();if(!hf23Stage(n)||B.cleared.includes(n))return false;
 B.cleared.push(n);run.forgeCombos=Math.max(0,run.forgeCombos|0)+2;return true;}
HF23.base.start=startRun;
startRun=function(){delete run._forgeBudget23;delete run._respecBase23;return HF23.base.start.apply(this,arguments);};
HF23.base.clear=setState;
setState=function(s){if(s===GS.STAGECLEAR&&state!==GS.STAGECLEAR&&run)hf23Grant(run.stage|0);return HF23.base.clear.apply(this,arguments);};
HF23.base.auto=campAutoAfterClear;
campAutoAfterClear=function(n){hf23Grant(n|0);return HF23.base.auto.apply(this,arguments);};
HF23.base.forgeStart=forgeStart;
forgeStart=function(){hf23Budget();const n=run.forgeCombos;const r=HF23.base.forgeStart.apply(this,arguments);run.forgeCombos=n;return r;};
HF23.base.combine=forgeCombine;
forgeCombine=function(){hf23Budget();const r=HF23.base.combine.apply(this,arguments);if(r==='ok')run._forgeBudget23.spent++;return r;};
HF23.base.snap=campSnapshot;
campSnapshot=function(){hf23Budget();const s=HF23.base.snap.apply(this,arguments);if(s){s.forgeBudget23=JSON.parse(JSON.stringify(run._forgeBudget23));s.forgeCombos=Math.max(0,run.forgeCombos|0);s.respecBase23=!!run._respecBase23;
 // The ship is parked at a service, not at the Stage1 flag used to navigate north.
 if(run.mode==='campaign'&&(UC22.focus||UC22.open||[GS.FORGE,GS.LOADOUT].includes(state)))s.stage=run._forgeBudget23.cleared.includes(run.stage|0)?Math.min(8,Math.max(run.stage+1,campaign.unlockedMax|0)):clamp(run.stage|0,1,9);
 }return s;};
HF23.base.apply=campApply;
campApply=function(s){
 const old=run._respecBase23;run._respecBase23=!!(s&&s.respecBase23);
 const ok=HF23.base.apply.apply(this,arguments);if(!ok){run._respecBase23=old;return ok;}
 delete run._forgeBudget23;
 if(s.forgeBudget23&&s.forgeBudget23.v===1&&Array.isArray(s.forgeBudget23.cleared)){
  const b=s.forgeBudget23,cleared=[...new Set(b.cleared.filter(hf23Stage).map(Number))];
  run._forgeBudget23={v:1,cleared,spent:Math.max(0,b.spent|0),reset:Math.max(0,b.reset|0)};
  run.forgeCombos=clamp(s.forgeCombos|0,0,cleared.length*2);
 }
 hf23Budget();return ok;
};
function hf23HasForms(){return Object.values(run.forgeForms||{}).some(q=>q&&Object.keys(q).length)||Object.keys(run.forge||{}).length>0;}
function hf23Info(){return{earned:hf23Earned(),left:Math.max(0,run.forgeCombos|0),fee:HF23.fee,balance:Math.max(0,furiousBalance()),hasForms:!!hf23HasForms()};}
function hf23PayReset(){
 const I=hf23Info();if(!I.hasForms)return 'bare';if(I.balance<I.fee)return 'poor';
 const old={forge:run.forge,forms:run.forgeForms,vars:run.wvars,infusion:run.infusion,combos:run.forgeCombos,base:run._respecBase23,budget:JSON.parse(JSON.stringify(run._forgeBudget23))};
 const L=furiousLedger();if(!L.supplies)L.supplies=[];
 const oldProfile=localStorage.getItem(ACHIEVEMENT_STORE_KEY),oldAuto=localStorage.getItem(CAMP_AUTO_KEY);
 L.supplies.push({kind:'respec',cost:I.fee,at:Date.now()});
 run.forge={};run.forgeForms={};run.wvars=[];run.infusion=null;run._respecBase23=true;
 run.forgeCombos=I.earned;run._forgeBudget23.spent=0;run._forgeBudget23.reset++;
 try{
  if(!achievementSave())throw Error('profile');
  if(run.mode==='campaign'){
   const data=campSnapshot(),raw=JSON.stringify(data);localStorage.setItem(CAMP_AUTO_KEY,raw);
   if(localStorage.getItem(CAMP_AUTO_KEY)!==raw)throw Error('campaign');campSession=data;
  }
 }catch(_save){
  HF23.lastSaveError=String(_save);
  L.supplies.pop();Object.assign(run,{forge:old.forge,forgeForms:old.forms,wvars:old.vars,infusion:old.infusion,forgeCombos:old.combos,_respecBase23:old.base,_forgeBudget23:old.budget});
  try{if(oldProfile==null)localStorage.removeItem(ACHIEVEMENT_STORE_KEY);else localStorage.setItem(ACHIEVEMENT_STORE_KEY,oldProfile);if(oldAuto==null)localStorage.removeItem(CAMP_AUTO_KEY);else localStorage.setItem(CAMP_AUTO_KEY,oldAuto);}catch(_rollback){}
  return 'save';
 }
 return 'ok';
}
function hf23Open(){hf23Warm();hf23Budget();HF23.modal={t:0,sel:1,md:!!Input.mouse.down,msg:'',frame:sm22Snapshot()};Input.clearTaps();}
forgeRespec=function(){hf23Open();return 'menu';};
function hf23Blit(key,x,y){if(XART.rdy(key))ctx.drawImage(XART.get(key),Math.round(x),Math.round(y));}
function hf23Text(text,r,size=12,color='#ecf6ff'){
 const q=mw21Text(text,r,size,color);HF23.layout.push({text,...q});return q;
}
function hf23Button(cx,cy,label,selected,enabled=true,small=false){
 const w=small?160:324,h=small?30:40;
 hf23Blit('hf23_'+(small?'small':'row')+'_'+(!enabled?'disabled':selected?'selected':'idle'),cx-w/2,cy-h/2);
 hf23Text(label,{x:cx-w/2+(small?23:34),y:cy-h/2+5,w:w-(small?31:45),h:h-10},small?11:13,!enabled?'#77818d':selected?'#ffdc87':'#d4dfec');
}
function hf23Backdrop(frame){const F=sm22Field();ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='#060c16';ctx.fillRect(0,0,F.W,F.H);ctx.restore();ctx.save();ctx.setTransform(F.k,0,0,F.k,F.ox,F.oy);hf23Blit('hf23_backdrop',0,0);return F;}
function hf23Close(){HF23.modal=null;Input.clearTaps();}
function hf23Draw(dt){
 const M=HF23.modal;if(!M)return;M.t+=Number.isFinite(dt)?dt:1/60;HF23.layout=[];hf23Warm();hf23Backdrop(M.frame);
 const I=hf23Info(),x=12,y=80;
 hf23Blit('hf23_menu',x,y);
 hf23Text('DECKER / RE-SPEC',{x:x+106,y:y+28,w:244,h:30},17,'#ffd17a');
 const msg=M.msg||(!I.hasForms?'YOUR WEAPONS ARE ALREADY AT THEIR BASIC ELEMENT FORMS.':
  'RESET EVERY WEAPON\'S ELEMENT UPGRADES. RETURN TO BASIC FORMS. SPEND YOUR '+I.earned+' UPGRADE POINTS AGAIN.');
 hf23Text(msg,{x:x+112,y:y+87,w:230,h:109},13,'#ecf6ff');
 hf23Text('FEE '+I.fee+' FP / HAVE '+I.balance,{x:x+30,y:y+222,w:182,h:32},12,'#ffce7b');
 hf23Text(I.earned+' POINTS TO REASSIGN',{x:x+244,y:y+222,w:180,h:32},12,'#7ee8ff');
 const enabled=I.hasForms&&I.balance>=I.fee;
 hf23Text(enabled?'PAY '+I.fee+' FP + RESET':I.hasForms?'NEED '+I.fee+' FP':'NO UPGRADES TO RESET',{x:x+31,y:y+279,w:232,h:31},13,enabled&&M.sel===0?'#ffdc87':'#9baaba');
 hf23Text('CANCEL',{x:x+286,y:y+279,w:135,h:31},13,M.sel===1?'#ffdc87':'#d4dfec');
 if(M.sel===0&&enabled)drawSelArrow(x+32,y+291,12,false,'g');else if(M.sel===1)drawSelArrow(x+286,y+291,12,false,'g');
 hf23Text('STAGE PROGRESS AND BASE WEAPONS ARE KEPT',{x:28,y:435,w:424,h:22},12,'#8fdbf1');
 controlHintRow([['pad_dpad','CHOOSE'],['pad_a','CONFIRM'],['pad_b','CANCEL']]);ctx.restore();
 const mouse=Input.mouse||{},click=mouse.down&&!M.md;M.md=!!mouse.down;const mx=sm22MouseX(),my=sm22MouseY();
 if(M.t<.25)return;
 if(Input.menuBack()||sm22StartTap()){hf23Close();return;}
 if(Input.menuLeft()||Input.menuRight()||Input.menuUp()||Input.menuDown())M.sel=1-M.sel;
 const hit=my>=y+274&&my<=y+315?(mx>=x+31&&mx<=x+263?0:mx>=x+286&&mx<=x+421?1:-1):-1;
 if(Input.consumeMouseMoved()&&hit>=0)M.sel=hit;
 if(click&&hit>=0)M.sel=hit;
 if(Input.menuConfirm()||(click&&hit>=0)){
  if(M.sel===1){hf23Close();return;}
  const r=hf23PayReset();M.msg=r==='ok'?'BUILD RESET. '+I.earned+' UPGRADE POINTS ARE READY AT THE FORGE.':r==='poor'?'NOT ENOUGH FURIOUS POINTS. NO CHARGE MADE.':r==='bare'?'YOUR WEAPONS ARE ALREADY BASIC.':"COULD NOT SAVE. NO CHARGE MADE. PLEASE TRY AGAIN.";
  if(r==='ok')M.sel=1;M.t=0;try{fsx(r==='ok'?'powerup':'blocked');}catch(_s){}
 }
}
/* Draw fixed authored world sprites. Only the existing whole-map camera scales them. */
uc22DrawRegion=function(){hf23Warm();hf23Blit('hf23_forge',UC22.pos.x-128,UC22.pos.y-128);
 if(sselBoot===0)campText('THE FORGE',UC22.pos.x,UC22.pos.y-132,10/Math.max(.05,cmap2.cam.z),UC22.focus?'#ffd17a':'#e7f4ff');};
map4eRegion=function(k){if(k!=='hq')return UC22_REGION.apply(this,arguments);hf23Warm();const p=cmap2World('hq');hf23Blit('hf23_hq',p.x-128,p.y-128);
 if(sselBoot===0)campText('FURY HQ',p.x,p.y-132,10/Math.max(.05,cmap2.cam.z),'#82e7ff');if(!uc22Off())uc22DrawRegion();};
uc22Choose=function(i){
 if(i===3){uc22Close();return;}if(i===2){hf23Open();return;}
 hf23Budget();UC22.open=false;UC22.frame=null;Input.clearTaps();
 if(i===0)forgeStart(uc22Return);else loadoutStart(uc22Return);
};
uc22Draw=function(dt){
 const P=UC22;P.t+=Number.isFinite(dt)?dt:1/60;HF23.layout=[];hf23Warm();hf23Backdrop(P.frame);
 hf23Blit('hf23_workshop',12,68);
 hf23Text("DECKER'S WORKSHOP",{x:50,y:87,w:380,h:27},19,'#ffd17a');
 const I=hf23Info();hf23Text('FORGE / LOADOUT / RE-SPEC',{x:50,y:119,w:380,h:24},12,'#a5dfee');
 const mouse=Input.mouse||{},click=mouse.down&&!P.md;P.md=!!mouse.down;const mx=sm22MouseX(),my=sm22MouseY();let hit=-1;
 if(P.t>.2){if(Input.menuDown())P.sel=(P.sel+1)%4;if(Input.menuUp())P.sel=(P.sel+3)%4;}
 for(let i=0;i<4;i++){const cy=174+i*49;hf23Button(240,cy,UC22_ROWS[i],P.sel===i);if(Math.abs(mx-240)<162&&Math.abs(my-cy)<20)hit=i;}
 hf23Text(I.left+' / '+I.earned+' UPGRADE POINTS AVAILABLE',{x:40,y:364,w:400,h:22},12,'#8fe7ff');
 hf23Text('RE-SPEC FEE '+I.fee+' FP / BALANCE '+I.balance+' FP',{x:40,y:391,w:400,h:22},11,'#d0b986');
 controlHintRow([['pad_dpad','CHOOSE'],['pad_a','ENTER'],['pad_b','LEAVE']]);ctx.restore();
 if(P.t<.25)return;if(Input.menuBack()||sm22StartTap()){uc22Close();return;}
 if(Input.consumeMouseMoved()&&hit>=0)P.sel=hit;
 if(click&&hit>=0){uc22Choose(hit);return;}if(Input.menuConfirm())uc22Choose(P.sel);
};
/* A modal consumes all input before the Forge/Loadout behind it can read it. */
for(const name of ['drawForge','drawLoadout']){
 const base=name==='drawForge'?drawForge:drawLoadout;
 const draw=function(dt){if(HF23.modal)return hf23Draw(dt);
  const S=name==='drawForge'?forge:loadoutScr,active=name==='drawForge'?GS.FORGE:GS.LOADOUT;
  const m=Input.mouse||{},cx=(typeof cutsceneViewWidth==='function'?cutsceneViewWidth():VW)/2,cy=VH*.88;
  if(S&&S.row===0&&(S.t||0)>.6&&state===active){
   const click=m.down&&!S.md&&Math.abs(m.x-cx)<80&&Math.abs(m.y-cy)<15;
   if((keybind.charge||[]).some(k=>Input.tap(k))||click){if(click)S.md=true;hf23Open();return hf23Draw(0);}
  }
  const r=base.apply(this,arguments);if(S&&state===active&&S.row===0)hf23Button(cx,cy,'RE-SPEC',false,true,true);return r;
 };
 if(name==='drawForge')drawForge=draw;else drawLoadout=draw;
}
HF23.base.scene=drawScene;
drawScene=function(dt){if(HF23.modal){if(typeof window!=='undefined')window.__bofFrames=(window.__bofFrames|0)+1;return hf23Draw(dt);}return HF23.base.scene.apply(this,arguments);};
HF23.base.backTick=menuBackTick;
menuBackTick=function(){if(HF23.modal)return false;return HF23.base.backTick.apply(this,arguments);};
HF23.base.footer=menuControlFooter;
menuControlFooter=function(){if(HF23.modal)return;return HF23.base.footer.apply(this,arguments);};
/* Claude's Start-menu routes, with authored button states rather than runtime tint/glow/fades. */
sm22DrawRoot=function(dt){
 const P=SM22,m=Input.mouse||{};HF23.layout=[];hf23Warm();
 if(P.t>.25){if(Input.menuDown())P.sel=(P.sel+1)%6;if(Input.menuUp())P.sel=(P.sel+5)%6;}
 hf23Text('MENU',{x:90,y:40,w:300,h:35},26,'#ff7a6c');
 const mx=sm22MouseX(),my=sm22MouseY();let hit=-1;
 for(let i=0;i<6;i++){const y=118+i*48,off=!!sm22Why(i),selected=P.sel===i;
  hf23Blit('hf23_start_'+(off?'disabled':selected?'selected':'idle'),90,y-17);
  hf23Text(SM22_ROWS[i],{x:120,y:y-12,w:258,h:24},12,off?'#8d939d':selected?'#ffd0c8':'#dce5ef');
  if(m.inside&&Math.abs(mx-240)<150&&Math.abs(my-y)<17)hit=i;
 }
 if(Input.consumeMouseMoved()&&hit>=0)P.sel=hit;
 const click=m.down&&!P.md;P.md=!!m.down;const why=P.msgT>0?P.msg:sm22Why(P.sel);
 if(why)hf23Text(why,{x:30,y:421,w:420,h:34},11,'#ffad92');
 if(Input.menuBack()||sm22StartTap()){sm22Close();return;}
 if(P.t>.85&&((click&&hit>=0)||Input.menuConfirm()))sm22Choose(click&&hit>=0?hit:P.sel);
};
sm22Draw=function(dt){dt=Number.isFinite(dt)?dt:1/60;SM22.t+=dt;if(SM22.msgT>0)SM22.msgT-=dt;hf23Backdrop(null);
 if(SM22.mode==='options'){if(Input.menuBack()&&!(typeof rebindAction!=='undefined'&&rebindAction))optCancel();else drawOptions(0);}
 else if(SM22.mode==='save'||SM22.mode==='load')sm22DrawSlots(dt);else sm22DrawRoot(dt);ctx.restore();};
window.BOF_HQ_FORGE=HF23;hf23Warm();
