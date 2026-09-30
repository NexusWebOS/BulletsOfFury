// Shared SIG parser: takes pdf.js pages -> {date, tour, rows:[{team,borough,station,fcas,set,site}], headerSet}
const BORO=/^(Manhattan|Bronx|Brooklyn|Queens|Staten Island)$/i;
const FCA_ONLY=/^[A-Z]\d{3}[A-Z]?([\s,\/]+[A-Z]\d{3}[A-Z]?)*[\s,\/]*$/;
function parseSigItems(pages){
  let date=null,tour=null,headerSet=null;const rows=[];
  for(const items of pages){
    const its=items.filter(i=>i.s.trim()).map(i=>({s:i.s.trim(),x:i.x,y:i.y,w:i.w||0}));
    for(const i of its){
      if(!date&&/^\d{1,2}\/\d{1,2}\/\d{4}$/.test(i.s))date=i.s;
      const m=i.s.match(/(\d{1,2}:\d{2})\s*x\s*(\d{1,2}:\d{2})/);if(m&&!tour)tour=m[1]+' x '+m[2];
    }
    if(!tour){ // tour split over items
      const t=its.filter(i=>/^\d{1,2}:\d{2}$/.test(i.s)||i.s==='x');
    }
    // header totals: "Gate Guards" line
    const gg=its.find(i=>/^Gate Guards$/i.test(i.s));
    if(gg&&headerSet==null){const nums=its.filter(i=>Math.abs(i.y-gg.y)<2&&i.x>gg.x&&/^\d+$/.test(i.s)).sort((a,b)=>a.x-b.x);if(nums.length>=2)headerSet=+nums[1].s;}
    const boros=its.filter(i=>BORO.test(i.s));
    const anchors=[];
    for(const b of boros){
      const a=its.filter(i=>/^\d{1,3}$/.test(i.s)&&Math.abs(i.y-b.y)<2.5&&i.x<b.x&&b.x-i.x<80).sort((p,q)=>q.x-p.x)[0];
      if(a)anchors.push({a,b});
    }
    anchors.sort((p,q)=>p.a.y-q.a.y);
    const allF=its.filter(i=>FCA_ONLY.test(i.s)).map(i=>i.x).sort((p,q)=>p-q);
    const pageFx=allF.length?allF[Math.floor(allF.length*0.1)]:null;
    for(let k=0;k<anchors.length;k++){
      const {a,b}=anchors[k];
      const prevY=k?anchors[k-1].a.y:a.y-12, nextY=k<anchors.length-1?anchors[k+1].a.y:a.y+12;
      const top=Math.max((prevY+a.y)/2,a.y-10), bot=Math.min((nextY+a.y)/2,a.y+10);
      const band=its.filter(i=>i.y>top&&i.y<=bot&&i!==a&&i!==b);
      const fcaItems=band.filter(i=>FCA_ONLY.test(i.s)&&i.x>b.x);
      const fcas=[...new Set(fcaItems.flatMap(i=>i.s.match(/[A-Z]\d{3}[A-Z]?/g)))];
      const fx=fcaItems.length?Math.min(...fcaItems.map(i=>i.x)):pageFx;
      const line=band.filter(i=>Math.abs(i.y-a.y)<2.5);
      const hrs=line.filter(i=>/^-?\d{1,6}:\d{2}$/.test(i.s)).sort((p,q)=>q.x-p.x)[0];
      let set=null,site=null;
      if(hrs){const ints=line.filter(i=>/^\d{1,3}$/.test(i.s)&&i.x<hrs.x&&(fx==null||i.x>fx+20)).sort((p,q)=>p.x-q.x);
        if(ints.length>=2){set=+ints[ints.length-1].s;site=+ints[ints.length-2].s;} else if(ints.length===1)set=+ints[0].s;}
      const nameItems=band.filter(i=>i.x>=b.x+ (b.w||20)*0.6 && (fx==null||i.x<fx-2) && !FCA_ONLY.test(i.s) && !/^\d{1,3}$/.test(i.s) || (i.x>b.x+10&&fx!=null&&i.x<fx-2&&!/^\d{1,3}$/.test(i.s)&&!BORO.test(i.s)));
      const uniq=[...new Set(nameItems)].sort((p,q)=>p.y-q.y||p.x-q.x);
      const station=uniq.map(i=>i.s).join(' ').replace(/\s+/g,' ').replace(/\s+\)/g,')').replace(/\(\s+/g,'(').trim();
      rows.push({team:+a.s,borough:b.s,station,fcas,set,site});
    }
  }
  return {date,tour,headerSet,rows};
}
if(typeof module!=='undefined')module.exports={parseSigItems};
