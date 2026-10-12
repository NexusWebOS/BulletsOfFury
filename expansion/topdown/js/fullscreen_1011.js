/* Native fullscreen on activation; the server launcher opens a fullscreen window. */
(function(root){
 'use strict';
 const TD=root.TD,button=document.getElementById('fs-btn'),params=new URLSearchParams(location.search);
 const S=TD.Fullscreen={auto:params.get('fullscreen')!=='0',pending:false,
  isOn(){return!!document.fullscreenElement;},
  sync(){const on=this.isOn();button.setAttribute('aria-pressed',String(on));button.setAttribute('aria-label',on?'Exit fullscreen':'Enter fullscreen');const im=button.querySelector('img');im.src='art/menu_1011/od_btn_'+(on?'windowed':'fullscreen')+'.png';im.alt=on?'Windowed':'Fullscreen';root.TDGAME?.resize();},
  request(){if(this.isOn()||this.pending)return;this.pending=true;try{const p=document.documentElement.requestFullscreen();Promise.resolve(p).catch(()=>{}).finally(()=>{this.pending=false;this.sync();});}catch(e){this.pending=false;}},
  toggle(){this.auto=false;if(this.isOn())document.exitFullscreen().catch(()=>{});else this.request();},
 };
 button.addEventListener('click',e=>{e.stopPropagation();TD.Audio.unlock();S.toggle();});
 document.addEventListener('fullscreenchange',()=>S.sync());
 root.addEventListener('keydown',e=>{if(TD.Input.rebind||TD.OriginalOptions?.snapshot().capture||TD.Frontend.typing)return;if(e.key==='Escape'&&S.isOn()){S.auto=false;document.exitFullscreen().catch(()=>{});return;}if(e.altKey&&e.key==='Enter'){e.preventDefault();S.toggle();return;}if(S.auto&&TD.game?.state==='boot'&&(TD.BIND.start.includes(e.key.toLowerCase())||TD.BIND.A.includes(e.key.toLowerCase())))S.request();});
 document.getElementById('screen').addEventListener('pointerdown',()=>{if(S.auto&&TD.game?.state==='boot')S.request();});
 S.sync();
}(window));
