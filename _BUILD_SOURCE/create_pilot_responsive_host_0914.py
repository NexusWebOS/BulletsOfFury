from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'_shots/pilot_fullscreen_0914';p.mkdir(parents=True,exist_ok=True)
(p/'responsive.html').write_text('<!doctype html><meta charset="utf-8"><title>Pilot responsive review</title><style>body{margin:0;background:#222;color:white;font:14px sans-serif}iframe{border:0;display:block}button{margin:4px}</style><button onclick="size(390,844)">Portrait</button><button onclick="size(1100,620)">Landscape</button><iframe id="review" title="Actual game" width="390" height="844" src="/_shots/pilot_fullscreen_0914/review.html?quality=low"></iframe><script>function size(w,h){let f=document.getElementById(\'review\');f.width=w;f.height=h;}</script>',encoding='utf-8')
