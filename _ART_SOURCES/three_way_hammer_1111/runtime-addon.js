
// TD1111: keep the selected whole overhead direction for the entire native attack.
const TD1111={base:{row:ba119Row,corrupt:ba119Corrupt,state:hammerState,start:hb20Start},order:['center','right','left'],events:[]};
function td1111Choose(owner,stage){const direction=TD1111.order[(owner._td1111Next||0)%3];owner._td1111Next=((owner._td1111Next||0)+1)%3;owner._td1111From=owner._td1111Dir||'center';owner._td1111Dir=direction;TD1111.events.push({stage,direction,clock:efxClock});if(TD1111.events.length>120)TD1111.events.shift();return direction;}
function td1111Name(prefix,direction){return prefix+'-overhead'+(direction&&direction!=='center'?'-'+direction:'');}
ba119Row=function(bank,f,mat='regular'){
 if(bank==='blue-overhead'&&ba119Blue(boss)){const h=boss._hammer,load=f<8&&['warn','storm_warn','giant_windup'].includes(h.state);bank=td1111Name('blue',load?h._td1111From:h._td1111Dir);}
 else if(bank==='corrupt-overhead'&&rd74Own(boss))bank=td1111Name('corrupt',hb20State(boss)._td1111Dir);
 return TD1111.base.row(bank,f,mat);
};
ba119Corrupt=function(Q,f,bank='corrupt-overhead'){if(bank==='corrupt-overhead'){const A=Q?.action,load=f<8&&A?.type==='skystrike'&&A.t<A.tell;bank=td1111Name('corrupt',load?Q._td1111From:Q?._td1111Dir);}return TD1111.base.corrupt(Q,f,bank);};
hammerState=function(b,s){if(ba119Blue(b)&&['warn','storm_warn','giant_windup'].includes(s))td1111Choose(b._hammer,5);return TD1111.base.state.apply(this,arguments);};
hb20Start=function(b,type){if(rd74Own(b)&&type==='skystrike')td1111Choose(hb20State(b),8);return TD1111.base.start.apply(this,arguments);};
ba119Clearance=function(prefix,k=1){const rows=['overhead','overhead-left','overhead-right','sides','right'].flatMap(n=>{const a=BA119_ART[prefix+'-'+n];return a.meta.map(m=>({m,p:a.pivot}));});return{left:Math.max(...rows.map(({m,p})=>p[0]-m.bounds[0]))*k+4,right:Math.max(...rows.map(({m,p})=>m.bounds[2]-p[0]))*k+4};};
for(const side of ['left','right']){const key='nca_ba119_blue-overhead-'+side+'_red';if(!BA119.keys[5].includes(key))BA119.keys[5].push(key);}
globalThis.BOF_THREE_WAY_HAMMER_1111=TD1111;
