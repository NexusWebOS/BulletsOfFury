from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'_BUILD_SOURCE/night_full_boss_1116.py').read_text(encoding='utf8')
s=s.replace("'_shots/cinema_overnight_1116/native-boss'","'_shots/cinema_overnight_1116/native-sweep'")
s=s.replace("J=S&&typeof j3State==='function'?j3State(b):null", "J=b?.kind==='vileexistence'&&typeof j3State==='function'?j3State(b):null")
s=s.replace(' BOFOnline.submitScore=()=>{};', ''' BOFOnline.submitScore=()=>{};
 const audit=window.cinemaDrawAudit={calls:0,bad:[],counts:{}};
 const nativeDraw=ctx.drawImage;
 ctx.drawImage=function(im,...a){
  audit.calls++;
  if(a.length===8&&im){const W=im.naturalWidth||im.videoWidth||im.width,H=im.naturalHeight||im.videoHeight||im.height;
   if(W>0&&H>0&&(a[0]<-.01||a[1]<-.01||a[0]+a[2]>W+.01||a[1]+a[3]>H+.01)){
    const file=String(im.currentSrc||im.src||'canvas').split('/').pop().split('?')[0],key=file+':'+a.slice(0,4).join(',');
    if(!audit.counts[key]&&audit.bad.length<64)audit.bad.push({file,source:a.slice(0,4),image:[W,H],stack:Error().stack.split('\\n').slice(1,5)});
    audit.counts[key]=(audit.counts[key]||0)+1;
   }
  }
  return nativeDraw.call(this,im,...a);
 };
''')
s=s.replace('return {...captureStats,god:DBGT.god,', 'return {...captureStats,drawAudit:cinemaDrawAudit,god:DBGT.god,')
(R/'_BUILD_SOURCE/night_sweep_1116.py').write_text(s,encoding='utf8',newline='\n')
print('Prepared bounded source-rectangle observations for native boss films')
