(function(root){
  'use strict';
  const fract=x=>x-Math.floor(x);
  const hash=n=>fract(Math.sin(n*127.1+78.233)*43758.5453);
  function drops(count,width,height){
    return Array.from({length:count},(_,i)=>({
      x:hash(i*4+1)*width,
      y:hash(i*4+2)*height,
      speed:185+hash(i*4+3)*135,
      length:8+Math.floor(hash(i*4+4)*10),
      opacity:.22+hash(i*4+5)*.25
    }));
  }
  function pose(drop,time,width,height){
    return{x:((drop.x-time*42)%width+width)%width,y:(drop.y+time*drop.speed)%height};
  }
  const api={drops,pose};
  if(typeof module==='object'&&module.exports)module.exports=api;else root.COAST_WEATHER=api;
})(typeof window==='object'?window:this);
