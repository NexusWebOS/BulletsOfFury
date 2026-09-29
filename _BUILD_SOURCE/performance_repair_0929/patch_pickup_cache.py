from pathlib import Path
P=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury\assets\game.js')
s=P.read_text(encoding='utf-8')
helper='''function lateShadowImage(g,im,...args){
  if(g!==ctx||(!g.shadowBlur&&(!g.filter||g.filter==='none')))return g.drawImage(im,...args);
  let rc,x,y,w,h;
  if(args.length===8){rc=args.slice(0,4);[x,y,w,h]=args.slice(4);}
  else if(args.length===4){rc=[0,0,im.naturalWidth||im.width,im.naturalHeight||im.height];[x,y,w,h]=args;}
  else return g.drawImage(im,...args);
  if(!(w>0&&h>0))return g.drawImage(im,...args);
  const plate=lateSpriteBake(im,rc,w,h,g.shadowColor,g.shadowBlur,g.filter,g.globalCompositeOperation==='lighter');
  g.save();g.shadowBlur=0;g.filter='none';lateSpriteBlit(plate,x,y);g.restore();
}
'''
anchor='const _glowOrder=new Map(),_blobOrder=new Map();'
assert s.count(anchor)==1;s=s.replace(anchor,helper+anchor)
for start,end in [('function iconBlit(', '/* ============================================================\n   GRAVITY MODE V2'),('function drawScrate(', 'function drawPlayerImpactEffects(')]:
    a=s.index(start);b=s.index(end,a);block=s[a:b]
    # Target only icon/pickup calls; the latter span also contains drawEffects.
    if start.startswith('function drawScrate'):
        b=s.index('function drawEffects(',a);block=s[a:b]
    block=block.replace('ctx.drawImage(', 'lateShadowImage(ctx,').replace('g.drawImage(', 'lateShadowImage(g,')
    s=s[:a]+block+s[b:]
P.write_bytes(s.encode('utf-8'));print('Cached main-context icon and pickup shadow draws')
