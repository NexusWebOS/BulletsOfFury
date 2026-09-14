from pathlib import Path
root=Path(__file__).resolve().parents[2];p=root/'assets/game.js';g=p.read_bytes().decode('utf-8')
old="function tempestPortXY(b,i){ const p=TLV_PORTS[i]; return {x:b.x+p[0]*TLV_S, y:b.y+p[1]*TLV_S}; }"
new="""function tempestPortXY(b,i){
  const p=TLV_PORTS[i],x=p[0]*TLV_S,y=p[1]*TLV_S;
  const a=b._jet&&!b._jetLocalDraw?b._jet.angle:0;
  return {x:b.x+x*Math.cos(a)-y*Math.sin(a),y:b.y+x*Math.sin(a)+y*Math.cos(a)};
}"""
assert g.count(old)==1;g=g.replace(old,new)
old="    enemyMachineShotHeavy:'assets/game/sounds/enemy_machine_shot_heavy.wav',"
new=old+"""
    tlvJetCharge:'assets/game/sounds/boss_weapon_charge.wav',
    tlvJetReady:'assets/game/sounds/retina_charge.mp3',
    tlvJetTurn:'assets/game/sounds/nsp_rcs_thruster.mp3',
    tlvJetThrust:'assets/game/sounds/nsp_booster_ignite.mp3',
    tlvJetEngine:'assets/game/sounds/nsp_engine_loop.mp3',
    tlvJetBrake:'assets/game/sounds/brake.wav',"""
assert g.count(old)==1;g=g.replace(old,new)
old="    enemyMachineShotHeavy:{g:0.50, lp:6800, min:0.15},"
new=old+"""
    tlvJetCharge:{g:0.60,lp:5200,min:0.70},
    tlvJetReady:{g:0.35,lp:6200,min:0.50},
    tlvJetTurn:{g:0.46,lp:5200,min:0.25},
    tlvJetThrust:{g:0.78,lp:6200,min:0.65},
    tlvJetEngine:{g:0.68,native:true},
    tlvJetBrake:{g:0.42,lp:4800,min:0.60},"""
assert g.count(old)==1;g=g.replace(old,new)
p.write_bytes(g.encode('utf-8'))
print('Rotating authored hardpoints and dedicated, gated engine sound aliases installed.')
