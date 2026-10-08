from pathlib import Path
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');O=R/'_shots/asset_layout_1007/loading_before';O.mkdir(parents=True,exist_ok=True)
def change(rel,patches):
 p=R/rel;b=p.read_bytes();s=b.decode('utf-8')
 for old,new in patches:
  assert old in s,(rel,old[:100]);s=s.replace(old,new,1)
 out=s.encode('utf-8');(O/p.name).write_bytes(b);p.write_bytes(out)
change('assets/asset_paths_1007.js',[("(BOF_ASSET_PATHS[path]||path)","(window.BOF_ASSET_PATHS[path]||path)")])
p=R/'assets/asset_paths_1007.js'
with p.open('a',encoding='utf-8',newline='') as f:f.write("function bofAssetLoadingAllowed(path){if(document.readyState!=='loading'||window.__bofAssetRuntimeReady)return true;const owner=bofAssetOwner(path);return owner==='shared/ui'||owner==='shared/fonts'||owner.endsWith('/portraits')||/weapon_special_icons/.test(bofAssetPath(path));}\n")
change('index.html',[( '<script src="assets/manifest.js"></script>', '<script src="assets/asset_paths_1007.js"></script>\n<script src="assets/manifest.js"></script>'),('<script src="assets/online.js"></script>','<script src="assets/online.js"></script>\n<script src="assets/asset_memory_1007.js"></script>')])
change('assets/game.js',[
 ("const ctx = cv.getContext('2d');","const ctx = cv.getContext('2d',{alpha:false});"),
 ("function mk(d,m){ if(!d)return null; const im=new Image(); im.src=(typeof d==='string'&&d.lastIndexOf('assets/',0)===0)?d:('data:'+m+';base64,'+d); return im; }", "function mk(d,m){ if(!d)return null; const im=new Image();im.decoding='async'; im.src=(typeof d==='string'&&d.lastIndexOf('assets/',0)===0)?(typeof bofAssetPath==='function'?bofAssetPath(d):d):('data:'+m+';base64,'+d); return im; }"),
 ("const X={img:{}};\n  function mk(o){ if(!o) return null; const im=new Image(); im.src=(typeof o==='string')?o:('data:'+o.m+';base64,'+o.d); return im; }", """const X={img:{}};const _imageURLs=new Map();
  function mk(o){
    if(!o)return null;
    const src=typeof o==='string'?(typeof bofAssetPath==='function'?bofAssetPath(o):o):('data:'+o.m+';base64,'+o.d);
    if(_imageURLs.has(src))return _imageURLs.get(src);
    const im=new Image();im.decoding='async';_imageURLs.set(src,im);im.src=src;return im;
  }"""),
 ("|ship_|port_|card_|face_|menu", "|ship_|port_cf_[a-z]+_idle$|card_|face_|menu"),
 ("  X._src = (window.BOFX && BOFX.img) ? BOFX.img : {};", """  X._src = (window.BOFX && BOFX.img) ? BOFX.img : {};
  if(typeof bofAssetPath==='function'){
    for(const k in X._src)X._src[k]=bofAssetPath(X._src[k]);
    X._src=new Proxy(X._src,{set(target,key,value){target[key]=bofAssetPath(value);return true;}});
    if(window.BOFX)BOFX.img=X._src;
  }"""),
 ("const src=X._src[k];\n    X.img[k]= src ? mk(src) : null;", "const src=X._src[k];\n    if(src&&typeof bofAssetLoadingAllowed==='function'&&!bofAssetLoadingAllowed(src))return null;\n    X.img[k]= src ? mk(src) : null;"),
 ("if(X.img[root]!==undefined)delete X.img[root];", """const path=typeof bofAssetPath==='function'?bofAssetPath(X._src[root]):X._src[root];
    for(const key in X.img){const src=typeof bofAssetPath==='function'?bofAssetPath(X._src[key]):X._src[key];if(key===root||(path&&src===path))delete X.img[key];}
    if(path)_imageURLs.delete(path);"""),
 ("  /* ⚠ THESE TWO READ THE CACHE DIRECTLY", """  X.memoryInfo=function(){
    let decodedBytes=0,decodedImages=0,cellBytes=0,cells=0;
    for(const im of _imageURLs.values()){if(im.complete&&im.naturalWidth>0){decodedImages++;decodedBytes+=im.naturalWidth*im.naturalHeight*4;}}
    for(const cache of [_genCells,_playerCells,_shipCells])for(const im of Object.values(cache)){if(im){cells++;cellBytes+=(im.width||0)*(im.height||0)*4;}}
    return {decodedImages,decodedRGBAEstimate:decodedBytes,cells,cellRGBAEstimate:cellBytes};
  };
  /* ⚠ THESE TWO READ THE CACHE DIRECTLY"""),
 ("function _levelCfg(){\n  switch(run.stage){", "function _levelCfg(stage=run.stage){\n  switch(stage){"),
 ("let SS = _renderQuality==='performance'?1:2;", "let _lowMemoryDevice=false;try{_lowMemoryDevice=(navigator.deviceMemory>0&&navigator.deviceMemory<=4)||(navigator.hardwareConcurrency>0&&navigator.hardwareConcurrency<=4);}catch(_hw){}\nlet SS = _renderQuality==='performance'||(_renderQuality==='auto'&&_lowMemoryDevice)?1:2;"),
 ("If PLAY sustains sub-30fps", "If PLAY sustains frames slower than 19ms"),
 ("_renderSlowT=d>.034?_renderSlowT+d", "_renderSlowT=d>.019?_renderSlowT+d"),
 ("  // 1. anything living in this stage's folder", """  // Named roster roots are mandatory before the first enemy can appear.
  addPrefix('nca_en_s'+n);addPrefix('nca_eproj_s'+n);
  add('bof_player_weapon_special_icons_atlas');add('bof_player_ordnance_projectiles_atlas');add('nca_player_weapons');
  // Portrait speech reels decode during deployment, rather than on the first spoken syllable.
  const portraitPilots=new Set([run.pilot]);if(typeof coopActive==='function'&&coopActive()&&typeof p2Pilot==='function')portraitPilots.add(p2Pilot().key);
  if(n===6)for(const P of PILOTS)portraitPilots.add(P.key);
  for(const k in XART._src)if((/^pp5_raw_/.test(k)&&portraitPilots.has(k.split('_')[2]))||(/^cp5_raw_/.test(k)&&portraitPilots.has('cole')))add(k);
  // 1. anything living in this stage's folder"""),
 ("function startGameLoop(){last=performance.now();requestAnimationFrame(loop);}", "function startGameLoop(){window.__bofAssetRuntimeReady=true;last=performance.now();requestAnimationFrame(loop);}")
])
change('assets/pilot_portraits_1005.js',[("for(const em of ['idle','talk-closed','talk-small','talk-medium','talk-wide','talk-o'])XART.rdy", "for(const em of ['idle'])XART.rdy")])
change('assets/cole_portraits_1005.js',[("for(const em of ['idle','talk-closed','talk-small','talk-medium','talk-wide','talk-o'])XART.rdy", "for(const em of ['idle'])XART.rdy")])
# The harness must load the same path resolver before any runtime registry.
p=R/'_BUILD_SOURCE/test_fl.js';b=p.read_bytes();s=b.decode('utf-8');needle="run('assets/manifest.js', 'manifest');"
assert needle in s
s=s.replace(needle,"run('assets/asset_paths_1007.js', 'asset paths');\r\n"+needle,1)
(O/'test_fl.js').write_bytes(b);p.write_bytes(s.encode('utf-8'))
print('Patched canonical image caching, ownership cleanup, boot deferral, correct stage warmup and adaptive render policy.')
