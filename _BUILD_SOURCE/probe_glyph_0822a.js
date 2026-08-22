(() => {
  const _orig = window.drawScene;
  window.drawScene = function(dt){
    try { _orig.apply(this, arguments); } catch(e){}
    try {
      const art = (typeof defFontArt==='function' && defFontArt()) ||
                  (typeof curFontArt==='function' && curFontArt());
      if(!art || !art.font) return;
      const W = ctx.canvas.width, Hc = ctx.canvas.height;
      ctx.save();
      ctx.setTransform(1,0,0,1,0,0);
      ctx.fillStyle='#12141a'; ctx.fillRect(0,0,W,Hc);
      const H = 54;                      // dialogue-ish size, large enough to read
      const rows = ["A'B", "A,B", "A.B", "A-B", "A+B", "A:B"];
      let cy = 70;
      for(const r of rows){
        // cap-box guides: blue = cap top, red = baseline
        ctx.fillStyle='#3a6ad0'; ctx.fillRect(0, Math.round(cy-H/2), W, 1);
        ctx.fillStyle='#d05a5a'; ctx.fillRect(0, Math.round(cy+H/2), W, 1);
        stageText(art, r, W/2, cy, H, null, 0, 1, 0.10);
        cy += 78;
      }
      ctx.restore();
    } catch(e){ window.__probeErr = String(e&&e.message||e); }
  };
})();
