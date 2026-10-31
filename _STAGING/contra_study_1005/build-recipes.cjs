'use strict';
const fs=require('node:fs'),path=require('node:path');
const {Encounter,recipes,presets}=require('./patterns.js');
const data={version:1,scope:'Original standalone BOF candidates; proposed tuning, not measured Contra data',
  units:{position:'normalized arena',time:'seconds',velocity:'arena units/second'},
  source:'https://www.youtube.com/watch?v=iooQeqdyB8E',presets,
  patterns:Object.entries(recipes).map(([id,meta])=>({id,...meta,
    presets:Object.keys(presets).map(difficulty=>{const e=new Encounter(id,difficulty);return{difficulty,duration:e.duration,activeEnd:e.end,warnings:e.warnings,schedule:e.plan};})}))};
fs.writeFileSync(path.join(__dirname,'recipes.json'),JSON.stringify(data,null,2)+'\n');
console.log('Saved six recipes across three presets.');
