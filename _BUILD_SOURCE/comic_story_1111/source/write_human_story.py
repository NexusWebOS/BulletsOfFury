"""Single source for the human shooting script and the in-game story data."""
from pathlib import Path
import json,re
PACK=Path(__file__).resolve().parents[1]
def L(who,text='',**extra):return dict(who=who,text=text,**extra)
scenes={
'opening':[
 L('CAPTION','For years, Earth had been at peace.',kind='wide',art='city'),
 L('CAPTION','Fury Division trained in secret. The best pilots from around the world, waiting for a call they hoped would never come.',kind='wide',bank='hq-conference',hold=0),
 L('COLE','Last check, Deck. Then you eat.',people=['cole','decker']),
 L('DECKER',"Hold on. I'm getting orders I didn't send.",people=['cole','decker']),
 L('DECKER',"It's everywhere. Roads, power stations, defense.",kind='insert',bank='city-takeover',cue='stage3AtomicSiren',cueAt=.1),
 L('FALVA',"Hangar door nearly took Lizzie's head off.",people=['falva','lizzie']),
 L('LIZZIE',"I'm fine. Worry about the planes.",people=['falva','lizzie']),
 L('COLE','Cut the uplinks. We fly by hand.',people=['cole','decker']),
 L('DECKER','Already cut. Our jets are clear.',people=['cole','decker']),
 L('AXEL','Freezer. On me.',people=['axel','freezer']),
 L('FREEZER','Right behind you.',people=['axel','freezer']),
 L('YURI',"Those people down there don't have wings.",people=['yuri','cole']),
 L('COLE',"That's why we're going.",people=['yuri','cole']),
 L('MAVERICK','And here I was getting bored.',people=['maverick','juggernaut']),
 L('JUGGERNAUT',"I'll get the doors. Get everybody out.",kind='insert',bank='juggernaut-help',people=['juggernaut','maverick']),
 L('COLE','Fury flight. Talk to me.',kind='travel',art='sky',cue='jetDash',cueAt=.1),
 L('PILOT','Lost the squad. Still flying. Where do you need me?',people=['$pilot','$tech'],cue='crackle',cueAt=.1),
 L('TECH',"Keep those things away from the towns. We'll find you.",people=['$pilot','$tech']),
],
'post-1':[
 L('PILOT',"That's one down. Tell me somebody heard that.",id='B101'),
 L('TECH',"I heard you. And something else is answering.",kind='insert',bank='radar-acquisition',cue='blip'),
 L('PILOT','Where?'),
 L('TECH','The volcanic belt. Same orders, over and over.'),
 L('PILOT',"Then we've got somewhere to start.",kind='travel',art='sky'),
],
'post-2':[
 L('PILOT','Come on, $techName. Pick up.',id='B201'),
 L('TECH',"There you are! I thought we'd lost you.",cue='crackle'),
 L('PILOT',"You can yell at me when I'm home. What is this thing?",kind='insert',bank='service-connector'),
 L('TECH',"A service port. Plug in the recorder. Keep it off the network."),
 L('TECH',"Got it. The next relay's in the ice field."),
 L('TECH',"I've got a fire rig ready. Those ice tanks won't like it.",upgrade=2),
 L('PILOT','Good. I could use something on my side.'),
 L('TECH','Get out of there. The ground is moving.',kind='travel',art='sky',cue='crackle'),
],
'post-3':[
 L('COLE',"All right. We're home. What did we bring back?",id='B301',kind='wide',bank='hq-conference',hold=0,tag='briefing'),
 L('DECKER',"The relay's recorder. Every machine heard the same voice.",tag='briefing'),
 L('COLE','Whose?',tag='briefing'),
 L('DECKER',"I don't know yet. There's a launch record in here. Same signal. It came from the airfield east of us.",kind='insert',bank='launch-correlation',tag='briefing'),
 L('LIZZIE','So we go to the airfield.',people=['lizzie','falva'],tag='briefing'),
 L('DECKER',"I also need its backup power cell. Without it, we don't get above the atmosphere.",tag='briefing'),
 L('AXEL',"I'll take point.",people=['axel','freezer'],tag='briefing'),
 L('FREEZER',"Then I'll watch your tail.",people=['axel','freezer'],tag='briefing'),
 L('MAVERICK','Try to leave something for the rest of us.',people=['maverick','juggernaut'],tag='briefing'),
 L('JUGGERNAUT',"Everybody gets home. That's the deal.",people=['maverick','juggernaut'],tag='briefing'),
 L('COLE',"That's the deal.",kind='wide',bank='hq-conference',hold=3,tag='briefing'),
 L('DECKER',"The ice core's safe. I'll see what we can use before you leave.",upgrade=3),
 L('CAPTION','A few minutes later. Decker\'s workshop.',kind='insert',bank='hq-laser-reveal',hold=0,tag='prototypes'),
 L('COLE','You moved the coil.',people=['cole','decker'],tag='prototypes'),
 L('DECKER',"Thought you'd spot that. Watch this.",people=['cole','decker'],tag='prototypes'),
 L('SYSTEM','',kind='insert',bank='hq-laser-demo',duration=2.1,action='laser-test',tag='prototypes'),
 L('COLE',"That's your Photon Cannon?",people=['cole','decker'],tag='prototypes'),
 L('DECKER','Ours. You wound half the coils.',people=['cole','decker'],tag='prototypes'),
 L('COLE','Come here, you lunatic.',kind='insert',bank='hq-cole-decker-hug',tag='prototypes'),
 L('DECKER','Easy! Still need those ribs.',kind='insert',bank='hq-cole-decker-hug',hold=5,tag='prototypes'),
 L('COLE','When can I fly it?',people=['cole','decker'],tag='prototypes'),
 L('DECKER','When it stops melting the stand. Bring me that power cell.',people=['cole','decker'],tag='prototypes'),
 L('COLE',"You've got it.",people=['cole','decker'],tag='prototypes'),
],
'arrival-4':[
 L('TECH',"There's the airfield. The launch pad's still lit.",kind='insert',bank='airbase-arrival',id='A401'),
 L('PILOT','Get the records. Get the cell. Get home.',kind='travel',art='sky'),
],
'post-4':[
 L('PILOT',"Got your power cell. And the launch camera's recorder.",id='B401'),
 L('TECH','All right. Show me what happened.',kind='insert',bank='decker-reaction',hold=0),
 L('SYSTEM','',id='B403',kind='wide',bank='satellite-takeover',duration=3.3,action='satellite',cue='crackle',cueAt=.4),
 L('PILOT',"It got inside the satellite."),
 L('TECH',"Symbiote code. It used the downlink to reach everything down here."),
 L('PILOT','So we cut it off.'),
 L('TECH',"Your space kits are ready. Just don't make me come get you.",upgrade=4),
 L('FALVA',"We got Granddad's bomber flying. We can handle this.",people=['falva','lizzie']),
 L('LIZZIE',"Granddad's bomber had air outside it.",people=['falva','lizzie']),
 L('PILOT',"One last check. Then we're going up.",kind='travel',art='earth'),
],
'warp-5-9':[
 L('TECH',"That gate isn't on our charts.",kind='insert',bank='warp-drive-lock',id='W5901',cue='blip'),
 L('PILOT','Can we clear it?'),
 L('TECH',"We're already through the last marker. Keep her straight!"),
 L('PILOT','Everybody hang on.',kind='warp',art='space',id='W5903',duration=2.4,cue='warp',cueAt=.25),
],
'arrival-9':[
 L('PILOT','Everybody still in one piece?',id='A901',kind='travel',art='space'),
 L('TECH','Ask me again when my hands stop shaking.'),
 L('PILOT',"Let's find a way back."),
],
'post-9':[
 L('TECH',"There's our way home. Take it while it's still open.",id='Q01',kind='insert',bank='warp-drive-lock',hold=5),
 L('PILOT',"Gladly."),
 L('TECH',"The recorder caught something useful. I'll see what I can make of it.",upgrade=9),
 L('PILOT',"First, get us back.",kind='travel',art='space'),
],
'post-5':[
 L('PILOT',"HQ, open the doors. We're coming home.",id='B501',kind='wide',bank='cole-decker-homecoming',hold=0),
 L('JUGGERNAUT',"Hey. We all made it, right?",people=['juggernaut','$pilot'],tag='workshop'),
 L('COLE',"We did. Give me a hand with this thing.",people=['cole','juggernaut'],tag='workshop'),
 L('DECKER',"You actually brought the gun back.",id='B503',kind='insert',bank='hq-chaingun-inspection',tag='workshop'),
 L('COLE',"Nearly killed us. Figured it owed us something.",people=['cole','decker'],tag='workshop'),
 L('JUGGERNAUT','Can I have it?',people=['juggernaut','decker'],tag='workshop'),
 L('DECKER','No.',people=['juggernaut','decker'],tag='workshop'),
 L('JUGGERNAUT','Had to ask.',people=['juggernaut','decker'],tag='workshop'),
 L('CAPTION','Later that night.',kind='insert',bank='hq-salvage-diagnostics',duration=2.2,tag='workshop'),
 L('DECKER',"It works. I can fit the squad with these.",upgrade=5,tag='workshop'),
 L('COLE',"Keep my rig as it is. Get everybody else ready.",people=['cole','decker'],tag='workshop'),
 L('JUGGERNAUT',"Now that's heavy metal.",kind='insert',bank='hq-heavy-metal',tag='workshop'),
 L('DECKER','Cole. Come look at this.',id='B505',kind='insert',bank='radar-acquisition',action='alarm',cue='stage3AtomicSiren',cueAt=1.0),
 L('COLE',"How many?",people=['cole','decker']),
 L('DECKER',"Too many. They're coming down on the city.",kind='insert',bank='radar-acquisition',hold=5),
 L('COLE',"[Guard names], hold the base. Everyone else, with me."),
 L('PILOT',"On your wing.",id='B507',kind='travel',art='sky',cue='jetDash'),
],
'post-6':[
 L('TECH','$routeReport',id='B601'),
 L('COLE','Everybody answer me. Need to hear your voices.'),
 L('FREEZER','Still here.',people=['axel','freezer']),
 L('TECH',"But the orders haven't stopped."),
 L('PILOT','We took out the carrier.'),
 L('TECH',"It was passing them along. Something below the city is still talking.",kind='insert',bank='subsurface-search'),
 L('YURI','Under that bridge?',people=['yuri','$tech']),
 L('TECH','In the drains. Look.',kind='insert',bank='river-arrival',hold=3),
 L('PILOT',"Mark the other contacts. We'll deal with them if we have to."),
 L('TECH',"Check your gear before you go under. I don't like how narrow that looks.",upgrade=6),
 L('PILOT','Keep talking to me. All the way in.',kind='travel',art='river-arrival'),
],
'arrival-7':[
 L('TECH',"Low under the bridge. There's your entrance.",id='A701',kind='wide',bank='river-arrival',hold=5),
 L('PILOT','I see it. Going in.'),
],
'post-7':[
 L('PILOT',"It's opening something.",id='B701',kind='portal',art='sewer'),
 L('TECH',"Back out. I can't see what's on the other side."),
 L('PILOT',"That's where the orders are coming from."),
 L('TECH','Then take me with you. Keep this line open.'),
 L('PILOT',"Don't go quiet on me.",kind='portal',art='sewer'),
],
'ending':[
 L('PILOT','$techName? Anybody?',id='E01',kind='wide',bank='city-takeover',hold=0),
 L('TECH',"I'm here."),
 L('PILOT','Is it over?'),
 L('TECH','The machines have stopped. All of them.'),
 L('PILOT',"Then let's go home.",kind='wide',bank='cole-decker-homecoming'),
 L('COLE','Fury flight. Talk to me.',kind='wide',bank='hq-conference',hold=3),
 L('AXEL','Axel. Home.',people=['axel','freezer']),
 L('FREEZER','Freezer. Still on his wing.',people=['axel','freezer']),
 L('YURI','Yuri. I should call my parents.',people=['yuri','cole']),
 L('COLE','Tell them you did good.',people=['yuri','cole']),
 L('FALVA','Mom is going to have questions.',people=['falva','lizzie']),
 L('LIZZIE',"You answer them. I'm going to sleep.",people=['falva','lizzie']),
 L('MAVERICK','Maverick. You can stop worrying now.',people=['maverick','cole']),
 L('DECKER',"Decker. Before you ask, the coffee's gone cold.",people=['cole','decker']),
 L('COLE',"I'll live.",people=['cole','decker']),
 L('JUGGERNAUT',"Juggernaut. I've got a song for this.",kind='wide',bank='juggernaut-guitar'),
 L('FREEZER','Does it have a volume knob?',people=['freezer','juggernaut']),
 L('JUGGERNAUT','Not one I use.',people=['freezer','juggernaut']),
 L('CAPTION','Everybody home.',kind='wide',bank='hq-conference',hold=3,duration=2.5),
],
'sting':[
 L('CAPTION','Far from Earth, a receiver wakes.',kind='wide',art='space',duration=2.8),
 L('SYSTEM','',kind='insert',bank='radar-acquisition',hold=2,duration=2.2,cue='blip',cueAt=1.2),
],
}

for scene,shot in [('post-5','B501'),('ending','ENDING-05')]:
 # A short real top-view flight replaces the rejected pseudo-3D hangar plate.
 if scene=='post-5':b=next(b for b in scenes[scene]if b.get('id')==shot)
 else:b=scenes[scene][4]
 b.pop('bank',None);b['kind']='travel';b['art']='earth'if scene=='ending'else'sky'
for name,rows in scenes.items():
 for i,b in enumerate(rows):
  b.setdefault('id',name.upper().replace('-','')+'-'+str(i+1).zfill(2))
  words=len(re.findall(r"\b[\w']+\b",b['text']))
  b.setdefault('duration',round(max(1.65,b['text'].__len__()/30+1.0,words/3.4+.55),2)if b['text']else 2.0)
  b.setdefault('kind','dialogue');b.setdefault('style',i%2)
  if 'people'not in b:b['people']=['cole','decker']if b['who']in ['COLE','DECKER']else['$pilot','$tech']

data=dict(revision=1,purpose='Human crew conversations; clear evidence-to-destination links; authored16-bit comic pages.',scenes=scenes,
 voices={
 'cole':'Calm, direct, observant. Checks on people before equipment. Knows Decker\'s work well enough to spot a moved coil.',
 'decker':'Clever and practical, with dry humor. Explains what a discovery means; never narrates menus or speaks in diagnostic labels.',
 'yuri':'Russian-American, raised in America after his parents fled with him at four during Cold War tensions. No fake accent. Notices the civilians beneath the fight.',
 'axel':'The experienced air-force commander. Short, dependable calls. Trusts Freezer without needing to say so.',
 'freezer':'Axel\'s former wingman and close friend. Relaxed, dry, loyal. A joke relieves pressure rather than erasing danger.',
 'falva':'American sister in pink, glasses, practical confidence. She and Lizzie learned together while repairing their late WWII-pilot grandfather\'s bomber, encouraged by their mother.',
 'lizzie':'American sister in yellow, hoop earrings, no glasses. Warm and blunt. Her answers ground Falva\'s confidence in what is actually happening.',
 'maverick':'Teal, green aviators, hired gun who chose Cole\'s team. Arrogant enough to joke, loyal enough to stay; never cruel to the crew.',
 'juggernaut':'Huge tattooed pilot in an open dark vest. A protective teddy bear with a thrash/progressive-metal habit. Strength and warmth first, jokes second.'},
 continuity=[
 'Earth begins at peace; Fury Division is a secret elite international pilot program.',
 'The networked machinery turns hostile. Decker cuts the jets\' receivers; manual/local control explains why Fury can still fly.',
 'The first repeating orders lead to the volcanic belt, then the ice relay. A recovered recorder points to the launch airfield.',
 'The airfield\'s launch camera shows symbiote code taking over a satellite. Its backup power cell makes the orbital refit possible.',
 'The Photon Cannon is a bench prototype. Its demonstration grants no weapon tier. Earned equipment and every pilot\'s actual progression remain native.',
 'Maverick\'s homing lasers stay fixed. Do not promise him elemental or chaingun conversions.',
 'The eight-gate warp is optional and keeps its real return to Stage5. The two Stage6 outcomes retain their separate surviving contacts and optional pursuit.',
 'The city battle exposes a source in the drains, the Warden\'s breach leads to Dracodia, and defeating him stops the orders.',
 'Pilot/co-op selections retain their actual names, aircraft, colors, guard assignments and continuation. A crew conversation never changes a save, reward or combat rule.'
 ])
(PACK/'source/human-story.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
story='''# Bullets of Fury — Everybody Home

Earth has enjoyed years of peace. Hidden away from the public, Fury Division brings together exceptional pilots from around the world. They train, argue, fix their aircraft and look after one another. Cole leads them; Decker builds the things that keep them alive. Most days, their greatest emergency is getting Decker to leave his workbench.

Then the orders arrive. Vehicles, power systems and defense machines begin attacking the people they were built to serve. No one knows who is commanding them. Decker cuts the jets off from remote control, leaving the crew able to fly by hand. Cole sends them out to protect the people trapped below. Interference breaks up the squad channel, but a repeating enemy transmission gives the isolated pilot a direction to follow.

The trail runs through the volcanic belt and an ice relay. Recovering a recorder finally gives the team something they can hold in their hands. At HQ, the pilots gather around the conference table. Decker can trace the transmitter to an airfield, but still cannot name whoever is behind it. They also need that airfield's backup power cell: their fighters will need protection and power for a trip beyond the atmosphere.

Before the next flight, Cole notices something new on Decker's bench. They share the small pleasure of a project that works: a laser array, then a Photon Cannon. Cole knows the build because he helped. He hugs his friend; Decker protests about his ribs. The weapon is not ready to fly, but for a moment they have something to look forward to. Then Cole goes to get the cell.

The airfield's launch camera answers the first big question. Symbiote code entered a satellite and used its downlink to spread the same hostile orders across Earth. The crew now knows why the machines turned, and where they must go to stop the commands. Decker finishes the space kits. Falva is determined; Lizzie reminds her that their grandfather's old bomber at least had air outside it.

In orbit, the fight becomes stranger and more dangerous. An optional gate can throw the pilots into a distant battle before they find their way back. Chronos nearly destroys them, but his recovered gun becomes something useful on Decker's bench. The crew has barely caught its breath when the radar fills with contacts descending toward the city. They go out again.

Defeating the carrier or the rebel formation does not stop the orders. Decker follows the remaining signal below the city, into a drainage line beneath a bridge. The surviving aircraft can be pursued separately. In the drains, the Warden opens a breach. This time the pilot knows the choice: stay outside while the attack continues, or follow the commands to their source. The crew keeps the channel open.

When Dracodia falls, the radios go quiet for an awful moment. Then Decker answers. The machines have stopped. The ending belongs to the people who made it back: Axel and Freezer still together, Yuri thinking about his parents, the sisters bracing for their mother's questions, Maverick pretending no one needed to worry about him, Decker with cold coffee, and Juggernaut already planning a very loud song. Cole asks the question he asked at the start. This time every voice answers. Everybody home.

The story never needs the crew to explain a menu. Instruments show the evidence; the people tell us why it matters.

'''
parts=[story,'## Shooting script\n\nPILOT means the selected player. TECH means the available technical partner. Bracketed staging is visual direction, not spoken dialogue. The optional gate and route variants only play when their real campaign event occurs.\n\n']
for name,rows in scenes.items():
 parts.append('### '+name.replace('-',' ').title()+'\n\n')
 for b in rows:
  if b['kind']!='dialogue':parts.append('['+b['kind']+': '+b.get('bank',b.get('art',''))+']\n\n')
  if b['text']:parts.append('**'+b['who']+':** '+b['text']+'\n\n')
  else:parts.append('[Brief visual beat. No explanatory speech.]\n\n')
parts.append('## Voice and continuity notes\n\n')
for name,voice in data['voices'].items():parts.append('**'+name.title()+':** '+voice+'\n\n')
parts.append('\n'.join('- '+x for x in data['continuity'])+'\n')
(PACK/'BULLETS_OF_FURY_STORY_AND_SCRIPT.md').write_text(''.join(parts),encoding='utf8')
print(json.dumps(dict(scenes=len(scenes),lines=sum(len(r)for r in scenes.values()),seconds=round(sum(b['duration']for r in scenes.values()for b in r),1))))
if __name__=='__main__':pass
