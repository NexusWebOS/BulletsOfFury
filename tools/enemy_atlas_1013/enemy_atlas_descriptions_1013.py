# Source-backed per-type notes. This is catalogue data, never a combat implementation.
# Projectile identifiers below are literal native eShootT/fire release kinds.
native_notes={}
def notes(controller, rows, file='assets/game.js'):
 for typ, title, kinds, description in rows:
  native_notes[typ]=(controller,title,kinds.split() if kinds else [],description,file)
notes('s4ChaseTick',[
 ('s4airfield','Center-lane cannon spread','s4steel','Advances through the center lane and releases an aimed three-round cannon spread.'),
 ('s4tractor','Paired brass brackets','s4brass','Advances with a sideways sway. Two turrets bracket the lane with brass rounds, leaving space between the banks.'),
 ('s4interceptor','Crossing nose burst','s4brass','Crosses the arena laterally and fires a three-round nose burst.'),
 ('s4command','Outer-nacelle rail fans','s4rail','Holds a high firing station with a shallow drift; the outer nacelles alternate rail-round fans.'),
 ('s4barrel','Explosive scenery','','Terrain-anchored explosive prop. It has no active firing sequence.'),
 ('s4tanker','Rear fuel-bomb pair','s4bomb','Advances with the convoy, swaying slowly and dropping paired accelerating fuel bombs behind it.'),
 ('s4bomber','Descending bomb ladder','s4bomb','Makes a lateral bombing run, dropping three bombs as a descending ladder.'),
 ('s4heavyjet','Twin missile-rack dive','s4missile','Makes a slow dive, releases twin missile racks, then accelerates away.'),
 ('s4missile','Parallel rocket racks','s4rocket','Holds its road lane with a slow advance and launches two parallel accelerating rocket racks.'),
 ('s4rocket','Diagonal rocket fan','s4rocket','Sweeps diagonally and releases a three-rocket fan aimed at the pilot.'),
 ('s4minitank','Machine-gun stitch','s4brass','Changes lanes sinusoidally while firing a four-round machine-gun stitch.'),
 ('s4sam','Three-lane missile wall','s4missile','Opens its launch rack during a long warning, then fills three separated lanes with missiles.')])
notes('s5SpaceTick',[
 ('s5frigate','Paired null-cannon banks','s5null','Hovers high and drifts laterally. Paired cannons fire offset null-round banks between its additional charged-beam sequences.'),
 ('s5rammer','Locked accelerating ram','','Approaches, telegraphs for 0.55 seconds, locks the target angle, then accelerates through that committed line.'),
 ('s5skimmer','Crossing chaos pair','s5chaos','Makes a fast crossing pass and fires a pair of downward chaos rounds.'),
 ('s5gravity','Gapped split-round crown','s5split','Rotates at a high station. Its fourteen-spoke crown omits the three spokes around the aimed escape sector.'),
 ('s5interceptor','Aimed fracture triplet','s5fracture','Descends in a sine weave and releases three fast aimed fracture rounds.'),
 ('s5minelayer','Split-round lane traps','s5split','Drifts high across the arena and lays three slow, accelerating split-round lanes.'),
 ('s5satellite','Divergent missile pair','s5missile','Hovers high and launches two divergent accelerating missiles; its added pressure sequence uses a separate missile fan.'),
 ('s5portalmine','Broken chaos crown','s5chaos','Spins at a hover point. Fires six spokes from an eight-spoke crown, omitting two opposite spokes.'),
 ('s5repair','Ally repair escort','','Tracks a nearby ally from behind. Repairs three scaled hull points every 0.8 seconds while within 150 pixels; it does not fire.'),
 ('s5leech','Aimed split-round shot','s5split','Descends while tracking the pilot horizontally and fires a single aimed split round.'),
 ('s5station','Fracture banks and halo','s5fracture s5halo','Oscillates broadly at a high station. Twin cannons fire three-round fans; every third release adds a large halo. Charged beams supplement this native pattern.')])
notes('s6StormTick',[
 ('s6lancer','Wind fan','s6wind','Hovers high and releases a three-round wind fan.'),
 ('s6cyclone','Corkscrew ram','','Circles in a corkscrew loop, gives a 0.52-second warning, then commits to an accelerating ram.'),
 ('s6bomber','Four-orb corridor','s6orb','Crosses laterally while its bomb rack lays a four-orb corridor.'),
 ('s6mine','Gapped lightning crown','s6bolt','Rotates at its station and fires a twelve-spoke bolt crown with three spokes omitted around the escape sector.'),
 ('s6skimmer','Crosswind orb pair','s6orb','Makes a fast crosswind pass and releases two crossing orbs.'),
 ('s6buoy','Six-spoke bolt crown','s6bolt','Legacy hover buoy with a six-spoke bolt crown. The current stage-six constructor explicitly removes this unit.'),
 ('s6dart','Slashing tracer stitch','s6tracer','Slashes through an S-shaped pass and fires a four-round tracer stitch.'),
 ('s6thunder','Twin lanes and center lance','s6bolt','Holds a high station, firing two vertical bolt lanes with a slower central lance.'),
 ('s6turbine','Countercurving wind crescents','s6wind','Hovers high and sends six wind rounds in countercurving crescent banks.'),
 ('s6probe','Locked pressure cells','s6seeker','Circles a bounded anchor at radius 42. After a long warning it places three fixed pressure cells near the pilot column.')])
notes('s7ToxicTick',[
 ('s7barge','Rotating acid gate','s7acid','Patrols slowly high in the arena, firing seven acid lanes with a rotating two-lane opening.'),
 ('s7pipe','Wall-mounted shard pair','s7shard','Descends along the left or right wall and fires paired aimed shards.'),
 ('s7tank','Three-round shard spread','s7shard','Advances into a firing station. Its modular cannon aims a spaced three-round shard spread.'),
 ('s7skimmer','Laser and acid channels','s7laser s7acid','Crosses laterally and opens three channels: a fast center laser round between two acid rounds. A charged sweep supplements this pattern.'),
 ('s7walker','Gapped grenade lanes','s7grenade','Lays three grenade lanes while leaving one lane open.'),
 ('s7lamprey','Aimed sludge triplet','s7sludge','Approaches in a sine weave and fires a three-round aimed sludge spread.'),
 ('s7sampler','Side-entry laser fan','s7laser','Enters from the side and fires a three-round laser fan from its nose.'),
 ('s7serpent','Accelerating bio pair','s7bio','Advances with sinuous motion and fires two accelerating biological rounds.'),
 ('s7mine','Gapped acid crown','s7acid','Fires a twelve-spoke acid ring with three spokes omitted for an escape opening.'),
 ('s7canister','Diagonal sludge release','s7sludge','Drifts into the arena and releases four diagonal sludge rounds once.')])
notes('s8MegaTick',[
 ('s8interceptor','Needle triplet','s8needle','Weaves while firing three fast aimed needles.'),
 ('s8manta','Blade hardpoint fans','s8blade','Sweeps broadly across a high station; three physical hardpoints each release a blade fan.'),
 ('s8deathorb','Rage crown and rift','s8rage s8rift','Rotates at a high hover point and fires a sixteen-spoke rage crown with three spokes omitted; every second release adds a rift round.'),
 ('s8parasite','Repair escort and slug','s8slug','Tracks and repairs a nearby ally while within 155 pixels, restoring four scaled hull points every 0.72 seconds. It also fires a single aimed slug.'),
 ('s8razor','Tangent blade pair','s8blade','Orbits an ellipse and releases fast paired blades along the tangent.'),
 ('s8skull','Rage burst and committed dive','s8rage','Approaches, releases eight radial rage rounds, then commits to an accelerating dive.'),
 ('s8carrier','Interceptor deployment and missile racks','s8missile','Patrols laterally high in the arena. Deploys two interceptors when the population limit allows, while two missile racks fire three-round fans.'),
 ('s8symbiote','Mirrored needle spread','s8needle','Mirrors the pilot column from the opposite side and fires a four-round fast needle spread.'),
 ('s8tentacle','Predictive slug pairs','s8slug','Hovers slowly and releases predictive slug pairs from three hardpoints.'),
 ('s8bomber','Crossing missile pair','s8missile','Makes a fast lateral pass and launches two accelerating missiles.'),
 ('s8gunship','Twin slugs and slow center shot','s8nf_gunship','Approaches into a station, firing paired shots and a slower central shot. The campaign replaces this legacy identity with a modular fighter.'),
 ('s8needlejet','Parallel needle lanes','s8nf_needle','Intercepts the pilot column and fires three parallel fast lances. The campaign uses a modular replacement for this legacy identity.'),
 ('s8scout','Predictive pulse fan','s8nf_scout','Tracks high above the pilot and fires a three-round predictive pulse fan. The campaign uses a modular replacement for this legacy identity.'),
 ('s8spread','Crossing machine-laser run','s8nf_spread','Crosses the arena at 252 pixels per second while two wing hardpoints fire vertical machine-laser slugs.'),
 ('s8crescent','Opposite-pocket blade drop','s8nf_crescent','Reads which half contains the pilot, cuts to the opposite firing pocket, then drops three blades from separate hardpoints.')])
notes('s81003EnemyTick',[
 ('s8leech','Gravity crown','s8pair','Approaches a high station, then follows a bounded elliptical orbit. Charges a radial pattern with the pilot sector omitted and releases paired energy orbs.'),
 ('s8hunter','Stalker beam pair','','Approaches a high station and orbits. Charges two parallel beam lanes around the pilot column, locks them before release, then fires the native alien beams.'),
 ('s8solar','Prism code beam','','Approaches a high station and orbits. Its charge locks a code-beam lane before release. This current controller replaces the older solar-disc volley.')], 'assets/stage8_1003.js')
notes('s9VoidTick',[
 ('s9beacon','Warp-shard spokes','warpshard','Hovers as a warp beacon and releases separated radial spokes. The current pressure controller converts its native shots to warp shards.'),
 ('s9comet','Crossing turbo shot','s9turbo','Crosses at 225 pixels per second while descending, firing a single fast downward round.'),
 ('s9gunship','Needle banks or orbital beams','s9needle','Holds a broad lateral station. The standard role fires three paired needle banks; the beam role uses two vertical orbital beams. Added charged sweeps are separate sequences.'),
 ('s9interceptor','Weaving needle fan','s9needle','Weaves broadly and fires three aimed needles. Its kamikaze role locks a dive angle, accelerates through it and releases one three-needle burst.'),
 ('s9gateturret','Six-spoke warp crown','s9warp','Rotates at its station and releases six radial warp rounds.'),
 ('s9prism','Gapped warp ring and lattice','s9warp s9lattice','Holds a high station and fires a twelve-spoke warp crown with three spokes omitted; every third release adds a large lattice round.'),
 ('s9ring','Tangent turbo pair','s9turbo','Orbits an ellipse and fires paired tangent rounds between its added radial pressure sequences.'),
 ('s9singularity','Gapped paired-energy crown','s9pair','Spins at its station and releases a fourteen-spoke crown with three spokes omitted around the escape sector.')])
notes('s9ChaosTick',[
 ('wskim','Banking photon fan','photon','Weaves and periodically barrel-rolls while firing a five-round aimed photon fan.'),
 ('pneedle','Phasing needle approach','riftshot photon','Tracks the pilot column while descending and intermittently phases. Fires a three-round spread with a rift center and photon wings.'),
 ('pmine','Rotating photon wheel','photon','Rotates at a held station and fires six radial photons with a changing angular offset.'),
 ('gleech','Edge-skimming rift fan','riftshot photon','Slides along the arena edge while slowly descending, firing a three-round spread with a rift center and photon wings.'),
 ('vmanta','Pivoting photon fan','photon','Weaves, pivots and periodically rolls while firing a five-round aimed photon fan.'),
 ('echof','Repeating echo fan','riftshot photon','Fires an aimed rift-and-photon triplet. Two older afterimages repeat it with staggered delays.'),
 ('tsplit','Split-hull rift fan','riftshot photon','Weaves and fires a three-round rift-and-photon spread. At half hull it splits off two pneedle units.'),
 ('cbreak','Breaker rift fan','riftshot photon','Weaves and periodically rolls while firing a three-round spread with a rift center and photon wings.'),
 ('horizon','Five-round event fan','riftshot','Oscillates broadly and periodically rolls, firing a five-round aimed rift fan between its additional beam sequences.'),
 ('dreadv','Seven-round dread fan','riftshot','Oscillates broadly and periodically rolls, firing a seven-round aimed rift fan between its additional ring and beam sequences.')])
notes('volcTick', [('firejet1002','Nose rocket and committed dive','s2rocket','Opens the nose during a visible tell, launches one accelerating rocket, then locks an accelerating dive. The current hull wraps the native volcanic lancer controller.')])
notes('pt11LegacyFrostTick',[('pt11frostcarrier','Frost veteran arsenal','','A former modular frost boss deployed as a stage-eight heavy. Uses the native frost encounter attack book, then withdraws after 35 seconds so it cannot stall the route.')], 'assets/playthrough_1011.js')
notes('updatePlay',[
 ('cometsm','Falling collision hazard','','Descends as a physical comet hazard; it has no firing sequence.'),
 ('cometbig','Falling collision hazard','','Large descending physical comet hazard; it has no firing sequence.'),
 ('cometmega','Falling collision hazard','','Largest descending physical comet hazard; it has no firing sequence.'),
 ('sandtank','Aimed ground cannon','groundup','Ground vehicle that advances with the scrolling terrain and fires its native ground-up cannon round.')])

for e in entries:
 typ=e['spawn'].get('type')
 if e['game']=='bof' and typ in native_notes:
  controller,title,kinds,description,file=native_notes[typ]
  e['description']=description;e['runtime']['controller']=controller
  src=ref(file,controller);e['sources'].append(src)
  # Preserve new EP13 specials, replacing the retired s8 solar/hunter base loadouts.
  if typ in ['s8leech','s8hunter','s8solar']:
   e['attacks']=[a for a in e['attacks'] if a['id'].startswith('ep13-')]
   e['projectileKinds']=[]
  e['attacks'].insert(0,{'id':'native-'+typ,'name':title,'description':description,'source':src})
  e['projectileKinds']=uniq(kinds+e['projectileKinds'])
  e.pop('attackNotes',None)
  if typ in ['s8hunter','s8solar']:e['nativeHazards']=uniq(e.get('nativeHazards',[])+['alien beam' if typ=='s8hunter' else 'code beam'])
 if e['game']=='bof' and typ and typ.startswith('l6v_'):
  e['description']='A stage-six fleet fighter with native formation movement and aimed machine-gun fire. Authored heading and roll banks follow the moving hull.'
  put_attacks(e,['machine-gun'],symbol_ref('L6_FLEET'),description='Fires aimed machine-gun rounds from the native fighter controller.');e['projectileKinds']=['mg']
 if e['game']=='bof' and typ and typ.startswith('xelite_'):
  row=R['ELITEX'].get(typ.removeprefix('xelite_'),{})
  if row:
   e['description']='Enters a high firing band, strafes toward the pilot column, and barrel-rolls away from approaching player rounds. Fires an aimed volley after reaching its station.'
   e['projectileKinds']=uniq(e['projectileKinds']+[row['kind']] if row.get('kind') else e['projectileKinds'])
   put_attacks(e,['elite-aimed-volley'],symbol_ref('elitexTick'),description=f"Releases {row.get('vol','a bank of')} aimed rounds with the native per-type spacing and cooldown.")
 if e['game']=='bof' and typ=='modturret':
  e['description']='A terrain-mounted modular emplacement. The visible weapon head aims and fires through its native machine-gun, missile, laser or sonic controller.'
  if not e['attacks']:put_attacks(e,['emplacement'],symbol_ref('modularGroundTurretTick'),description=e['description'])
  weapon=e['spawn'].get('options',{}).get('_modWeapon')
  details={'mg':'Aims and fires discrete machine-gun rounds from the weapon head.','missile':'Launches native enemy missiles from the mounted rack.','laser':'Charges and fires the native beam collision geometry from the weapon head.','sonic':'Releases the native expanding sonic hazard from the weapon head.'}
  for a in e['attacks']:a['description']=details.get(weapon,e['description'])

# Correct names that were stored with a UTF-8/Windows-1252 decoding mismatch.
def clean_text(s):
 if not isinstance(s,str):return s
 for _ in range(2):
  if not any(c in s for c in ['â','Ã','Â','ð']):break
  for encoding in ['cp1252','latin1']:
   try:
    t=s.encode(encoding).decode('utf-8')
    if t!=s:s=t;break
   except (UnicodeEncodeError,UnicodeDecodeError):pass
  else:break
 return s.replace('â€”','—').replace('â€“','–').replace('â€™',"'").replace('Â·','·')
def clean_tree(x):
 if isinstance(x,str):return clean_text(x)
 if isinstance(x,list):return [clean_tree(v) for v in x]
 if isinstance(x,dict):return {k:clean_tree(v) for k,v in x.items()}
 return x
entries[:]=clean_tree(entries)

# Overrides named in the currently loaded source files, not old wrapper names.
corrections={
 'ac10JetTick':('assets/arcade_combat_1010.js','ac10Jet'),
 'ac10RamTick':('assets/arcade_combat_1010.js','ac10Ram'),
 'p2IronTick':('assets/part2_encounters_1010.js','p2eAttack'),
 'p2StormTick':('assets/part2_encounters_1010.js','p2eAttack'),
 'j3Tick':('assets/finale_structure_1003j.js','r30Tick'),
 'sc13Sequence':('assets/stage6_carrier_1013.js','sc13BeginSequence'),
 'hd1003Start':('assets/herald_1003f.js','hd1003Tell'),
 'hk5HammerTick':('assets/hardcorps_finale_1007.js','hc7RiftStep'),
 'hc7Rook':('assets/rebel_air_1007.js','ra7HookTick'),
 'on5LaunchEncounter':('assets/overnight_routes_1005.js','on5LaunchEncounter')}
def correct_refs(x):
 if isinstance(x,list):return [correct_refs(v) for v in x]
 if isinstance(x,dict):
  sym=x.get('symbol')
  if sym in corrections:return ref(*corrections[sym])
  return {k:correct_refs(v) for k,v in x.items()}
 return x
for e in entries:
 if e['runtime'].get('controller') in corrections:e['runtime']['controller']=corrections[e['runtime']['controller']][1]
entries[:]=correct_refs(entries)

# Overdrive's current replacement campaign (fortress_1013 and convoy_1013).
odnotes={
 'odRobot':([3],'mg','od_robot_south_0','Patrol robot with authored walking/fire frames and native machine-gun bursts.'),
 'odElite':([3],'laser','od_elite_south_0','Elite patrol robot with authored motion frames and native laser projectiles.'),
 'convoyJet':([6],'missile','od_hunter_jet_0','Convoy pursuit jet. Its native convoy controller supplies the approach fields and missile release.'),
 'convoyTruck':([6],'mg','od_guntruck_0','Moving convoy guntruck that fires native machine-gun rounds.'),
 'convoyRunner':([6],'mg','od_robot_north_0','Convoy runner robot using the convoy movement controller and native machine-gun rounds.'),
 'convoyElite':([6],'laser','od_elite_north_0','Convoy elite robot using the convoy movement controller and native laser rounds.'),
 'jackal':([2],'mg','od_jackal_0','Armored chassis with native turret rotation and a machine-gun burst.'),
 'lancer':([2],'snipe','od_lancer_0','Armored chassis with native turret rotation and a sniper shot.'),
 'manticore':([2],'missile','od_manticore_0','Armored chassis with native turret rotation and a rocket attack.'),
 'bastion':([2],'shell','od_bastion_0','Armored chassis with native turret rotation and twin shells.')}
for e in entries:
 if e['game']!='overdrive':continue
 typ=e['spawn'].get('type');kind=e['spawn'].get('kind')
 if typ in odnotes:
  stages,projectile,key,description=odnotes[typ];e['stages']=stages;e['spawn']['stage']=stages[0];e['description']=description
  e['projectileKinds']=[projectile];set_art(e,[key]);e['attacks']=[{'id':projectile,'name':human(projectile),'description':description,'source':ref('expansion/topdown/js/armor_1013.js' if typ in ['jackal','lancer','manticore','bastion'] else 'expansion/topdown/js/convoy_1013.js' if typ.startswith('convoy') else 'expansion/topdown/js/fortress_1013.js','TD.unitTick')}]
 if kind=='gosfer':
  e['name']='GOSFER';e['stages']=[3];e['spawn']['stage']=3;e['description']='Current mission-three boss. Cycles through three laser-volley phases and dodges in response to approaching player projectiles.';set_art(e,['od_gosfer_south_1']);e['projectileKinds']=['laser']
  put_attacks(e,['laser-volley','projectile-dodge'],ref('expansion/topdown/js/fortress_1013.js','makeGosfer'),replace=True,description=e['description'])
 if kind=='warrior':e['name']='THE WARRIOR'
 for a in e['attacks']:
  if a.get('id')=='pellet':a['id']='mg'
 e['projectileKinds']=['mg' if k=='pellet' else k for k in e['projectileKinds']]

# Individual controller phases: concise mechanics, with exact source identifiers retained.
attack_descriptions={
 'ep13-charge':'Charges at its physical muzzle, commits to the warned pilot angle, fires a stationary beam, then visibly recovers.',
 'ep13-sweep':'Warns the full corridor, then slides horizontally while firing a downward beam; the visible beam core defines the damaging strip.',
 'ep13-ring':'Releases difficulty-scaled radial pellet rings with a committed open sector, then yields the shared pressure turn.',
 'ep13-shards':'Releases radial warp-crystal shards with an open sector; a crystal muzzle reel marks the physical emitter.',
 'ep13-missile':'Locks a target angle and launches difficulty-scaled, spaced missile fans from the actual muzzle.',
 'ep13-rifle':'Alternates the surviving rifle modules in a difficulty-scaled burst. Each gun locks its own aim during the tell and uses the native rifle muzzle flash.',
 'BATTERY CASCADE':'The carrier triggers its six surviving turret positions one by one in travel order, creating a moving sequence of charged vertical lasers.',
 'CROSS-DECK GATES':'Paired carrier turrets fire in outside-to-inside or inside-to-outside groups. Each bank fully recovers before the next begins.',
 'ALTERNATING COMB':'Odd and even carrier turret banks alternate. The sequence reserves an open lane and allows the first bank to recover before the second.',
 'p2-battery':'Surviving left and right cannons alternate a twelve-shot machine-gun sequence. Aim stops following the pilot during the final 0.45 seconds of the warning.',
 'p2-rockets':'Surviving rocket racks alternate a short volley of shootable, non-homing missiles along the committed aim.',
 'p2-core-laser':'The core charges a native continuous beam along the committed target line, then recovers.',
 'p2-core-balls':'The core fires three beats of large energy balls; higher encounter ranks add side rounds.',
 'p2-charge':'Marks a broad movement lane, commits to a 0.65-second body charge, then returns to its firing station.',
 'p2-core-charge':'With its side weapons broken, the exposed core commits to a marked body charge and returns to station.',
 'skulls':'Surviving gun modules stagger aimed skull-energy fans. The number of rounds grows with encounter rank.',
 'lances':'Surviving wing emitters charge two offset lanes and release short alien beams. Easy omits this attack from the Herald book.',
 'salvo':'The head fires three plus encounter-rank alternating-offset energy shots, spaced 0.2 seconds apart.',
 'needle-relay':'The left and right emitters alternate aimed needle banks after a committed warning.',
 'rift-gates':'Releases warp shards through several marked columns, preserving the pilot-facing escape gate.',
 'horizon-orbit':'Releases radial warp-orb crowns with a broad open sector around the committed aim.',
 'prism-sweep':'Twin emitters step through five warned angular lanes in sequence with warp lances.',
 'tidal-scissors':'Left and right emitters alternate inward-slanting cutter banks.',
 'torpedo-hunt':'Alternates aimed torpedo banks. Torpedoes accelerate, remain shootable, and follow the warned lines.',
 'abyssal-gates':'Launches torpedoes through marked columns while preserving an open escape gate.',
 'maelstrom-crown':'Releases radial tidal crowns with a broad open sector around the committed pilot angle.',
 'hydro-sweep':'Twin emitters step through five warned angular lanes with tidal crown rounds.',
 'sentinel-warp-crown':'A sentinel releases an eight-round crown from ten possible spokes, omitting two opposite spokes. The pair alternates attack turns.',
 'sentinel-needle-fan':'A sentinel fires five needles around a committed pilot angle. The pair alternates attack turns.',
 'sentinel-fusion':'After both sentinels are disabled, they converge into an animated aperture and reveal the Tidal Sovereign. This is a transformation, not a damaging projectile.',
 'bombs':'Drops bombs from the visible belly bay toward fixed ground reticles. Furious walks the targets across five cells while preserving one safe lane.',
 'crossfire':'Surviving side emitters send paired aimed energy rounds, expanding to three-round banks at the highest encounter rank.',
 'charge':'Visible weapon charge prepares the following committed release.',
 'beam':'Surviving emitter modules sustain vertical beams after their charge warnings.',
 'lob':'The belly bay lobs rounds toward warned floor positions; the rounds burst when they arrive.',
 'carpet':'Walks a row of lobbed bombs across the pilot band while preserving an open cell.',
 'overdrive':'A transition at the Furious half-hull threshold changes the boss attack book and movement pressure.',
 'hammer-leap':'Winds up, marks a landing region and commits to the hammer jump strike.',
 'hammer-throw':'Throws the modular hammer as a separate moving weapon before retrieval.',
 'spike-ball':'Transforms into the rolling spike-ball attack, then returns to the humanoid arsenal.',
 'chromium-shield':'Raises the Chromium shield. It absorbs incoming shots and plays impact feedback rather than reflecting them.',
 'hammer-recharge':'Recharges through the hammer, exposing the marked hammer target to player fire.',
 'chain-gun':'Uses the native hammer arsenal chain-gun firing sequence.',
 'spell':'Raises the casting hand and marks several locked spell targets before release.',
 'mega-beam':'Uses a dedicated charge state before releasing the large beam.',
 'orbital-hammer':'The Furious arsenal sends the hammer through its orbital attack sequence.',
 'chromium-void-rift':'Raises the casting arm to summon a Chromium rift. Its pull and lightning pressure reward moving toward the arena edge.',
 'hammer-storm':'Calls the native hammer storm sequence with its separate warnings and recovery.',
 'rookhook':'Rook extends a modular grapple, captures a jet on contact, then pulls and throws it toward the screen edge.',
 'machine-gun':'Fires aimed machine-gun rounds through the native gun and muzzle controller.',
 'committed-ram':'Stops its former projectile queue, warns a target lane and commits to the accelerating body attack.',
 'paired-burst':'Alternates paired shots from the physical jet guns while following its attack movement.',
 'fusion':'Charges and fires the rebel pilot’s native fusion-beam ability.',
 'cloak':'Uses Nyx’s cloaking sequence and the moving spiral effect before rejoining the attack pattern.',
 'slug':'Fires Rook’s heavy slug signature through his native rebel controller.',
 'turbo':'Uses Voss’s high-speed signature movement attack.',
 'rockets':'Launches the actor’s native rocket sequence from its visible weapon mounts.',
 'helix':'Uses Jace’s native helix projectile signature.',
 'ram':'Commits to the actor’s native body-attack movement and recovery.',
 'leapSlash':'The knight winds up a jumping blade strike before committing to its attack line.',
 'shieldSmite':'The knight attacks with its shield module through the native smite sequence.',
 'blade-tempest':'The knight form releases its dedicated blade-tempest pattern.',
 'code-shockwave':'The knight form releases its dedicated code shockwave.',
 'MUTATION SPEAR':'The first final-boss phase uses its native mutation-spear signature, with phase-specific warnings and recovery.',
 'SPECTRAL RAIL RELAY':'The ghost phase uses its native staggered spectral-rail signature.',
 'COLOSSUS CROWN GATE':'The colossus phase releases its native crown pattern with a dedicated escape gate.'}

attack_descriptions.update({
 'wall':'Releases the registered wall-pattern volley from the native actor controller.',
 'strafe':'Fires during the actor’s lateral strafing pass.',
 'stagger':'Releases the actor’s shots on a staggered firing beat.',
 'burst':'Releases the actor’s native short burst, then waits for its firing cooldown.',
 'spawn':'Deploys the native child enemies from the carrier.',
 'fan':'Releases rounds across a spread of angles from the native emitter.',
 'ring':'Releases a radial ring through the native projectile controller.',
 'pincer':'Moves the paired attack arms inward through the warned region.',
 'elite-ball1002':'Alternates large energy-ball fans from left and right cannons, varying the center angle between waves.',
 'elite-beam1002':'Charges up to four surviving cannon modules, then fires two inward-slanting beam banks.',
 'elite-missile1002':'Alternates shootable missiles from surviving rocket racks; alternate missiles use the native homing behavior.',
 'elite-ram1004k':'Uses the frost elite’s committed body-charge controller and its separate warning.',
 'elite-strafe1002':'Alternates fast machine-gun stitches between the surviving side cannons, followed by a longer pause every ninth beat.',
 'missile':'Launches the actor’s registered missile weapon from its native mount.',
 'mg':'Fires the actor’s registered machine-gun rounds through its actual gun controller.',
 'volley':'Releases the registered volley from the actor’s native firing controller.',
 'kick':'Uses the native APC kick movement and firing pattern.',
 'cannon':'Fires through the actor’s native cannon controller and physical weapon mount.',
 'jungleMissile':'Launches the stage-one truck’s native jungle-missile volley.',
 'lance':'Releases the actor’s dedicated lance projectile pattern.',
 'suppression':'Razorback uses its surviving gun modules for the native suppression sequence.',
 'sonic':'Releases the native expanding sonic-wave attack.',
 'missiles':'Launches a missile sequence from the actor’s surviving launch hardware.',
 'nova':'Releases Razorback’s native radial nova pattern.',
 'rocketFlurry':'The Furious Razorback attack book adds this rapid rocket sequence between its other heavy attacks.',
 'twin-mg':'The Overlord fires its paired machine-gun mounts.',
 'rocket-volley':'Launches a spread from the native rocket hardpoints after their warning.',
 'green-volley':'The Overlord releases its dedicated green-energy volley.',
 'rotor-tempest':'Uses the Overlord’s rotor-tempest movement and attack phase.',
 'gun-sweep':'Sweeps fire from the Overlord’s gun mounts across its firing arc.',
 'missile-lock':'Warns a locked missile line before the Overlord releases its missiles.',
 'rush':'The Overlord commits to its rush movement through the arena.',
 'sonic-combo':'The Overlord chains the native sonic attack through its combo phase.',
 'ember-hunt':'Alternates three-round fans around committed aim, pausing between groups before reacquiring on a later attack.',
 'furnace-strafe':'Strafes across the arena, firing downward banks while withholding fire over its reserved safe band.',
 'magma-rain':'Uses the magma encounter’s dedicated rain sequence and its native target warnings.',
 'furnace-lance':'Charges the magma encounter’s dedicated furnace-lance attack.',
 'charred-battery':'The charred phase warns a ground battery with an open cell and supplements it with side-mounted five-round fans.',
 'ash-pursuit':'Alternates five-round aimed fans around committed target lines, with a pause after each four-wave group.',
 'ash-rain':'The charred phase uses its dedicated ash-rain sequence.',
 'charcoal-wheel':'Releases radial rounds with alternating curvature while leaving an opening around the committed pilot angle.',
 'blackout-pass':'The charred phase makes a strafing pass, firing three-round downward banks while preserving a safe band.',
 'cinder-scissors':'Alternates left and right four-round shutters; both sides do not close together.',
 'ash-eruption':'Releases paired large burst rounds on either side of the committed center line, with a pause between releases.',
 'spin900':'The Furnace arms perform the native spinning attack before recovering.',
 'sweep':'Sweeps the native weapon effect through its dedicated angular attack phase.',
 'coreLaser':'The exposed Furnace core uses its dedicated laser sequence.',
 'rollerball':'The Furnace core enters its native rollerball attack phase.',
 'rotor':'The Furnace core enters its native rotor attack phase.',
 'eyeBurst':'The Furnace head fires through its eye-burst phase.',
 'eyeSweep':'The Furnace head sweeps fire through its eye-sweep phase.',
 'ice-battery1002':'Alternates rapid machine-gun stitches between surviving ice-battery cannons, with a pause after each nine-wave group.',
 'cannon-relay':'The ice carrier sequences fire through its native cannon relay.',
 'rime-missile1004k':'The ice carrier uses its dedicated rime-missile sequence.',
 'ice-crossfire1002':'Alternates paired fast machine-gun rounds from side cannons, spreading each pair around the committed aim.',
 'glacier-press':'Releases a broad downward spread while omitting three positions around the reserved gap.',
 'rime-orbit1004k':'The ice carrier uses its native orbiting rime-projectile pattern.',
 'ap10-stormburst':'The storm carrier uses the dedicated lightning-gun stormburst sequence.',
 'storm':'The Hammer calls its native storm sequence through the hammer arsenal.',
 'tank-cross':'The tank’s surviving guns fire along their warned aim lines.',
 'caustic-lob':'Alternates aimed toxic rounds from the surviving guns. The rounds travel to marked positions and burst on arrival.',
 'tank-mortar':'Releases the tank mortar after its targeting warning.',
 'tank-charge':'Warns the lane and drives the tank toward a committed target point before recovering.',
 'tank-orbits':'Releases three separated aimed orb fans, shifting the center angle between waves.',
 'pressure-salvo':'In overpressure, surviving guns alternate three-round acid fans around committed target lines.',
 'chase':'The Warden advances toward the pilot with planted steps, then starts its chained claw swipes.',
 'chain':'Surviving Warden guns fire a sustained sequence through their warned aim lines.',
 'mortar':'The Warden launches its mortar after the native targeting warning.',
 'spore-lob':'Lobs toxic spores from alternating canisters toward warned floor positions; harder ranks add an impact burst.',
 'orbs':'Releases three separated aimed orb fans, shifting the center angle between waves.',
 'bounce':'Performs three short hops. Each landing releases a downward orb fan after its own warning beat.',
 'jump':'Rises above the arena, tracks during the early tell, then locks the landing and descends with three impact-wave beats.',
 'crawl':'The rear phase crawls toward the pilot at reduced speed, then starts the bounce sequence.',
 'aim':'Surviving guns aim and fire through the exposed-core attack sequence.',
 'portal-volley':'The exposed Furious core opens toxic portals at field edges that fire targeted balls.',
 'laser':'Opens the faceplate during the tell, then sweeps fast laser rounds from the exposed emitter.',
 's3spearburst':'The alternate Cryospear uses its registered spear-burst pattern.',
 's3spearcross':'The alternate Cryospear uses its registered crossing-spear pattern.',
 's3spearcore':'The alternate Cryospear uses its registered exposed-core spear pattern.',
 'stormbolts':'The alternate storm encounter releases its registered storm-bolt sequence.',
 'talons':'The copied host form attacks through its paired talon modules.',
 'gravity':'Uses the final-form controller’s native gravity attack.',
 'code':'Uses the final-form controller’s native code-energy attack.',
 'rotorMG':'The copied helicopter form fires its rotor machine-gun pattern.',
 'bombing':'The copied helicopter form runs its native bombing pattern.',
 'pass':'The helicopter form crosses the arena in a committed sonic broadside, then returns to its origin.',
 'magma':'The copied Furnace form releases its native magma attack.',
 'eruptions':'The copied Furnace form launches its native eruption pattern.',
 'furnaceBeam':'The copied Furnace form charges and releases its native beam.',
 'orbit':'Uses the copied form’s native orbiting projectile pattern.',
 'bellows':'The Furnace form raises its paired weapon modules and discharges its dedicated bellows beam pattern.',
 'iceGates':'The copied Cryo Hive fires its native ice-gate pattern.',
 'iceLance':'The copied Cryo Hive uses its dedicated ice-lance attack.',
 'iceSiege':'The copied Cryo Hive uses its dedicated siege sequence.',
 'glacierPress':'The copied Cryo Hive uses its native glacier-press pattern.',
 'shutters':'The Cryo Hive sequences its cannon shutters in two releases, with a full warning gap between them.',
 'lightning':'The copied Storm form fires its native lightning attack.',
 'scissors':'The Storm form rotates its cross-beam scissors, dissolves the beams, and leaves a warning gap before the next release.',
 'knight':'Uses the copied knight’s native sword-and-shield combat controller.',
 'riposte':'The knight baits with its shield, then commits to a jumping sword riposte.',
 'turbines':'The copied Harrier form attacks through its turbine modules.',
 'carrierLance':'The copied Harrier form charges its carrier-lance attack.',
 'press':'The Harrier spreads its turbine modules and sequences the beam pressure in two releases with a full warning gap.',
 'wardenMG':'The copied Warden form uses its native machine-gun modules.',
 'stomp':'The copied Warden form executes its native stomp attack.',
 'scissor':'The copied Warden form executes its native claw-scissor pattern.',
 'portalVolley':'The copied Warden form opens its native projectile portals.',
 'vault':'The Warden form leaps toward the warned target and brings its attached claws down at the end of the vault.',
 'hammer':'Uses the copied Hammer’s full native controller and modular weapon behavior.',
 'pulse':'The Sonic siege tank releases its native sonic pulse.',
 'lock':'The Deviator siege tank uses its locked-target weapon sequence.',
 'cannons':'The Devastator siege tank fires its native cannon banks.',
 'harrier-cannons':'The selected Harrier route runs its native cannon sequence.',
 'harrier-beam':'The selected Harrier route charges and fires its native beam.',
 'squad':'Runs the five Rebel Fighters together, each retaining its own weapons, movement and special ability.'})

# The stage-nine second form is reached through fusion in the current campaign.
for e in entries:
 kind=e['spawn'].get('kind');typ=e['spawn'].get('type')
 if e['game']=='bof' and kind=='tidalsovereign':
  e['status']='current';e['stages']=[9];e['spawn'].update(stage=9,role='boss');e['category']='form';e['name']='Tidal Sovereign';e['runtime']['controller']='late27Tick'
  e['description']='The second form of the stage-nine boss, revealed when the disabled Warp Sentinels fuse. Uses five committed tidal attack patterns.'
  e['audit']['statusEvidence']='s9FusionBossTick changes kind and initializes tidalsovereign after the native fusion sequence.'
  put_attacks(e,['tidal-scissors','torpedo-hunt','abyssal-gates','maelstrom-crown','hydro-sweep'],ref('assets/late_encounters_0927.js','late27Book'),replace=True)
  e['projectileKinds']=['tidalcut','tidaltorp','tidalcrown'];set_art(e,['ns9_tidal_intact'])
 if e['game']=='bof' and kind=='tidalfusion':
  e['name']='Warp Sentinels';e['description']='Two sentinels alternate committed warp crowns and needle fans. Disable both to trigger their fusion into the Tidal Sovereign.'
  put_attacks(e,['sentinel-warp-crown','sentinel-needle-fan','sentinel-fusion'],ref('assets/game.js','s9FusionWardenFire'),replace=True)
  e['projectileKinds']=['s9warp','s9needle'];e['transformsInto']='bof-legacy-boss-tidalsovereign';set_art(e,['ns9_warpsen_intact'])
 if e['game']=='bof' and kind=='voidhorizon':e['projectileKinds']=['s9needle','warpshard','warporb','warplance']
 if e['game']=='bof' and kind=='heralddeath':e['projectileKinds']=['s8pair'];e['nativeHazards']=['alien beam']
 if e['game']=='bof' and kind in ['spacebomber','siegebomber']:
  e['description']='Modular pursuit bomber. Destroying its engines reduces lateral travel; destroying laser modules removes their beam and crossfire turns.'
  e['projectileKinds']=uniq(e['projectileKinds']+['s5split' if kind=='spacebomber' else 's6orb']);e['nativeHazards']=['charged continuous beams','ground-targeted bomb impacts']
 if e['game']=='bof' and typ and typ.startswith('mm1003_'):
  k=typ.removeprefix('mm1003_');brief={
   'bluehybrid':'Enters a firing pocket, warns the pilot, then releases five blue energy rounds around a committed target angle.',
   'hexpyre':'Uses articulated casting arms. Current pressure turns release a gapped radial energy ring; breaking the casting modules cancels the attack.',
   'hellram':'Commits to a body dash, backs away to reopen space, then alternates three paired plasma salvos before returning to its firing pocket.',
   'riflelocust':'Alternates six native machine-gun shots between surviving gun modules. Its enhanced pressure turn scales the burst length by difficulty without changing the rifle weapon.',
   'impharrow':'Releases two offset energy shots from opposite sides of its hull; later pressure turns add a missile fan.',
   'furnacemaw':'Alternates two large three-round energy banks from its side hardpoints, with a later missile pressure sequence.',
   'hellhugger':'Warns and commits to a short claw dash, recovers, then leaves the arena.'}.get(k)
  if brief:
   e['description']=brief
   for a in e['attacks']:
    if not a['id'].startswith('ep13-'):a['description']=brief
  e['projectileKinds']=uniq((['mg'] if k=='riflelocust' else [] if k=='hellhugger' else ['s8pair'])+e['projectileKinds'])
 if e['game']=='bof' and typ=='pt11frostcarrier':
  frost=native_by_kind.get('frostcruiser',{}).get('books',{}).get('er26',{})
  for rank,book in frost.items():put_attacks(e,uniq(book),ref('assets/playthrough_1011.js','pt11LegacyFrostTick'),ranks=[int(rank)])
 for a in e['attacks']:
  if a['id'] in attack_descriptions:a['description']=attack_descriptions[a['id']]
 e['attackCount']=len({a['id'] for a in e['attacks']});e['projectileKinds']=uniq(e['projectileKinds'])

od_patch=json.loads((SOURCE_DIR/'overdrive_metadata_1013.json').read_text(encoding='utf-8'))
for e in entries:
 if e['id'] in od_patch:e.update(od_patch[e['id']])

# Resolve drawable hull keys before fallback aliases; never use an FX key as a hull.
preferred_art={
 'cometsm':'ns9c_sm_idle','cometbig':'ns9c_big_idle','cometmega':'ns9c_mega_idle',
 'crawl':'nvl_crawl_0','lavamaw':'nvl_maw_0','miner':'nvl_miner_0','pod':'nvl_pod_0',
 's1boatgun':'s1_boat_gun_idle','s1boatpatrol':'s1_boat_patrol_idle',
 's4barrel':'s4atk_explosive_barrel_0','s4missile':'s4atk_missile_vehicle_0',
 's4sam':'s4atk_sam_carrier_0','s4tanker':'s4atk_fuel_tanker_0','s4tractor':'sm10_desert_tractor_0',
 's6bomber':'s6atk_four_engine_bomber_0','s7barge':'tnkG_g2_idle',
 's7pipe':'sm10_toxic_pipe_0','s7tank':'overhaul_tank_7_hull',
 'sandtank':'tnkG_g2_idle','modturret':'overhaul_ground_head_mg'}
for typ in ['basaltbomber','cinderwasp','cryoeye','glaciercarrier','magmaorb','sharddart']:preferred_art[typ]='ndr_'+typ+'_idle_0'
for e in entries:
 if e['game']!='bof':continue
 typ=e['spawn'].get('type');kind=e['spawn'].get('kind');password=e['spawn'].get('password')
 if typ in preferred_art and preferred_art[typ] in X:set_art(e,[preferred_art[typ]],atlas_records)
 if kind=='damkeeper':set_art(e,['ovbody_intact'],atlas_records)
 if kind=='chromehammer':set_art(e,['arch_idle','hammer_ship'],atlas_records)
 if password=='HARR6':
  carrier=next(q for q in entries if q['id']=='bof-boss-warhive')
  e['name']='Warhive Siege Carrier · HARR6';e['attacks']=[dict(a) for a in carrier['attacks']]
  e['projectileKinds']=carrier['projectileKinds'][:];e['nativeHazards']=carrier['nativeHazards'][:];set_art(e,['s6cargo13_hull'],atlas_records)
  e['description']='The stage-six left-route password now selects the current six-turret cargo fortress. Its sequenced laser banks replace the former carrier chase.'
 if password=='XHARR':
  e['name']='Stage X Harrier / Warhive Carrier';set_art(e,['whv_closed','whv_ace'],atlas_records)
  e['description']='The Stage X left route retains the carrier deployment and ace encounter. It descends, opens its bay, deploys fighters, attacks, retreats and returns until its modules are defeated; the ace then emerges.'
  e['attacks']=[
   {'id':'fighter-deployment','name':'Fighter deployment','description':'Opens the bay and launches a formation of native escort fighters.','source':ref('assets/game.js','whvLaunchJet')},
   {'id':'carrier-cannons','name':'Carrier cannon banks','description':'Surviving nacelle cannons release their native energy-ball sequences on Hard and Furious.','source':ref('assets/game.js','whvCannonTick')},
   {'id':'carrier-beam','name':'Carrier beam','description':'Runs the carrier’s dedicated continuous-beam warning and release.','source':ref('assets/game.js','whvBeamTick')},
   {'id':'bay-mortar','name':'Bay mortar','description':'The open carrier bay fires its native targeted mortar sequence.','source':ref('assets/game.js','whvBayMortar')},
   {'id':'ace-guns','name':'Ace guns','description':'The emerging ace fires its native gun patterns between flight maneuvers.','source':ref('assets/game.js','whvAceGuns')},
   {'id':'ace-missiles','name':'Ace missiles','description':'The ace releases shootable accelerating missiles from its wing hardpoints.','source':ref('assets/game.js','whvAceFireMissiles')},
   {'id':'ace-dash','name':'Ace dash and evasion','description':'The ace commits to dashes, rolls and somersaults through its native movement controller.','source':ref('assets/game.js','whvAceDashTick')},
   {'id':'ace-desperation','name':'Ace desperation','description':'The low-hull ace uses its native desperation sequence.','source':ref('assets/game.js','whvAceDesperation')}]
  e['projectileKinds']=['emissile'];e['nativeHazards']=['carrier-owned ball and bolt arrays','carrier beam']
  e['runtime']['controller']='warhiveTick (Stage X original carrier/ace owner)'
 # Stable actual keys precede aliases such as tankA, which are not XART keys.
 actual=[k for k in e['artKeys'] if k in X]
 if actual:set_art(e,actual,atlas_records)

manifest_text=(ROOT/'assets/manifest.js').read_text(encoding='utf-8')
manifest=json.JSONDecoder().raw_decode(manifest_text.split('window.BOFX=',1)[1])[0]
path_text=(ROOT/'assets/asset_paths_1007.js').read_text(encoding='utf-8')
asset_paths=json.JSONDecoder().raw_decode(path_text.split('window.BOF_ASSET_PATHS=',1)[1])[0]
def resolve_paths(x):
 if isinstance(x,list):return [resolve_paths(v) for v in x]
 if isinstance(x,dict):return {k:asset_paths.get(v,v) if k=='path' and isinstance(v,str) else resolve_paths(v) for k,v in x.items()}
 return x
for e in entries:
 if e['game']=='bof':
  for art in e.get('art',[]):
   cell=manifest['cells'].get(art['key'])
   if cell and len(cell)>=5:
    atlas_key=cell[0];path=manifest['img'].get(atlas_key)
    if path and art.get('path')==path:
     art.update(atlasKey=atlas_key,rect=cell[1:5],crop=cell[1:5])
     if len(cell)>=9:art.update(trimOffset=cell[5:7],logicalSize=cell[7:9])
 e['attackCount']=len({a['id'] for a in e['attacks']})
entries[:]=resolve_paths(entries)
runtime_atlas=json.JSONDecoder().raw_decode((ROOT/'assets/game/shared/atlases/stage_runtime_atlases.js').read_text(encoding='utf-8').split('=',1)[1])[0]
for e in entries:
 if e['game']!='bof':continue
 for art in e.get('art',[]):
  cell=runtime_atlas['cells'].get(art['key'])
  if cell:
   path=runtime_atlas['roots'].get('nca_'+cell[0])
   if path:art.update(path=path,atlasKey=cell[0],rect=cell[1:5],crop=cell[1:5])
