'use strict';
/* Pure difficulty math is available before encounter initialization in both the
   browser and headless checks. Late difficulty_rules_1101 owns live tuning. */
const DR15={step:1.15,keys:['normal','hard','furious'],base:null,events:[]};
function difficultyEnhancement15(key=diffKey){const i=DR15.keys.indexOf(key);return i<0?1:Math.pow(DR15.step,i);}
function difficultyHealth15(normal,key=diffKey){return Math.max(1,Math.round(normal*difficultyEnhancement15(key)));}
function difficultyHealthBaseline15(normal,legacy){return DR15.keys.includes(diffKey)?difficultyHealth15(normal):legacy;}
function turretSpeed15(normal=1){return normal*difficultyEnhancement15();}
function turretInterval15(normal,legacy=normal){return DR15.keys.includes(diffKey)?normal/difficultyEnhancement15():legacy;}
