"""Fit the Loadout catalog into a readable one-weapon element page."""
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "assets/game.js"
raw = path.read_bytes()
assert b"\r\n" not in raw, "game.js must remain LF"
src = raw.decode("utf-8")
first = src.index("  /* Six authored badges per row, across two pages: BASE plus five of the nine elements.")
last = src.index("  if(L.row===2&&selW!=null)opts=weaponFormOptions", first)
block = """  /* One weapon at a time gives its badges and states readable room on the authored
     Loadout plate. D-pad L/R chooses a weapon; U/D traverses BASE and the two element pages. */
  const allW=WEAPONS.map((_,i)=>i),elements=Object.keys(INFUSIONS),visible=1;
  L.catSel=clamp(L.catSel|0,0,allW.length-1);
  L.catCol=clamp(L.catCol|0,0,elements.length);
  L.cat=clamp(L.cat|0,0,allW.length-1);
  if(L.row===1)L.cat=L.catSel;
  const page=Math.floor(Math.max(0,L.catCol-1)/5),pageElems=elements.slice(page*5,page*5+5);
  L.catalogRects=[];
  if(L.row!==2){
    const ri=L.cat,w=allW[ri],owned=L.pool.indexOf(w)>=0,focused=L.row===1&&L.catSel===ri;
    const cy=B[1]+B[3]*.52,pitch=B[2]*.145,x0=B[0]+B[2]*.13,h=Math.min(31,B[3]*.46);
    if(focused){ctx.save();ctx.globalAlpha=.65+.25*Math.sin(t*8);ctx.strokeStyle='#ffd24a';
      ctx.shadowColor='#ffce57';ctx.shadowBlur=13;ctx.lineWidth=2;
      ctx.strokeRect(B[0]+2,B[1]+2,B[2]-4,B[3]-4);ctx.restore();}
    if(art){
      const heading='WEAPON '+(ri+1)+'/'+allW.length+'   '+weaponDisplayName(w)+'   ELEMENTS '+(page+1)+'/2';
      stageText(art,heading,B[0]+B[2]*.5,B[1]+B[3]*.12,
        Math.min(9,stageFitH(art,heading,B[2]*.91,9,6,.04)),owned?'#ffe099':'#8795a9',.9,1,.04);
    }
    const forms=forgeFormsFor(w),cells=[{key:weaponIconKey(w,3,{bare:1}),ok:owned,name:'BASE',kind:'bare'}];
    for(const e of pageElems){const f=forms[e],earned=forgeComboOwned(e,w);
      cells.push({key:f?forgeBadgeKey(e,w,f.lv):'inf_'+e,ok:owned&&!!f,name:INFUSIONS[e].name,elem:e,kind:'forge',earned:earned,price:earned&&!f?forgeComboCost():0});}
    for(let ci=0;ci<cells.length;ci++){
      const c=cells[ci],cx=x0+ci*pitch,col=ci+page*5*(ci>0),selected=focused&&L.catCol===col;
      forgeIconFit(c.key,cx,cy,h,0,c.ok?1:.25);
      if(selected){ctx.save();ctx.globalAlpha=.84+.16*Math.sin(t*13);
        ctx.shadowColor=c.ok?'#ffd24a':'#7bb0d7';ctx.shadowBlur=13;
        ctx.strokeStyle=c.ok?'#ffe089':'#7bb0d7';ctx.lineWidth=2;
        ctx.strokeRect(cx-h*.58,cy-h*.58,h*1.16,h*1.16);ctx.restore();}
      if(art)stageText(art,c.name,cx,B[1]+B[3]*.86,
        Math.min(7.5,stageFitH(art,c.name,pitch*.93,7.5,4.5,.025)),
        c.ok?'#dceaff':'#8292a7',.82,1,.025);
      L.catalogRects.push({x:cx-pitch*.48,y:cy-h*.65,w:pitch*.96,h:h*1.9,
        weapon:w,ri:ri,col:col,cell:c});
    }
  }
  if(art&&L.row!==2){
    const r=(L.catalogRects||[]).find(q=>q.ri===L.catSel&&q.col===L.catCol),c=r&&r.cell;
    if(c){const status=c.ok?'OWNED':(c.price?'ARMORY '+c.price+' FP':(c.earned?'ARMORY RECIPE':'BOSS LOCKED'));
      const detail=L.msgT>0?L.msg:weaponDisplayName(r.weapon)+' + '+c.name+'  -  '+status;
      const dy=H*.627,dw=W*.76,dh=H*.037;
      ctx.save();ctx.globalAlpha=.92;ctx.fillStyle='#08101c';ctx.fillRect((W-dw)/2,dy-dh*.5,dw,dh);
      ctx.strokeStyle=c.ok?'#d9a83f':'#5b879f';ctx.lineWidth=1;ctx.strokeRect((W-dw)/2,dy-dh*.5,dw,dh);ctx.restore();
      stageText(art,detail,W*.5,dy,Math.min(9,stageFitH(art,detail,dw*.96,9,6,.04)),
        L.msgT>0?'#ffffff':(c.ok?'#ffe18b':'#b2c7da'),.9,1,.04);}
  }
"""
src = src[:first] + block + src[last:]
src = src.replace("[['pad_dpad','WEAPON / ELEMENT'],['pad_a','EQUIP']", "[['pad_dpad','L/R WEAPON U/D ELEMENT'],['pad_a','EQUIP']", 1)
path.write_bytes(src.encode("utf-8"))
print("Paged Loadout catalog to one readable weapon row with selected-cell glow")
