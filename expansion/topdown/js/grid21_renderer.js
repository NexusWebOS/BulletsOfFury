/* Grid21: real perspective corridor geometry with authored 2D texture flats.
 * The orthographic sprite pass preserves the combat system's screen-space
 * sockets/hitboxes. It does not rotate or rescale authored animation banks. */
(function(root){
 'use strict';
 const TD=root.TD,T=root.THREE,W=640,H=480;
 const tex=new Map(),pool=[],coverPool=[];
 let renderer,scene,camera,normalCamera,flatScene,flatCamera,coverScene,door,base,queued=0,outputCtx,layerCtx,layerTexture,layerScene,layerDirty=false;
 const api=TD.Grid21={active:false,clipBottom:480,lost:false,error:null,stats:{frames:0,flatDraws:0,gridCells:0,cameraZ:4,environmentDraws:0}};
 function texture(key,srgb=false){
  const id=key+':'+srgb;if(tex.has(id))return tex.get(id);
  const g=ART.get(key);if(!g)return null;
  const cv=document.createElement('canvas');cv.width=g.sw;cv.height=g.sh;
  const c=cv.getContext('2d');c.imageSmoothingEnabled=false;c.drawImage(g.im,g.sx,g.sy,g.sw,g.sh,0,0,g.sw,g.sh);
  const t=new T.CanvasTexture(cv);t.magFilter=t.minFilter=T.NearestFilter;t.generateMipmaps=false;t.anisotropy=1;t.colorSpace=srgb?T.SRGBColorSpace:T.NoColorSpace;tex.set(id,t);return t;
 }
 function material(key,color=0xffffff){return new T.MeshBasicMaterial({map:texture(key,true),color,side:T.DoubleSide,toneMapped:false});}
 function surface(key,quads,color){
  const p=[],uv=[],ix=[];for(const q of quads){const n=p.length/3;q.forEach(v=>p.push(...v));uv.push(0,0,1,0,1,1,0,1);ix.push(n,n+1,n+2,n,n+2,n+3);}
  const g=new T.BufferGeometry();g.setAttribute('position',new T.Float32BufferAttribute(p,3));g.setAttribute('uv',new T.Float32BufferAttribute(uv,2));g.setIndex(ix);g.computeBoundingSphere();const m=new T.Mesh(g,material(key,color));scene.add(m);api.stats.gridCells+=quads.length;return m;
 }
 function flatMesh(){
  const g=new T.PlaneGeometry(1,1);g.setAttribute('position',new T.BufferAttribute(new Float32Array(12),3));
  const m=new T.ShaderMaterial({transparent:true,depthTest:false,depthWrite:false,side:T.DoubleSide,forceSinglePass:true,toneMapped:false,
   uniforms:{image:{value:null},opacity:{value:1},flash:{value:0},clipBottom:{value:480}},
   vertexShader:'varying vec2 vUv; void main(){vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0);}',
   fragmentShader:'uniform sampler2D image; uniform float opacity; uniform float flash; uniform float clipBottom; varying vec2 vUv; void main(){if(480.0-gl_FragCoord.y>clipBottom)discard; vec4 c=texture2D(image,vUv); if(c.a<0.01)discard; gl_FragColor=vec4(mix(c.rgb,vec3(1.0),flash),c.a*opacity);}' });
  const mesh=new T.Mesh(g,m);mesh.frustumCulled=false;return mesh;
 }
 function init(){
  if(renderer)return !api.lost;if(!T){api.error='Three.js module unavailable';return false;}
  if(['grid21_wall','grid21_floor','grid21_ceiling','grid21_rearwall','grid21_door_0','grid21_cover_0','grid21_cover_1','grid21_cover_2','grid21_cover_3'].some(k=>!ART.get(k)))return false;
  try{
   renderer=new T.WebGLRenderer({antialias:false,alpha:true,preserveDrawingBuffer:true,powerPreference:'high-performance'});renderer.setPixelRatio(1);renderer.setSize(W,H,false);renderer.autoClear=false;renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.NoToneMapping;
   renderer.domElement.addEventListener('webglcontextlost',()=>{api.lost=true;api.error='WebGL context lost';});renderer.domElement.addEventListener('webglcontextrestored',()=>{api.lost=false;api.error=null;});
   scene=new T.Scene();camera=new T.PerspectiveCamera(50,W/H,.05,80);camera.setViewOffset(W,H,0,50,W,H);camera.position.set(0,3,4);camera.updateMatrixWorld();normalCamera=camera.clone();normalCamera.updateMatrixWorld();
   flatCamera=new T.OrthographicCamera(0,W,0,H,.1,20);flatCamera.position.z=10;flatScene=new T.Scene();coverScene=new T.Scene();
   const layer=document.createElement('canvas');layer.width=W;layer.height=H;layerCtx=layer.getContext('2d');layerCtx.imageSmoothingEnabled=false;
   for(const name of ['drawImage','fillRect','strokeRect','fill','stroke','fillText','strokeText']){const original=layerCtx[name].bind(layerCtx);layerCtx[name]=function(...args){layerDirty=true;return original(...args);};}
   layerTexture=new T.CanvasTexture(layer);layerTexture.magFilter=layerTexture.minFilter=T.NearestFilter;layerTexture.generateMipmaps=false;layerTexture.colorSpace=T.NoColorSpace;tex.set('native-fx-layer',layerTexture);
   layerScene=new T.Scene();const lm=flatMesh();lm.geometry.attributes.position.array.set([0,0,0,W,0,0,0,H,0,W,H,0]);lm.geometry.attributes.position.needsUpdate=true;lm.material.uniforms.image.value=layerTexture;layerScene.add(lm);api.layerContext=layerCtx;
   const floor=[],ceiling=[],left=[],right=[];
   for(let z=4;z> -30;z-=2){for(let x=-6;x<6;x+=2){floor.push([[x,0,z],[x+2,0,z],[x+2,0,z-2],[x,0,z-2]]);ceiling.push([[x,7,z],[x+2,7,z],[x+2,7,z-2],[x,7,z-2]]);}
    for(let y=0;y<7;y+=3.5){left.push([[-6,y,z],[-6,y,z-2],[-6,y+3.5,z-2],[-6,y+3.5,z]]);right.push([[6,y,z],[6,y,z-2],[6,y+3.5,z-2],[6,y+3.5,z]]);}}
   surface('grid21_floor',floor,0xc3c3c3);surface('grid21_ceiling',ceiling,0xa7a7a7);surface('grid21_wall',left,0xd0d0d0);surface('grid21_wall',right,0xd0d0d0);
   surface('grid21_rearwall',[[[-6,0,-18],[-2.30,0,-18],[-2.30,7,-18],[-6,7,-18]],[[2.30,0,-18],[6,0,-18],[6,7,-18],[2.30,7,-18]],[[-2.30,6.4,-18],[2.30,6.4,-18],[2.30,7,-18],[-2.30,7,-18]]],0xffffff);
   const black=new T.Mesh(new T.PlaneGeometry(12,7),new T.MeshBasicMaterial({color:0x020306,side:T.DoubleSide}));black.position.set(0,3.5,-30);scene.add(black);
   const dm=new T.MeshBasicMaterial({map:texture('grid21_door_0',true),transparent:true,alphaTest:.5,side:T.DoubleSide,forceSinglePass:true,toneMapped:false});door=new T.Mesh(new T.PlaneGeometry(4.78,root.TD_PIXEL25_ART?4.78*184/128:6.82),dm);door.position.set(0,3.02,-17.99);scene.add(door);
   api.texture=texture;api.renderer=renderer;api.scene=scene;api.camera=camera;api.normalCamera=normalCamera;api.flatScene=flatScene;api.coverScene=coverScene;api.textures=tex;api.pool=pool;api.coverPool=coverPool;api.project=(point)=>{const v=new T.Vector3(...point).project(camera);return{x:(v.x+1)*320,y:(1-v.y)*240};};
   return true;
  }catch(e){api.error=String(e);console.error('Grid21 renderer:',e);return false;}
 }
 function copy(ctx){ctx.save();ctx.setTransform(base);ctx.imageSmoothingEnabled=false;ctx.drawImage(renderer.domElement,0,0,W,H);ctx.restore();}
 api.begin=function(ctx,G){
  api.active=false;if(!init())return false;base=ctx.getTransform();outputCtx=ctx;layerCtx.setTransform(1,0,0,1,0,0);layerCtx.clearRect(0,0,W,H);layerDirty=false;queued=0;api.clipBottom=480;api.active=true;
  let travel=0;const c=G.bastion,tr=c.transition;if(c.phase==='breach'&&tr?.phase==='walk'){const t=Math.min(1,tr.t/1.65/.80);travel=27*t*t*(3-2*t);}else if(c.phase==='breach'&&tr?.phase==='black')travel=27;
  if(TD.Lighting22&&!api.lighting)api.lighting=TD.Lighting22.install(api);api.lighting?.update(G);camera.position.z=4-travel;camera.updateMatrixWorld();api.stats.cameraZ=camera.position.z;door.visible=c.phase!=='breach'||tr?.phase==='blast';door.material.opacity=c.phase==='breach'?Math.max(0,1-tr.t*2.5):1;
  renderer.setClearColor(0x020306,1);renderer.clear();renderer.render(scene,camera);api.stats.environmentDraws=renderer.info.render.calls;api.stats.frames++;return true;
 };
 api.flat=function(ctx,key,x,y,s=1,o={}){
  if(!api.active)return false;const image=texture(key),m=root.TD_ASSAULT_ART.assets[key];if(!image||!m)return false;
  let mesh=pool[queued];if(!mesh){mesh=flatMesh();pool.push(mesh);flatScene.add(mesh);}mesh.visible=true;mesh.renderOrder=queued++;const u=mesh.material.uniforms;u.image.value=image;u.opacity.value=(o.alpha??1)*ctx.globalAlpha;u.flash.value=o.flash||0;u.clipBottom.value=api.clipBottom;
  const a=m.anchor[0],b=m.anchor[1],w=m.size[0],h=m.size[1],matrix=ctx.getTransform(),verts=mesh.geometry.attributes.position.array,angle=o.a||0,cs=Math.cos(angle),sn=Math.sin(angle);
  // PlaneGeometry vertex order: top-left, top-right, bottom-left, bottom-right.
  [[0,0],[w,0],[0,h],[w,h]].forEach(([px,py],i)=>{const lx=(px-a)*s,ly=(py-b)*s,dx=x+lx*cs-ly*sn,dy=y+lx*sn+ly*cs;verts[i*3]=matrix.a*dx+matrix.c*dy+matrix.e;verts[i*3+1]=matrix.b*dx+matrix.d*dy+matrix.f;verts[i*3+2]=0;});mesh.geometry.attributes.position.needsUpdate=true;api.stats.flatDraws++;return true;
 };
 function flushCanvas(){if(!layerDirty)return;layerTexture.needsUpdate=true;renderer.clearDepth();renderer.render(layerScene,flatCamera);layerCtx.save();layerCtx.setTransform(1,0,0,1,0,0);layerCtx.clearRect(0,0,W,H);layerCtx.restore();layerDirty=false;}
 api.flush=function(ctx){if(!api.active)return;flushCanvas();if(!queued)return;for(let i=queued;i<pool.length;i++)pool[i].visible=false;renderer.clearDepth();renderer.render(flatScene,flatCamera);queued=0;};
 function worldQuad(mesh,key,x,y,z,opacity,flash,s=1.04){
  const m=root.TD_ASSAULT_ART.assets[key];mesh.material.uniforms.image.value=texture(key);mesh.material.uniforms.opacity.value=opacity;mesh.material.uniforms.flash.value=flash;mesh.material.uniforms.clipBottom.value=480;
  const distance=4-z,ndcZ=new T.Vector3(0,3,z).project(normalCamera).z,verts=mesh.geometry.attributes.position.array;
  [[0,0],[m.size[0],0],[0,m.size[1]],[m.size[0],m.size[1]]].forEach(([px,py],i)=>{const v=new T.Vector3((x+(px-m.anchor[0])*s)/320-1,1-(y+(py-m.anchor[1])*s)/240,ndcZ).unproject(normalCamera);verts[i*3]=v.x;verts[i*3+1]=v.y;verts[i*3+2]=v.z;});mesh.geometry.attributes.position.needsUpdate=true;mesh.visible=distance>0;
 }
 api.cover=function(ctx,G){
  if(!api.active)return false;api.flush(ctx);const c=G.bastion;
  c.cover.forEach((wall,i)=>{let mesh=coverPool[i];if(!mesh){mesh=flatMesh();coverPool.push(mesh);coverScene.add(mesh);}mesh.renderOrder=100+i;const state=wall.hp<=0?3:wall.hp/wall.max<.34?2:wall.hp/wall.max<.70?1:0;worldQuad(mesh,'grid21_cover_'+state,wall.x,api.lighting?.coverBase??454,api.lighting?.coverZ??0,1,wall.flash>0?.65:0);if(api.lighting&&wall.hp>0)mesh.visible=false;});
  renderer.clearDepth();renderer.render(coverScene,camera);return true;
 };
 api.end=function(ctx){if(!api.active)return;api.flush(ctx);copy(outputCtx);api.active=false;};
})(window);
