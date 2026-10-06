"use strict";
/* Mike requested every current/new code pinned in the game. This is a reference
   and entry picker; it never submits, launches a fight, grants an unlock or saves. */
const PC5_BASE={draw:drawPassword,hotspots:pwHotspots,key:pwKey,text:passwordStageText,back:menuBackTick,state:setState};
const PC5={open:false,page:0,row:0,md:false,rendered:[]};
function pc5Pages(){
 const groups=[],seen=new Set();
 const add=(title,rows)=>{rows=rows.filter(r=>!seen.has(r[0]));for(const r of rows)seen.add(r[0]);
  for(let i=0;i<rows.length;i+=9)groups.push({title,rows:rows.slice(i,i+9)});};
 add('STAGES',Object.entries({FURY:1,IRON:2,DAM5:3,STRM:4,ORBT:5,TURB:6,SEWR:7,DETH:8,RIFT9:9}).filter(([c])=>PASSWORDS[c]).map(([c,n])=>[c,'STAGE '+n]));
 add('SKY ENCOUNTERS',[['HARR6','STAGE 6 HARRIER'],['REBEL6','STAGE 6 REBELS'],['XHARR','STAGE X HARRIER'],['XREBEL','STAGE X REBELS']].filter(([c])=>PASSWORDS[c]));
 add('BOSSES',Object.entries(ON5_CODES).filter(([,e])=>e.role==='boss'&&e.phase==null).map(([c,e])=>[c,'STAGE '+e.stage+' BOSS']));
 add('MINIBOSSES',Object.entries(ON5_CODES).filter(([,e])=>e.role==='mini').map(([c,e])=>[c,'STAGE '+e.stage+' MINIBOSS']));
 add('ALTERNATE FIGHTS',Object.entries(ON5_CODES).filter(([,e])=>e.role==='alt').map(([c,e])=>[c,{ALT3:'RIME WALL',ALT6:'BLACKSTEEL',ALT8:'HERALD ALTERNATE'}[c]||'STAGE '+e.stage+' ALTERNATE']).concat([['HAMMER','HAMMER MUSIC FIGHT'],['HAMA','HAMA MUSIC FIGHT']]));
 add('FINAL BOSS PHASES',Object.entries(ON5_CODES).filter(([,e])=>e.phase!=null&&e.mimic==null).map(([c,e])=>[c,['MUTATED DRONE','GHOST','DRACULA / SYMBIOTE'][e.phase]]));
 const names=['MUTATED DRONE','HELICOPTER','FURNACE','CRYO','STORM','SWORD / SHIELD KNIGHT','ACE','WARDEN','CODE HAMMER'];
 add('FINAL BOSS COPIES',Object.entries(ON5_CODES).filter(([,e])=>e.mimic!=null).map(([c,e])=>[c,names[e.mimic]]));
 add('UNLOCKS',[['COLE4U','UNLOCK COLE'],['BOMBER','UNLOCK LIZZIE BOMBER'],['SPCBOY','TOGGLE CLASSIC FURYSHIP']]);
 add('COLE SCENE PREVIEWS',Object.entries(COLE_SCENE).map(([c,n])=>[c,n===9?'FINAL OUTRO PREVIEW':'STAGE '+n+' OUTRO PREVIEW']));
 add('OTHER STAGE CODES',Object.entries(PASSWORDS).filter(([c])=>!seen.has(c)).map(([c,n])=>[c,'STAGE '+n+' ENTRY']));
 return groups;
}
function pc5Open(){PC5.open=true;PC5.page=clamp(PC5.page,0,pc5Pages().length-1);PC5.row=0;PC5.md=Input.mouse.down;_pwTyped=[];drawPassword.typing=false;Audio.SFX.select?.();}
function pc5Close(code){PC5.open=false;_pwTyped=[];drawPassword.typing=false;drawPassword._md=Input.mouse.down;PC5.md=Input.mouse.down;
 if(code){pwInput=code;drawPassword.sel=-1;drawPassword.err=0;}Input.clearTaps?.();Audio.SFX.select?.();}
function pc5Turn(dir){const pages=pc5Pages();PC5.page=(PC5.page+dir+pages.length)%pages.length;PC5.row=0;Audio.SFX.blip?.();}
function pc5Text(text,x,y,h,width,color,align='center'){
 const art=pilotFont(2),fit=Math.max(11,stageFitH(art,text,width,h,11,.06)),w=stageWidth(art,text,fit,.06);
 const center=align==='left'?x+w/2:x;PC5.rendered.push({text,x:center-w/2,y,w,h:fit});
 PC5_BASE.text(art,text,center,y,fit,width,color,1,.06);
}
function pc5Draw(dt){
 _pwTyped=[];uiFontWarm?.();const pages=pc5Pages();PC5.page=clamp(PC5.page,0,pages.length-1);let page=pages[PC5.page];
 const mx=Input.mouse.x,my=Input.mouse.y,press=Input.mouse.down&&!PC5.md;PC5.md=Input.mouse.down;
 if(Input.menuLeft())pc5Turn(-1);if(Input.menuRight())pc5Turn(1);page=pages[PC5.page];
 if(Input.menuUp()){PC5.row=(PC5.row+page.rows.length-1)%page.rows.length;Audio.SFX.blip?.();}
 if(Input.menuDown()){PC5.row=(PC5.row+1)%page.rows.length;Audio.SFX.blip?.();}
 if(press&&my>=42&&my<=74){if(mx<88)pc5Turn(-1);else if(mx>VW-88)pc5Turn(1);page=pages[PC5.page];}
 if(press&&mx>=28&&mx<=VW-28&&my>=100&&my<100+page.rows.length*36){PC5.row=Math.floor((my-100)/36);pc5Close(page.rows[PC5.row][0]);return PC5_BASE.draw(0);}
 if(Input.menuConfirm()){pc5Close(page.rows[PC5.row][0]);return PC5_BASE.draw(0);}
 if(Input.menuBack()){pc5Close();return PC5_BASE.draw(0);}
 if(press&&my>=VH-50&&mx<108){pc5Close();return PC5_BASE.draw(0);}
 drawCanonBackdrop('nbt_3',.62);bofPanel(16,12,VW-32,VH-56);PC5.rendered=[];
 pc5Text('PINNED PASSWORDS',VW/2,29,18,VW-64,'#f3f6ff');
 pc5Text('PREV',55,58,11,60,'#89d9ff');pc5Text(page.title,VW/2,58,13,VW-180,'#ffd36b');pc5Text('NEXT',VW-55,58,11,60,'#89d9ff');
 pc5Text((PC5.page+1)+' / '+pages.length+'   -   '+pages.reduce((n,p)=>n+p.rows.length,0)+' CODES',VW/2,83,11,VW-70,'#b4c8df');
 for(let i=0;i<page.rows.length;i++){const [code,label]=page.rows[i],y=100+i*36;
  if(i===PC5.row){ctx.fillStyle='rgba(67,137,198,.25)';ctx.fillRect(28,y,VW-56,34);}
  pc5Text(label,42,y+17,11,268,i===PC5.row?'#ffffff':'#b7cce2','left');
  pc5Text(code,VW-87,y+17,17,110,'#ffd36b');
 }
 pc5Text('SELECT A CODE TO FILL THE ENTRY BOX',VW/2,VH-68,11,VW-64,'#a6bed8');
 controlHintRow([['pad_dpad','BROWSE'],['pad_a','USE CODE'],['pad_b','BACK']],VH-22);
}
pwHotspots=function(wx,wy,ww,wh){return PC5_BASE.hotspots.apply(this,arguments).concat({c:'__PC5__',x:VW/2-132,y:wy+144,w:264,h:32,wide:true});};
passwordStageText=function(art,text){if(text==='__PC5__')arguments[1]='PINNED PASSWORDS';return PC5_BASE.text.apply(this,arguments);};
pwKey=function(c){if(c==='__PC5__')return pc5Open();return PC5_BASE.key.apply(this,arguments);};
const pc5PasswordDraw=function(dt){
 if(PC5.open)return pc5Draw(dt);
 // Only the physical pad shortcut owns this action. A typed letter C remains C.
 if(!drawPassword.typing&&Input.tapAny((keybind.retina||[]).filter(k=>/^pad_/.test(k)))){pc5Open();return pc5Draw(dt);}
 // Raw keyboard text already owns these taps. The old entry path otherwise
 // deleted twice on Backspace (and could type twice in explicit TYPE mode).
 for(const c of _pwTyped){if(c==='\b')Input.tap('backspace');else if(drawPassword.typing&&/^[A-Z0-9]$/i.test(c))Input.tap(c.toLowerCase());}
 const r=PC5_BASE.draw.apply(this,arguments);if(state===GS.PASSWORD&&PC5.open)pc5Draw(0);return r;
};
Object.assign(pc5PasswordDraw,drawPassword);drawPassword=pc5PasswordDraw;
menuBackTick=function(){if(state===GS.PASSWORD&&PC5.open){if(Input.menuBack()){pc5Close();return true;}return false;}return PC5_BASE.back.apply(this,arguments);};
setState=function(next){if(next!==GS.PASSWORD){PC5.open=false;_pwTyped=[];}return PC5_BASE.state.apply(this,arguments);};
