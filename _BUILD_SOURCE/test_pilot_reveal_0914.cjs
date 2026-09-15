/* Reuse the full game's established VM boot; exercise production reveal state for every pilot. */
const fs=require('fs'),path=require('path'),Module=require('module');
const root=path.resolve(__dirname,'..');
const harness=fs.readFileSync(path.join(__dirname,'test_fl.js'),'utf8');
const boot=harness.slice(0,harness.indexOf('/* top-level const/let'));
const tests=`
const assert=require('assert/strict');
const result=vm.runInContext(\`(()=>{
  const rows=[];
  for(const P of PILOTS){
    const copy=pcScreenCopy(P),total=copy.join('').length;
    pcStart(P.key); pcard.textTotal=total;
    if(pcRevealText(copy,0)!==''||pcVisibleSegments(0,20)!==0) throw Error(P.key+' initial reveal');
    let elapsed=0,partial=false,filling=false,previous=pcard.stats.map(()=>0);
    while(!pcard.done&&elapsed<8){
      pcUpdate(1/120); elapsed+=1/120;
      const visible=copy.map((_,i)=>pcRevealText(copy,i));
      if(visible.some((s,i)=>!copy[i].startsWith(s)))throw Error('text order');
      if(visible.some((s,i)=>s.length>0&&s.length<copy[i].length))partial=true;
      pcard.stats.forEach((s,i)=>{
        const value=pcVisibleSegments(i,s.val);
        if(value<previous[i]||value>s.val)throw Error('bar bounds/order');
        if(value>0&&value<s.val)filling=true;
        if(i>0&&value>0&&previous[i-1]<pcard.stats[i-1].val)throw Error('row ordering');
        previous[i]=value;
      });
    }
    if(!pcard.done||!partial||!filling)throw Error(P.key+' incomplete animation');
    if(copy.some((s,i)=>pcRevealText(copy,i)!==s))throw Error('missing final copy');
    pcStart(P.key);pcard.textTotal=total;pcUpdate(.5);pcUpdate(.05);pcSkip();
    if(!pcard.done||copy.some((s,i)=>pcRevealText(copy,i)!==s))throw Error('skip text');
    if(pcard.stats.some((s,i)=>pcVisibleSegments(i,s.val)!==s.val))throw Error('skip bars');
    pcStart(P.key);
    if(pcard.done||pcard.typed||pcard.seg||pcard.bar)throw Error('re-entry reset');
    rows.push({pilot:P.key,seconds:+elapsed.toFixed(3),stats:pcard.stats.length,partialText:partial,progressiveBars:filling,skip:true,reset:true});
  }
  return rows;
})()\`,ctxv);
assert.equal(result.length,9);
console.log(JSON.stringify({passed:result.length,failed:0,rows:result},null,2));
`;
const m=new Module(__filename,module);m.filename=__filename;m.paths=module.paths;
m._compile(boot+tests,__filename);
