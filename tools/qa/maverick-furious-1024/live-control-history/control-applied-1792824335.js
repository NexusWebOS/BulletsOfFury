()=>({t:FURYBOT.age(),suspendedStage5:run._s5Resume,miniTrace:FURYBOT.actorSamples?.filter(s=>s.stage===5&&s.kind==='siegebomber'&&s.t>1290).map(s=>({t:s.t,hp:s.hp,parts:s.parts})).slice(-4)})
