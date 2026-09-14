function furyIntroClouds(S){
 if(S.space||S.t<2.4)return;
 const draw=(i,x,y,w)=>{
  const key='cm2_cloud_'+(i%7);if(!XART.rdy(key))return;
  const im=XART.get(key),h=w*(im.height/im.width);
  if(y+h/2<0||y-h/2>VH)return;
  ctx.save();ctx.globalAlpha=1;ctx.drawImage(im,x-w/2,y-h/2,w,h);ctx.restore();
 };
 // One finite world-space cloud deck passes down the screen. No wraparound
 // brings a top/bottom cap back alongside the player.
 const travel=(S.scroll-FURY_INTRO_SPEED*2.4)*.7;
 for(let row=0;row<18;row++)for(let col=0;col<3;col++){
  const x=(col+.5)*VW/3+Math.sin(row*2.3+col)*38;
  const y=travel-row*150-col*55-170;
  draw(row*3+col,x,y,235);
 }
 // Side banks frame the clearing at fixed screen positions. No travelling
 // cross-screen top or bottom cloud is attached to this frame.
 for(let row=0;row<4;row++){
  const y=VH*.15+row*VH*.31;
  draw(row,-56,y,272);draw(row+3,VW+56,y,272);
 }
}
