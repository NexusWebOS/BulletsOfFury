/* Portable atlas adapter. The host supplies image loading and a blit callback.
   No font loading API, canvas text, runtime tint, filters, or per-glyph scaling. */
export function createBitmapFont(metrics,image,blit){
 const glyph=c=>metrics.glyphs[c.codePointAt(0)]||metrics.glyphs[63];
 const measure=text=>[...text].reduce((n,c)=>n+glyph(c).xadvance,0);
 function wrap(text,maxWidth){const out=[];for(const paragraph of text.split('\n')){let line='';for(const word of paragraph.split(' ')){
  if(measure(word)>maxWidth){if(line){out.push(line);line='';}for(const c of word){if(line&&measure(line+c)>maxWidth){out.push(line);line='';}line+=c;}continue;}
  const next=line?line+' '+word:word;if(line&&measure(next)>maxWidth){out.push(line);line=word;}else line=next;
 }out.push(line);}return out;}
 function draw(text,x,y,{align='left',maxWidth=Infinity}={}){let py=Math.round(y);for(const line of wrap(text,maxWidth)){
  let px=Math.round(x-(align==='center'?measure(line)/2:align==='right'?measure(line):0));
  for(const c of line){const g=glyph(c);blit(image,g.x,g.y,g.w,g.h,px,py);px+=g.xadvance;}py+=metrics.lineHeight;
 }return py-Math.round(y);}
 return{measure,wrap,draw,lineHeight:metrics.lineHeight,baseline:metrics.baseline};
}
