from pathlib import Path
import hashlib,json
R=Path(r'D:\BOF-Downloads\2026-11-14\RevG-source');f=R/'assets/game.js';raw=f.read_bytes();assert b'\r\n'not in raw
S=R/'_ART_SOURCES/release_qa_1116';(S/'game.js.before').write_bytes(raw);s=raw.decode('utf8')
a="""  const _padHeld={};
  function pollGamepad(){"""
b="""  const _padHeld={};
  // In co-op a missing device leaves its seat empty. Compacting the live-pad
  // list on every poll transfers the surviving wingman's pad to player one.
  const _padSeats=[null,null];let _padWasCoop=false;
  function pollGamepad(){"""
assert a in s;s=s.replace(a,b,1)
a="""    const live=[];
    for(let i=0;i<(pads?pads.length:0);i++){ if(pads[i]) live.push(pads[i]); }
    const gp=live[0], gp2=live[1];
    if(!gp){gpConnected=false;for(const k in _padHeld){_padHeld[k]=false;keys[k]=false;pressed[k]=false;}return;}
    gpConnected=true;"""
b="""    const live=[],indexes=[];
    for(let i=0;i<(pads?pads.length:0);i++){if(pads[i]&&pads[i].connected!==false){live.push(pads[i]);indexes.push(i);}}
    const party=typeof coopOn!=='undefined'&&coopOn;let gp,gp2;
    if(party){
      if(!_padWasCoop){_padSeats[0]=null;_padSeats[1]=null;}
      const assigned=_padSeats.map(i=>i!=null&&live.includes(pads[i])?pads[i]:null),used=new Set(assigned.filter(Boolean));
      const available=live.filter(p=>!used.has(p));
      for(let seat=0;seat<2;seat++)if(!assigned[seat]&&available.length){const next=available.shift();assigned[seat]=next;_padSeats[seat]=indexes[live.indexOf(next)];}
      gp=assigned[0];gp2=assigned[1];
    }else{gp=live[0];gp2=live[1];_padSeats[0]=_padSeats[1]=null;}
    _padWasCoop=party;
    if(!gp&&!gp2){gpConnected=false;for(const k in _padHeld){_padHeld[k]=false;keys[k]=false;pressed[k]=false;}return;}
    gpConnected=true;"""
assert a in s;s=s.replace(a,b,1)
a="""    padInto(gp,'pad_',setk);
  }""";b="""    if(gp)padInto(gp,'pad_',setk);else for(const k in _padHeld)if(k.startsWith('pad_'))setk(k,false);
  }""";assert a in s;s=s.replace(a,b,1)
f.write_text(s,encoding='utf8',newline='\n');assert b'\r\n'not in f.read_bytes()
(S/'pad-seat-change.json').write_text(json.dumps({'file':'assets/game.js','before':hashlib.sha256(raw).hexdigest(),'after':hashlib.sha256(f.read_bytes()).hexdigest(),'scope':'Only native controller seat reservation and missing-device key release. Solo first-present mapping remains.'},indent=2),encoding='utf8');print('Fixed persistent native co-op controller seats; retained LF.')
