"""One-shot exact-byte insertion for the Stage-1 campaign flight bridge."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / 'assets/game.js'
data = path.read_bytes()
assert b'\r\n' not in data

def replace(old, new):
    global data
    old, new = old.encode(), new.encode()
    assert data.count(old) == 1, (old[:100], data.count(old))
    data = data.replace(old, new, 1)

replace("  X._src['cinbg_jungle']='assets/game/cinematic_level_approaches/stage01_rumble_in_the_jungle_approach.png';",
        "  X._src['cinbg_jungle']='assets/game/cinematic_level_approaches/stage01_rumble_in_the_jungle_approach.png';\n"
        "  X._src['cinbg_stage1_route']='assets/game/mapJungle.png';")
replace("const dialogueViewW=(typeof state!=='undefined' && state===GS.CAMPAIGNINTRO)?cutsceneViewWidth():VW;",
        "const dialogueViewW=(typeof state!=='undefined' && (state===GS.CAMPAIGNINTRO ||\n"
        "      (state===GS.CUTSCENE && hqMode==='bridge')))?cutsceneViewWidth():VW;")
replace("/* Group HQ scenes remain archived, while live campaign boundaries pass through.\n   The selected pilot narrates Stage 1's return flight in campaignIntro. */\nfunction hqTrigger(when, stage, onDone){\n  if(onDone)onDone();\n  return false;\n}",
        """/* The ensemble HQ scenes remain archived. Stage 1 instead gets a short, top-down
   radio flight on its way back from the dam: the selected ship and one existing pilot.
   It uses the current 16-bit dialogue panel and front-facing comm portraits. */
let campaignBridge=null;
function campaignBridgeStart(onDone){
  const lead=(run&&run.pilot)||((typeof PILOTS!=='undefined'&&PILOTS[pilotIndex])?PILOTS[pilotIndex].key:'axel');
  const wing=lead==='cole'?'axel':'cole';
  campaignBridge={lead:lead,wing:wing,i:0,t:0,md:!!Input.mouse.down};
  hqMode='bridge'; hqSc={beats:[
    {who:lead,text:'Dam is down. The corridor is open.'},
    {who:wing,text:'Copy. Form up on me. The volcanic front is next.'},
    {who:lead,text:'I see it. Staying fast and staying together.'}
  ]};
  hqDone=onDone||null;
  for(const p of [lead,wing]){XART.rdy(cinShipKey(p,1));XART.rdy('dlg_'+p);commPortrait(p,'idle');}
  XART.rdy('cinbg_stage1_route');if(typeof bmfReady==='function')bmfReady('dialogue');
  try{if(Audio&&Audio.startMusic)Audio.startMusic('cinematics');}catch(_cbm){}
  setState(GS.CUTSCENE);return true;
}
function drawCampaignBridge(dt){
  const B=campaignBridge,W=cutsceneViewWidth(),H=VH;
  ctx.fillStyle='#05090d';ctx.fillRect(0,0,W,H);
  if(!B||!hqSc){campaignBridge=null;hqEnd();return;}
  const im=XART.rdy('cinbg_stage1_route')&&XART.get('cinbg_stage1_route');
  const leadReady=XART.rdy(cinShipKey(B.lead,1)),wingReady=XART.rdy(cinShipKey(B.wing,1));
  const faceReady=typeof bmfReady==='function'&&bmfReady('dialogue');
  if(!im||!leadReady||!wingReady||!faceReady)return;
  B.t+=dt;
  const sw=im.naturalWidth||im.width,sh=im.naturalHeight||im.height,srcH=Math.min(sh,H*sw/W);
  const travel=Math.max(0,sh-srcH),sy=Math.round(travel*(.53-.12*clamp((B.i*4+B.t)/12,0,1)));
  ctx.drawImage(im,0,sy,sw,srcH,0,0,W,H);
  ctx.fillStyle='rgba(3,10,17,.22)';ctx.fillRect(0,0,W,H);
  const flight=B.i*4+B.t,bob=Math.sin(flight*2.1)*H*.008;
  cinDrawShip(B.wing,1,W*.66+Math.sin(flight*.7)*W*.012,H*.42-bob,H*.29,false,1,0);
  cinDrawShip(B.lead,1,W*.35+Math.sin(flight*.85)*W*.015,H*.59+bob,H*.34,false,1,0);
  const beat=hqSc.beats[B.i],full=beat.text;
  dlgBox({who:beat.who.toUpperCase(),portrait:beat.who,full:full,
    shown:full.slice(0,Math.floor(B.t*42)),fade:clamp(B.t/.20,0,1),
    tint:(PILOTS.find(p=>p.key===beat.who)||{}).tint||'#dce7ff',
    pw:Math.min(W*.77,910),ph:Math.min(H*.25,145),
    x:Math.round(W*.115),y:Math.round(H*.72),screenSpace:false});
  msgFaceUse('dialogue');controlHintRow([['pad_start','SKIP']],H-20,W/2,W-24);msgFaceUse(null);
  const click=Input.mouse.down&&!B.md;B.md=!!Input.mouse.down;
  if(B.t>=4.0 || (B.t>.4&&(click||(typeof anyTap==='function'&&anyTap())))){
    Input.mouse.down=false;B.i++;B.t=0;
    if(B.i>=hqSc.beats.length){campaignBridge=null;hqEnd();}
  }
}
function hqTrigger(when, stage, onDone){
  if(when==='post' && stage===1 && run.mode==='campaign')return campaignBridgeStart(onDone);
  if(onDone)onDone();
  return false;
}""")
replace("function drawCutsceneState(dt){\n  if(hqMode==='beats') return drawCutsceneBeats(dt);",
        "function drawCutsceneState(dt){\n  if(hqMode==='bridge') return drawCampaignBridge(dt);\n  if(hqMode==='beats') return drawCutsceneBeats(dt);")

assert b'\r\n' not in data
path.write_bytes(data)
