"""Layer existing authored game recordings into distinct weapon cues; no synthesized art/audio."""
import json,subprocess,wave
from pathlib import Path
import numpy as np
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[2]
BANK=ROOT/'assets/game/sounds'
SR=48000
FF=imageio_ffmpeg.get_ffmpeg_exe()
cache={}
def source(name):
    if name not in cache:
        raw=subprocess.check_output([FF,'-v','error','-i',str(BANK/name),'-f','f32le','-ac','1','-ar',str(SR),'-'])
        a=np.frombuffer(raw,dtype='<f4').copy()
        # Strip source leading silence so every attack transient belongs to its frame.
        nz=np.flatnonzero(np.abs(a)>.005)
        if len(nz):a=a[max(0,nz[0]-int(.003*SR)):]
        cache[name]=a/max(.04,float(np.max(np.abs(a))))
    return cache[name]
def mix(name,duration,layers,peak=.72,loop=False):
    n=round(duration*SR);out=np.zeros(n,dtype=np.float64)
    for file,gain,offset,rate in layers:
        a=source(file);a=np.interp(np.arange(0,len(a),rate),np.arange(len(a)),a)
        start=round(offset*SR);count=min(len(a),n-start)
        if count>0:out[start:start+count]+=a[:count]*gain
    fade=min(round(.075*SR),n//4);out[-fade:]*=np.linspace(1,0,fade)
    out[:round(.002*SR)]*=np.linspace(0,1,round(.002*SR))
    if loop:
        # Equal end values and a short overlap remove clicks on every loop wrap.
        c=round(.045*SR);out[:c]=out[:c]*np.linspace(0,1,c)+out[-c:]*np.linspace(1,0,c);out=out[:-c]
    out*=peak/max(.01,float(np.max(np.abs(out))))
    path=BANK/(name+'_0913.wav')
    with wave.open(str(path),'wb')as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((out*32767).astype('<i2').tobytes())
    return {'file':str(path.relative_to(ROOT)).replace('\\','/'),'seconds':len(out)/SR,'peak':float(np.max(np.abs(out))),'rms':float(np.sqrt(np.mean(out*out))),'layers':layers,'loop':loop}
recipes={
 'cole_pressure_start':(.48,[('reviewed_cole_sonic_charge_start.wav',.8,0,.92),('nsp_rcs_thruster.mp3',.20,0,.85)],.64,False),
 'cole_pressure_loop':(1.18,[('reviewed_cole_sonic_charge_loop.wav',.75,0,.9),('ice_breath_loop.wav',.15,0,.75)],.48,True),
 'cole_pressure_release':(.70,[('reviewed_cole_sonic_release.wav',.8,0,.83),('explosion_air_small_02.wav',.23,0,.76)],.76,False),
 'cole_pressure_impact':(.28,[('shield_hit_heavy.wav',.5,0,.76),('reviewed_cole_sonic_release.wav',.23,0,1.3)],.60,False),
 'juggernaut_charge_start':(.48,[('furnace_chain_reel.wav',.5,0,1.15),('nsp_booster_ignite.mp3',.34,0,.65)],.66,False),
 'juggernaut_charge_loop':(.90,[('nsp_engine_loop.mp3',.6,0,.64),('furnace_chain_reel.wav',.18,0,.83)],.48,True),
 'juggernaut_ram_launch':(.45,[('nsp_booster_ignite.mp3',.68,0,.75),('furnace_chain_launch.wav',.22,0,.8)],.76,False),
 'juggernaut_ram_loop':(.55,[('nsp_engine_loop.mp3',.60,0,1.18),('ice_breath_loop.wav',.25,0,1.6)],.52,True),
 'juggernaut_ram_stop':(.36,[('explosion_air_small_01.wav',.65,0,.65),('debris_scatter_metal.wav',.20,0,1.15)],.72,False),
 'juggernaut_chains':(1.15,[('furnace_chain_reel.wav',.6,0,1.05),('debris_scatter_metal.wav',.13,0,.75)],.35,True),
 'juggernaut_wreck_hit':(.36,[('shield_hit_heavy.wav',.70,0,.65),('debris_scatter_metal.wav',.28,0,.9),('explosion_air_small_02.wav',.16,0,.8)],.73,False),
 'juggernaut_wreck_block':(.16,[('shield_hit_light.wav',.55,0,1.35),('debris_scatter_metal.wav',.17,0,1.5)],.54,False),
 'laser_mist_fire':(.30,[('ice_breath_release.wav',.64,0,1.25),('reviewed_player_laser_beam_start.wav',.4,0,1.3)],.68,False),
 'laser_mist_split':(.16,[('ice_breath_start.wav',.60,0,1.7),('shield_graze.wav',.20,0,1.5)],.48,False),
 'laser_mist_bloom':(.24,[('ice_breath_release.wav',.58,0,1.8),('reviewed_player_laser_beam_start.wav',.24,0,1.65)],.56,False),
 'laser_mist_impact':(.24,[('ice_breath_release.wav',.50,0,1.9),('shield_hit_light.wav',.23,0,1.55)],.60,False),
}
if __name__=='__main__':
    report={name:mix(name,*args)for name,args in recipes.items()}
    (Path(__file__).parent/'audio-build.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('Built %d authored sample mixes; peaks %.2f–%.2f'%(len(report),min(r['peak']for r in report.values()),max(r['peak']for r in report.values())))
