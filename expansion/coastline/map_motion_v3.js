(function(root){
  'use strict';
  function pose(a,t){let x=a.center[0],y=a.center[1],angle=0;if(a.radius){const p=t*a.speed+a.phase;x+=Math.cos(p)*a.radius[0];y+=Math.sin(p)*a.radius[1];angle=Math.atan2(Math.cos(p)*a.radius[1]*a.speed,-Math.sin(p)*a.radius[0]*a.speed)+Math.PI/2;}else{x+=Math.sin(t*a.speed/100+(a.phase||0))*(a.drift||120);y+=Math.sin(t*.055+(a.phase||0))*8;}return{x,y,angle};}
  const api={pose};if(typeof module==='object'&&module.exports)module.exports=api;else root.COAST_MOTION=api;
})(typeof window==='object'?window:this);
