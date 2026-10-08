
const MVAR_SETUP=MV7.setup;
MV7.setup=function(c){
 if(c.variant){ON5_CODES.QAVAR={stage:6,role:'boss',kind:'warhive'};c={...c,code:'QAVAR'};}
 const result=MVAR_SETUP(c);
 if(c.variant==='ace'){whvAceSpawn(B);B._whv.mode='ace';B._whv.ace.st='fight';B._whv.ace.x=worldWidth()/2;B._whv.ace.y=180;B.x=B._whv.ace.x;B.y=180;BAL7.q.initialHP=BAL7.health();}
 return result;
};
