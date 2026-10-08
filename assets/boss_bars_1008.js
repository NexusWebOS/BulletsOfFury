'use strict';
/* boss_bars_1008.js - Mike, 2026-10-08:
   "the shields no longer get a seperate giant bar, but instead can be the sub bar of a boss bar of our
   generations. #2, hammer boss still gets 2x boss bar. It fills and then fills over in Gray. Stage 8 3rd
   phase boss, same deal. Should stack Red first, then dark gray, then green, then light gray, then yellow,
   then black, then orange, red/purple mix. if any enemies utilize a shield, use the boss bar with the shield
   version. When we switch forms, he gets a full hp bar per form, but that is 1 of his 8 health bars."

   Loaded after player_hud_1008.js. The generated stage frames (enemy_hud_1007c.js, EH7) are the only boss and
   miniboss housings: a shield is the thin sub-bar of the 'bossShield' / 'miniShield' variant, never the old
   separate shield plate, and every shield system the game has reports through bossShieldFrac().

   ⚠ GREYS AND BLACK CANNOT COME FROM xartPalette. It composites in 'color' and keeps the plate's luminosity, so
   '#202020', '#606060' and '#d0d0d0' all render as the SAME mid grey. The grey layers are the authored grey
   plate (bmbar_fill_grey) darkened or lightened by an overlay inside the well's clip. */

const BB8={last:null};
const BB8_BASE={bar:drawHealthBarV2,shield:bossShieldFrac,shieldArt:drawShieldBarArt};

/* Dracodia's stack, bottom to top. Fills go on red first; the last fill (his own body) is on top and is the
   first to drain. Every pool the fight owns is one layer, whatever form it belongs to. */
const BB8_STACK=[
 {name:'red',hex:'#ff2a2a'},
 {name:'dark gray',grey:true,dark:.52},
 {name:'green',hex:'#35d64a'},
 {name:'light gray',grey:true,light:.30},
 {name:'yellow',hex:'#ffd92e'},
 {name:'black',grey:true,dark:.84},
 {name:'orange',hex:'#ff8a1c'},
 {name:'red/purple',hex:'#ff2a3a',stripe:'#9a2cff'},
 {name:'dracodia',hex:'#9b2bd8',glow:'#ff2a6a'}
];

/* ---- shields: every system reports into the generated frame's sub-bar ---- */
bossShieldFrac=function(b){
 const J=b&&typeof j3State==='function'?j3State(b):null,S=b&&b._r30;
 // Dracodia's code wall / knight barrier lives on _r30; the third encounter always wears the shield frame so
 // the housing does not change height every time a wall rises and falls.
 if(J&&J.encounter===2&&S)return clamp((S.shield||0)/Math.max(1,S.shieldMax||1),0,1);
 return BB8_BASE.shield.apply(this,arguments);
};
// The separate giant shield plate is retired. Every caller that still reaches it is covered by the sub-bar.
drawShieldBarArt=function(){return false;};

/* ---- painting inside a measured well ---- */
function bb8Fill(L){
 if(L.grey)return XART.rdy('bmbar_fill_grey')?XART.get('bmbar_fill_grey'):null;
 return XART.rdy('bmbar_fill_solid')?xartPalette('bmbar_fill_solid',L.hex):null;
}
function bb8Paint(L,x,y,w,h,frac){
 const im=bb8Fill(L);frac=clamp(frac||0,0,1);if(!im||frac<=0)return;
 ctx.save();ctx.beginPath();ctx.rect(x,y,w*frac,h);ctx.clip();ctx.imageSmoothingEnabled=true;
 ctx.drawImage(im,x,y,w,h);
 if(L.dark){ctx.fillStyle='rgba(0,0,0,'+L.dark+')';ctx.fillRect(x,y,w,h);}
 if(L.light){ctx.globalCompositeOperation='screen';ctx.fillStyle='rgba(255,255,255,'+L.light+')';ctx.fillRect(x,y,w,h);ctx.globalCompositeOperation='source-over';}
 if(L.stripe){const p=xartPalette('bmbar_fill_solid',L.stripe);if(p){
  // a blend, not candy stripes: the purple laid half over the red, with a slow diagonal sheen of pure purple
  ctx.globalAlpha=.5;ctx.drawImage(p,x,y,w,h);ctx.globalAlpha=.45;
  const off=((typeof stateT!=='undefined'?stateT:0)*18)%(h*4);ctx.beginPath();
  for(let sx=x-h*2+off;sx<x+w;sx+=h*4){ctx.moveTo(sx,y+h);ctx.lineTo(sx+h,y);ctx.lineTo(sx+h*2,y);ctx.lineTo(sx+h,y+h);ctx.closePath();}
  ctx.clip();ctx.drawImage(p,x,y,w,h);ctx.globalAlpha=1;}}
 if(L.glow){ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.20;ctx.fillStyle=L.glow;ctx.fillRect(x,y,w,h*.35);}
 ctx.restore();
}
function bb8Well(){
 const last=typeof EH7!=='undefined'?EH7.lastBoss:null;if(!last)return null;
 const f=eh7Frame(last.theme,last.variant,last.w);if(!f)return null;
 return{x:last.x+f.hp[0],y:last.y+f.hp[1],w:f.hp[2],h:f.hp[3],frame:f,last};
}
/* the second, grey fill: the Hammer's chromium armour, painted over the live HP */
function bb8Armor(W,ratio,t){
 if(!(ratio>0)||!XART.rdy('bmbar_fill_grey'))return;
 const im=XART.get('bmbar_fill_grey');
 ctx.save();ctx.beginPath();ctx.rect(W.x,W.y,W.w*clamp(ratio,0,1),W.h);ctx.clip();ctx.drawImage(im,W.x,W.y,W.w,W.h);
 ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.10+.10*(.5+.5*Math.sin((t||0)*9));ctx.drawImage(im,W.x,W.y,W.w,W.h);ctx.restore();
}
function bb8HammerArmorRatio(p){
 const A=typeof fr27Armor==='function'?fr27Armor(p):null;if(!A)return 0;
 const h=p._hammer;
 if(h.state==='fr_activation'&&typeof FR27_ACT!=='undefined')return clamp((h.t-FR27_ACT.brace)/(FR27_ACT.plate-FR27_ACT.brace),0,1);
 return A.max>0?clamp(A.hp/A.max,0,1):0;
}
/* the stacked gauge: one layer per pool still alive, the active one draining on top */
function bb8Stack(b){
 const J=j3State(b),S=b._r30,n=J.hp.length;
 const intro=['coronation1003j','voidIntro1005'].includes(S.mode);
 if(intro){const G=fmcGauge(b);if(G.charge<0)return{top:-1,under:-1,frac:0,left:0};
  const k=Math.min(BB8_STACK.length-1,G.charge);return{top:k,under:k-1,frac:G.frac,left:k+1};}
 const left=J.hp.filter(h=>h>0).length,top=Math.min(BB8_STACK.length,n,left)-1;
 // between pools (the active one has just hit zero) the next layer shows full
 const live=J.hp[J.active]>0,frac=live?clamp(b.hp/Math.max(1,b.maxhp),0,1):1;
 return{top,under:top-1,frac,left};
}
function bb8Count(W,left){
 // how many of his bars remain, in the stage face on a dark chip at the right end of the well
 if(!(left>0))return;const face=typeof curFontArt==='function'?curFontArt():null,H=Math.max(9,Math.min(13,W.h*1.05));
 const bw=H*2.3,bx=W.x+W.w-bw-2;
 ctx.save();ctx.fillStyle='rgba(6,4,12,.78)';ctx.fillRect(bx,W.y,bw,W.h);
 if(face&&typeof stageText==='function')stageText(face,'X'+left,bx+bw/2,W.y+W.h/2,H,'#ffffff',1,1,0.10);
 ctx.restore();
}
drawHealthBarV2=function(kind,frac,cx,cy,w,inWorld,lagKey){
 const r=BB8_BASE.bar.apply(this,arguments);
 if(!r||kind!=='boss'||typeof boss==='undefined'||!boss||boss._rebels)return r;
 const b=boss,J=typeof j3State==='function'?j3State(b):null,W=bb8Well();if(!W)return r;
 ctx.save();if(inWorld===true&&typeof camX==='number')ctx.translate(camX,0);ctx.globalAlpha*=bossHealthAlpha(b);
 if(J&&J.encounter===2&&b._r30){
  const s=bb8Stack(b);
  // repaint the whole well: the base fills from the older form colours must not show through
  if(s.top>=0){
   ctx.save();ctx.beginPath();ctx.rect(W.x,W.y,W.w,W.h);ctx.clip();
   ctx.drawImage(W.frame.canvas,W.frame.hp[0],W.frame.hp[1],W.w,W.h,W.x,W.y,W.w,W.h);ctx.restore();
   if(s.under>=0)bb8Paint(BB8_STACK[s.under],W.x,W.y,W.w,W.h,1);
   bb8Paint(BB8_STACK[s.top],W.x,W.y,W.w,W.h,s.frac);
  }
  // the Code Hammer copy keeps its armour as the grey second fill, like the real Hammer
  const D=J.mimic===8&&J.gp4Donors?J.gp4Donors[8]:null;
  if(D&&b._r30.mode==='fight')bb8Armor(W,bb8HammerArmorRatio(D.p),D.p._hammer&&D.p._hammer.t);
  bb8Count(W,s.left);
  BB8.last={kind:'stack',top:s.top,under:s.under,frac:s.frac,left:s.left,colour:s.top>=0?BB8_STACK[s.top].name:null};
 }else if(b._hammer&&!b._gp4Host){
  const ratio=bb8HammerArmorRatio(b);bb8Armor(W,ratio,b._hammer.t);
  BB8.last={kind:'hammer',armor:ratio};
 }else BB8.last=null;
 ctx.restore();
 return r;
};
window.BOFBossBars=BB8;
