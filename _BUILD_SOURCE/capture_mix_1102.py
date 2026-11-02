"""Capture the same post-compression bus heard in actual HTTP gameplay."""
def postmix(source):
    start=source.index(' const seen=new WeakSet(), originalPlay=HTMLMediaElement.prototype.play;')
    end=source.index(' const canvas=document.createElement',start)
    replacement=''' const stats=window.captureStats={peak:0,tapped:0,playing:{},tapErrors:[],frames:0};
 const output=BOF_AUDIO_QUALITY_1102.tap();if(!output)throw Error('Missing actual post-mix bus');output.connect(analyser);stats.tapped=1;
 const oldPlay=Snd.play;Snd.play=function(name){const r=oldPlay.apply(this,arguments);if(r!==false)stats.playing[name]=(stats.playing[name]||0)+1;return r;};
'''
    return(source[:start]+replacement+source[end:]).replace('gain.gain.value=.5','gain.gain.value=.95')
