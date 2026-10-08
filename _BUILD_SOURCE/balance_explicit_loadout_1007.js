// Select the authored MG option instead of accepting the Stage 6 primary upgrade.
const BAL7_EXPLICIT_SETUP=BAL7.setup,BAL7_EXPLICIT_RESULT=BAL7.result;
BAL7.setup=function(c){
 const result=BAL7_EXPLICIT_SETUP(c);
 if(c.primary){const selected=weaponFormSelect(run.weapon,{kind:'primary1003b',id:c.primary});if(selected!=='ok')throw new Error('Could not select primary: '+selected);}
 result.selection={pilot:_pilotKey(),weapon:run.weapon,primary:run._primary1003b,chainEligible:primary1003bEligible()};
 return result;
};
BAL7.result=function(){return {...BAL7_EXPLICIT_RESULT(),identity:{pilot:_pilotKey(),pilotIndex,primary:run._primary1003b,chainEligible:primary1003bEligible()}};};
