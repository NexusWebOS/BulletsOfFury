from pathlib import Path

path = Path('assets/game.js')
data = path.read_bytes()
assert b'\r\n' not in data
old = b"_jet:{angle:Math.PI,baseAngle:Math.PI,active:false,state:'',cue:null,cooldown:0,\n        passes:0,greens:0,thrusts:0},\n      _duoLite:{phase:'entry',t:0,homeX:i?0.68:0.32,homeY:154,shots:0}};"
new = b"_jet:{angle:Math.PI,baseAngle:Math.PI,active:false,state:'',cue:null,cooldown:0,\n        passes:0,greens:0,thrusts:0}};"
assert data.count(old) == 1
data = data.replace(old, new)
old = b"    s.damage=function(n){\n      if(!this.vulnerable||this.gone||!(n>0))return;\n      this.hitFlash=.045;this.hp=Math.max(0,this.hp-n);\n      if(!this.hp){this.phase='death';this.t=0;this.st=0;this.vulnerable=false;this.beams=[];this.events.push('impact');}\n    };\n"
assert data.count(old) == 1
data = data.replace(old, b'')
path.write_bytes(data)
