module.exports=function(vm,ctxv,ok){
 const fs=require('fs'),path=require('path');
 vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/campaign_flags_art_1004f.js'),'utf8'),ctxv,{filename:'campaign_flags_art_1004f.js'});
 vm.runInContext(fs.readFileSync(path.join(__dirname,'../assets/campaign_landscape_1004e.js'),'utf8'),ctxv,{filename:'campaign_landscape_1004e.js'});
 console.log('=== Connected campaign landscape, authored geography and shared navigation ===');
 const out=JSON.parse(vm.runInContext(`JSON.stringify((()=>{
 const out={};run.mode='campaign';campaign.unlockedMax=8;campaign.bonusUnlocked=false;campaign.stageX1004=null;CF4.focus=false;CF4.flight=4;
 s9MapCine=null;riftReturn=null;sselUnlockCine=null;openStageSelect(1,{});sselBoot=0;
 const o=map30Overview();
 out['continent overview fits the existing open map band']=MAP4E.landH*o.z<=CM2_BAND_BOT-CM2_BAND_TOP-16+.01&&o.z>0;
 out['all nine mission landmarks are distinct and contained by the expanded world']=Object.values(SSEL_POS).every(p=>p[0]>0&&p[0]<MAP4E.w&&p[1]>0&&p[1]<MAP4E.h)&&new Set(Object.values(SSEL_POS).map(p=>p.join(','))).size===9;
 out['original blue ocean and original stage flags remain registered']=XART._src.cm2_ocean.includes('ocean')&&!!XART._src.nss_flag1_av;
 out['all nine Roman flags share measured mast-base anchors']=Object.values(MAP4F_FLAGS).map(f=>f.roman).join(',')==='I,II,III,IV,V,VI,VII,VIII,IX'&&Object.values(MAP4F_FLAGS).every(f=>f.anchor[0]>0&&f.anchor[0]<1&&f.anchor[1]>.9);
 out['every flag state is registered without changing the original atlas']=Object.keys(MAP4F_FLAGS).every(n=>MAP4F_FLAG_STATES.every(v=>XART._src['map4f_flag'+n+'_'+v]?.endsWith('flag_'+n+'_'+v+'.png')));
 out['the bonus rift is northeast of the glacier region']=SSEL_POS[9][0]>SSEL_POS[3][0]&&SSEL_POS[9][1]<SSEL_POS[3][1];
 const path=[1];let selected=1;for(const direction of [1,1,1,1,-1,-1,-1]){selected=sselMoveHorizontal(direction,1,8,selected);path.push(selected);}
 out['horizontal D-pad navigation can reach every campaign stage']=path.join(',')==='1,2,3,4,5,6,7,8';
 out['locked portal still uses the campaign bonus latch']=!cmap2Unlocked(9);campaign.bonusUnlocked=true;
 out['earned bonus portal opens through the existing latch']=cmap2Unlocked(9);campaign.bonusUnlocked=false;
 out['Stage X flight fits both the city and departed Stage 6 region']=cmap2Frame(6,'hub').z>0&&cmap2Frame(6,'hub').z<.34;
 const keys=MAP4E.keys.flatMap(k=>['','_lock','_shadow','_glow'].map(v=>'map4e_region_'+k+v));
 out['every generated region state has a fresh explicit asset key']=keys.every(k=>XART._src[k]?.startsWith(k.startsWith('map4e_region_hq')?'assets/game/campaign_landscape_1004f/':k.startsWith('map4e_region_hub')?'assets/game/campaign_stagex_1004g/':'assets/game/campaign_landscape_1004e/'));
 const hub=map4eHubPose(),marker=map4eStageXPoint(),orbit=fr27CoreMapPosition(),expectedOrbit=cmap2ToScreen(hub.x,hub.y-80);
 out['Stage X floats above its fixed landscape anchor']=cmap2World('hub').y-hub.y>100;
 out['Stage X flag and fighter orbits share the floating city pose']=marker.y===hub.y+55&&Math.abs(orbit.y-expectedOrbit.y)<.001;
 out['the floating island itself is inspectable by pointer']=map4eStageXAt(...Object.values(cmap2ToScreen(hub.x,hub.y)));
 const routes=[[4,5,Math.PI],[7,8,0],[8,1,0]];
 const savedMove=Audio.SFX.mapMove;let moves=0;Audio.SFX.mapMove=()=>moves++;
 for(const [from,to,head] of routes){
  const p=sselFlagXY(from);sselShip={...p,t:0,phase:'idle',trail:0,cur:from,head:Math.PI/2};sselCursor=to;particles=[];
  sselShipUpdate(1/60);const flash=particles[0];
  out['ship holds the requested heading on '+from+' to '+to]=sselShip.head===head;
  out['engine trail stays behind the vertical ship on '+from+' to '+to]=head===0?flash.y>sselShip.y:flash.y<sselShip.y;
  for(let i=0;i<180;i++)sselShipUpdate(1/60);
  out['terrain bobbing preserves the arrival heading on '+from+' to '+to]=sselShip.head===head;
 }
 out['each selection emits one map move cue, never a frame loop']=moves===3;Audio.SFX.mapMove=savedMove;
 out['Stage X is visible but cannot launch without a pending encounter']=!!XART._src.map4f_flagx&&!cf4LaunchX();
 campaign.unlockedMax=1;openStageSelect(1,{});out['opening the map preserves campaign locks']=campaign.unlockedMax===1&&!campaign.bonusUnlocked;
 return out;
})())`,ctxv));
 for(const [name,pass] of Object.entries(out))ok(pass,name);
 const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,'../assets/game/campaign_landscape_1004e/manifest.json'),'utf8'));
 ok(manifest.sources.length===4&&manifest.sources.every(s=>s.sha256.length===64),'all four authored generation sources have archived hashes');
 const currentFiles=JSON.parse(vm.runInContext('JSON.stringify(MAP4E.keys.flatMap(k=>[\"\",\"_lock\",\"_shadow\",\"_glow\"].map(v=>XART._src[\"map4e_region_\"+k+v])).concat(XART._src.map4e_landscape))',ctxv));
 ok(currentFiles.every(f=>typeof f==='string'&&fs.existsSync(path.join(__dirname,'..',f))),'every currently registered terrain and landmark output exists');
};
