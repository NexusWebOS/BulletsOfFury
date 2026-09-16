module.exports=function testPilotDeployPad(vm,ctxv,ok){
  console.log('=== 360. the pilot screen deploys on a pad, mid-spin, on any face button ===');
  /* Mike, 0916: "I still cannot get past the pilot select screen in either mode" / "Im on
     controller but that shouldnt matter" - it did. Two independent gates, both invisible on a
     keyboard:
       1. the deploy test sat BELOW `if(pilotRot>0) return;`, and pilotRot is re-armed by every
          roster step, so a pad that keeps nudging the cursor could hold the screen for ever;
       2. confirmPilot ITSELF refused while pilotRot>0, so even a press that was read was dropped.
     Reproduced in real Chromium with a synthetic stick oscillating across the deadzone
     (probe_pad_pilot.py); these pins are the source half. */
  const src=vm.runInContext('drawPilot.toString()',ctxv).replace(/\/\*[\s\S]*?\*\/|\/\/[^\n]*/g,'');
  const iGo=src.indexOf('pilotConfirmPressed()');
  const iLock=src.indexOf('if(pilotRot>0) return;');
  ok(iGo>0 && iLock>0 && iGo<iLock, 'the deploy press is answered BEFORE the spin lock');

  const conf=vm.runInContext('confirmPilot.toString()',ctxv).replace(/\/\*[\s\S]*?\*\/|\/\/[^\n]*/g,'');
  ok(!/pilotPending!=null\|\|pilotRot>0/.test(conf), 'confirmPilot no longer refuses during a spin');
  ok(/pilotRot=0/.test(conf), 'it snaps the spin to its end instead, so you get the pilot you see');

  /* the face set: every face and shoulder except B (cancel) and SELECT. A six-button pad can
     report the button marked A as b2 or b5, which is the whole reason this list exists. */
  const pads=vm.runInContext('PILOT_GO_PAD.join(",")',ctxv);
  ok(pads.indexOf('pad_b0')>=0 && pads.indexOf('pad_b2')>=0 && pads.indexOf('pad_b5')>=0,
     'any face button deploys, b2 and b5 included');
  ok(pads.indexOf('pad_b1')<0 && pads.indexOf('pad_b8')<0,
     'B and SELECT are left alone, so back still backs out');

  /* one press, not two: the card-reveal skip and the deploy share one predicate */
  ok(/pilotConfirmPressed\(\)\)\{\s*pcSkip\(\)/.test(src.replace(/\s+/g,' ').replace(/ \{/g,'{')) ||
     /pcSkip\(\)/.test(src) && (src.match(/pilotConfirmPressed\(\)/g)||[]).length>=2,
     'the reveal skip and the deploy read the same press');
};
