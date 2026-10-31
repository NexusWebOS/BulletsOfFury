/* Lighting22: lit corridor surfaces, solid foreground cover, readable ordnance.
 * All visible texture/sprite art remains the existing authored PNGs. */
(function(root){
 'use strict';
 const TD=root.TD,T=root.THREE,M=TD.M;
 const api=TD.Lighting22={stats:{playerShots:0,enemyShots:0,echoShots:0},enabled:true};
 api.install=function(grid){
  const scene=grid.scene,coverScene=grid.coverScene,cam=grid.normalCamera;
  const ambient=new T.AmbientLight(0xcbd1d9,1.30),hemi=new T.HemisphereLight(0xaacbdd,0x241b17,.65);
  scene.add(ambient,hemi);scene.fog=new T.Fog(0x03060c,20,46);
  const keyLight=new T.SpotLight(0xffc184,85,24,Math.PI*.32,.15,2);keyLight.position.set(-2,6.7,-5);keyLight.target.position.set(0,0,-8);scene.add(keyLight,keyLight.target);keyLight.castShadow=true;keyLight.shadow.mapSize.set(512,512);keyLight.shadow.camera.near=.3;keyLight.shadow.camera.far=30;keyLight.shadow.bias=-.002;keyLight.shadow.normalBias=.025;
  const core=new T.PointLight(0x31bbff,55,18,2);core.position.set(0,4.9,-16);scene.add(core);
  const muzzle=new T.PointLight(0xffd69a,0,7,2);scene.add(muzzle);
  const rim=new T.DirectionalLight(0x729cba,.36);rim.position.set(0,4,3);scene.add(rim);
  grid.renderer.shadowMap.enabled=true;grid.renderer.shadowMap.type=T.BasicShadowMap;grid.renderer.shadowMap.autoUpdate=false;
  function shaded(map,color=0xffffff){
   const mat=new T.MeshLambertMaterial({map,color,side:T.DoubleSide,flatShading:true,toneMapped:false});
   return mat;
  }
  for(const mesh of [...scene.children])if(mesh.isMesh&&mesh.material.map){const old=mesh.material;mesh.geometry.computeVertexNormals();mesh.material=shaded(old.map,0xffffff);mesh.material.transparent=old.transparent;mesh.material.alphaTest=old.alphaTest;mesh.material.forceSinglePass=true;mesh.receiveShadow=true;old.dispose();}
  const ca=new T.AmbientLight(0xa7b7c9,.7),cr=new T.DirectionalLight(0xffc291,.8);cr.position.set(-3,7,2);coverScene.add(ca,cr);
  const boxes=[],proxies=[],proxyMat=new T.MeshBasicMaterial({colorWrite:false,depthWrite:false});
  function projected(x,y,z){const depth=new T.Vector3(0,3,z).project(cam).z;return new T.Vector3(x/320-1,1-y/240,depth).unproject(cam);}
  function floorPoint(x,y){const v=new T.Vector3(x/320-1,1-y/240,.5).unproject(cam).sub(cam.position);return cam.position.clone().addScaledVector(v,-cam.position.y/v.y);}
  function shadowProxy(index,x,y,width,height,round){
   let mesh=proxies[index];if(!mesh){mesh=new T.Mesh(new T.BoxGeometry(1,1,1),proxyMat);mesh.castShadow=true;mesh.userData.shadowProxy=true;scene.add(mesh);proxies.push(mesh);}
   const foot=floorPoint(x,y),unit=(4-foot.z)*2*Math.tan(25*Math.PI/180)/480;
   mesh.visible=true;mesh.position.set(foot.x,height*unit/2,foot.z);mesh.scale.set(width*unit,height*unit,width*unit*(round?.65:.72));
  }
  const result={ambient,hemi,keyLight,core,muzzle,boxes,proxies,floorPoint,projected,shadowStamp:null,coverBase:410,coverZ:floorPoint(320,410).z};
  // Put the authored grille directly on the solid wall face. The old
  // separate decal sat below a dark, oversized box and read as two walls.
  const faces=new Map();
  function coverFace(state){
   if(faces.has(state))return faces.get(state);
   const k='grid21_cover_'+state,g=ART.get(k),meta=root.TD_ASSAULT_ART.assets[k],q=meta.bounds;
   const cv=document.createElement('canvas');cv.width=q[2]-q[0];cv.height=q[3]-q[1];const ctx=cv.getContext('2d');ctx.imageSmoothingEnabled=false;
   const back=grid.texture('grid21_wall',true).image;ctx.drawImage(back,0,0,cv.width,cv.height);ctx.drawImage(g.im,g.sx+q[0],g.sy+q[1],cv.width,cv.height,0,0,cv.width,cv.height);
   const texture=new T.CanvasTexture(cv);texture.magFilter=texture.minFilter=T.NearestFilter;texture.generateMipmaps=false;texture.colorSpace=T.SRGBColorSpace;grid.textures.set('cover24_face_'+state,texture);faces.set(state,texture);return texture;
  }
  result.beforeCover=function(G){
   G.bastion.cover.forEach((wall,i)=>{
    let mesh=boxes[i];if(!mesh){const side=shaded(grid.texture('grid21_wall',true)),cap=shaded(grid.texture('grid21_floor',true)),front=new T.MeshBasicMaterial({map:coverFace(0),toneMapped:false});
     mesh=new T.Mesh(new T.BoxGeometry(1,1,1),[side,side,cap,side,front,side]);for(const mat of mesh.material){mat.depthTest=false;mat.depthWrite=false;}mesh.renderOrder=i;coverScene.add(mesh);boxes.push(mesh);}
    mesh.visible=wall.hp>0;if(!mesh.visible)return;
    const ratio=wall.hp/wall.max,state=ratio>=.70?0:ratio>=.34?1:2,top=[336,360,384][state];
    const a=projected(wall.x-80.25,top,result.coverZ),b=projected(wall.x+80.25,result.coverBase,result.coverZ);
    mesh.position.set((a.x+b.x)/2,(a.y+b.y)/2,result.coverZ-.05);mesh.scale.set(b.x-a.x,a.y-b.y,.10);mesh.material[4].map=coverFace(state);mesh.material[4].color.setHex(wall.flash>0?0xffe2b6:0xffffff);mesh.userData.screenTop=top;mesh.userData.segment=wall.index;
   });
  };
  result.update=function(G){
   const c=G.bastion,p=G.player,b=G.boss;
   const pulse=1+.11*Math.sin(c.age*4.2);core.color.setHex(b?.form==='helios'?0xff702b:c.flash>.3?0xe9faff:0x31bbff);core.intensity=(b?.form==='helios'?92:b?.form==='core'?72:c.wallCore?.hp>0?48:10)*pulse;
   if(b?.form==='helios'){const pt=floorPoint(b.x,Math.max(280,b.y));core.position.set(pt.x,2.3,pt.z);}else core.position.set(0,4.9,-16);
   const pt=floorPoint(p.x,448);muzzle.position.set(pt.x,1.7,pt.z+.2);muzzle.intensity=p.firing>0&&!p.dead?22*Math.min(1,p.firing/.08):0;
   let i=0;for(const barrel of c.barrels)if(!barrel.dead)shadowProxy(i++,barrel.x,barrel.y,36,48,true);
   for(const cover of c.enemyCover)if(cover.hp>0)shadowProxy(i++,cover.x,cover.y,66,cover.kind==='wall'?34:48,false);
   if(c.phase!=='breach'&&!p.dead)shadowProxy(i++,p.x,448,38,p.prone?36:p.rise<.25?65:106,false);
   for(;i<proxies.length;i++)proxies[i].visible=false;
   result.beforeCover(G);keyLight.intensity=85*(.97+.03*Math.sin(c.age*.9));
   const stamp=c.barrels.map(b=>b.dead?'x':b.x+':'+b.y).join('|')+'/'+c.enemyCover.map(w=>w.hp>0?w.x+':'+w.y:'x').join('|')+'/'+p.x.toFixed(1)+':'+p.prone+':'+p.rise.toFixed(2)+':'+p.dead+':'+c.phase;
   if(stamp!==result.shadowStamp){grid.renderer.shadowMap.needsUpdate=true;result.shadowStamp=stamp;}
  };
  return result;
 };
 const headScales={rifle:.76,minigun:.94,shotgun:.72,laser:.52};
 api.playerShot=function(ctx,s,fade=1){
  const gun=s.gun||'rifle',scale=headScales[gun]||.76,key=gun==='laser'?'tank_laser_silver':'mfx_mg_2_0',angle=M.angTo(s.sx,s.sy,s.tx,s.ty)+(gun==='laser'?Math.PI:0),dx=s.tx-s.sx,dy=s.ty-s.sy,length=Math.hypot(dx,dy)||1,ux=dx/length,uy=dy/length;
  const trail=gun==='laser'?30:gun==='minigun'?24:18;
  for(let j=3;j>0;j--){const distance=Math.min(trail*j/3,Math.hypot(s.x-s.sx,s.y-s.sy));ART.draw(ctx,key,s.x-ux*distance,s.y-uy*distance,{a:angle,s:scale*(1-j*.16),alpha:fade*(.44-j*.07),flash:.32});}
  ART.draw(ctx,key,s.x,s.y,{a:angle,s:scale*1.18,tint:'#050810',alpha:fade});ART.draw(ctx,key,s.x,s.y,{a:angle,s:scale,alpha:fade,flash:gun==='minigun'?.48:.28});api.stats.playerShots++;if(fade<1)api.stats.echoShots++;
 };
 api.enemyShot=function(ctx,e,key,scale){
  const a=M.angTo(e.sx,e.sy,e.tx,e.ty),px=(e.tx-e.sx),py=(e.ty-e.sy),length=Math.hypot(px,py)||1,ux=px/length,uy=py/length;
  for(let j=2;j>0;j--)if(e.kind==='laser'||e.kind==='mg')TD.AssaultArt.draw(ctx,key,e.x-ux*j*7,e.y-uy*j*7,{s:scale*(1-j*.17),alpha:.50-j*.13});
  TD.AssaultArt.draw(ctx,key,e.x,e.y,{s:scale*1.2,tint:'#03040a',alpha:.92});TD.AssaultArt.draw(ctx,key,e.x,e.y,{s:scale,flash:.22});api.stats.enemyShots++;
 };
 // Top-down infantry uses the same authored shots, with a larger readable head.
 const oldShot=TD.drawShot;
 TD.drawShot=function(ctx,s,enemy){
  const G=TD.game;if(!G?.player?.onfoot||G.player.pseudo3D)return oldShot(ctx,s,enemy);
  const lift=TD.projectileLift?.(s)||0;ctx.save();ctx.translate(s.x,s.y-lift);ctx.scale(enemy?1.45:1.95,enemy?1.45:1.95);oldShot(ctx,Object.assign({},s,{x:0,y:0,drawLift:0,liftStart:null,liftEnd:null}),enemy);ctx.restore();
 };
})(window);
