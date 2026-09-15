const fs=require('fs'),path=require('path');
const ROOT=path.resolve(__dirname,'..'),GAME=path.join(ROOT,'assets','game.js');
const REC=path.join(ROOT,'_shots','shared_nonlaser_warning_0915','recovery');
function count(s,n){let c=0,i=0;while((i=s.indexOf(n,i))!==-1){c++;i+=n.length;}return c;}
function once(s,a,b,label){const n=count(s,a);if(n!==1)throw new Error(`${label}: ${n} matches`);return s.replace(a,b);}
let s=fs.readFileSync(GAME,'utf8');if(s.includes('\r\n'))throw new Error('game.js lost LF discipline');
fs.mkdirSync(REC,{recursive:true});fs.writeFileSync(path.join(REC,'game_before_alert_layer.js'),s,'utf8');
s=once(s,
`      combatWarningDraw(b,{x:hub[0],y:hub[1],ex:T.lane,ey:VH,progress:p,width:42});
`,
`      combatWarningDraw(b,{x:hub[0],y:hub[1],ex:T.lane,ey:VH,progress:p,width:42,fieldOnly:true});
`, 'field layer');
s=once(s,
`    const _drawPodFlash=()=>{
      for(const [tk,ox] of [['_mzlT',-48],['_mzrT',46]]){
        const t=b[tk]; if(!(t>0)) continue;
        const fi=Math.min(6, ((0.32-t)/0.32*7)|0);
        const fk='mlaunch_'+fi; if(!XART.rdy(fk)) continue;
        const p=ovMount(b, ox, 41), fs=40;
        ctx.drawImage(XART.get(fk), p[0]-fs/2, p[1]-fs*0.08, fs, fs);
      }
    };
`,
`    const _drawPodFlash=()=>{
      for(const [tk,ox] of [['_mzlT',-48],['_mzrT',46]]){
        const t=b[tk]; if(!(t>0)) continue;
        const fi=Math.min(6, ((0.32-t)/0.32*7)|0);
        const fk='mlaunch_'+fi; if(!XART.rdy(fk)) continue;
        const p=ovMount(b, ox, 41), fs=40;
        ctx.drawImage(XART.get(fk), p[0]-fs/2, p[1]-fs*0.08, fs, fs);
      }
    };
    const _drawChargeAlert=()=>{
      if(b._ovState!=='chargeTell'||!b._chargeTell)return;
      const T=b._chargeTell,p=clamp(T.t/T.dur,0,1),hub=ovMount(b,0,4);
      combatWarningDraw(b,{x:hub[0],y:hub[1],ex:T.lane,ey:VH,progress:p,width:42,alertOnly:true});
    };
`, 'alert overlay helper');
s=once(s,
`      ctx.restore();
      b._pivot = piv*0.93;                              // ease pivot back to level (per-frame decay)
      return;
`,
`      ctx.restore();
      _drawChargeAlert();
      b._pivot = piv*0.93;                              // ease pivot back to level (per-frame decay)
      return;
`, 'banked alert overlay');
s=once(s,
`    if(b.flash>0){ const tc=xartTint(bodyKey,hitFlashColor(b,b.flash>0.04?'#ffffff':'#ff8a4a'),0.85); if(tc) ctx.drawImage(tc,dx-w/2,yy-h/2,w,h); }
    return;
  }
  // MEGA BOSSES`,
`    if(b.flash>0){ const tc=xartTint(bodyKey,hitFlashColor(b,b.flash>0.04?'#ffffff':'#ff8a4a'),0.85); if(tc) ctx.drawImage(tc,dx-w/2,yy-h/2,w,h); }
    _drawChargeAlert();
    return;
  }
  // MEGA BOSSES`, 'level alert overlay');
s=once(s,
`function combatWarningDraw(owner,q){
  if(!owner||!q||q.progress==null)return;
  const k=clamp(q.progress,0,1),a=Math.atan2(q.ey-q.y,q.ex-q.x),p={x:q.x,y:q.y},
    B={family:'rime',angles:[a],t:(owner.t||stateT||0),warm:1,released:false};
  ctx.save();ctx.translate(p.x,p.y);ctx.rotate(a-Math.PI/2);
  l23FovDraw(owner,B,0,p,k,q.width||20);ctx.restore();
  B.t=k;l23WarnSymbolDraw(owner,B);
}
`,
`function combatWarningDraw(owner,q){
  if(!owner||!q||q.progress==null)return;
  const k=clamp(q.progress,0,1),a=Math.atan2(q.ey-q.y,q.ex-q.x),p={x:q.x,y:q.y},
    B={family:'rime',angles:[a],t:(owner.t||stateT||0),warm:1,released:false};
  if(!q.alertOnly){ctx.save();ctx.translate(p.x,p.y);ctx.rotate(a-Math.PI/2);
    l23FovDraw(owner,B,0,p,k,q.width||20);ctx.restore();}
  B.t=k;if(!q.fieldOnly)l23WarnSymbolDraw(owner,B);
}
`, 'split warning layers');
if(s.includes('\r\n'))throw new Error('patch introduced CRLF');fs.writeFileSync(GAME,s,'utf8');
console.log('layered Overlord field below hull and alert above hull');
