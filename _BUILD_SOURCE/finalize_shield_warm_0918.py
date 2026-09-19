from pathlib import Path
p=Path('assets/game.js'); s=p.read_text(encoding='utf-8')
a="'bmbar_frame_shield','bmbar_tab_shield'"
b="'bmbar_frame_shield','bmbar_frame_shield_v2','bmbar_tab_shield'"
assert s.count(a)==1, s.count(a)
s=s.replace(a,b,1)
a='''        /* ⚠ THE GAP HAS TO CLEAR THE SHIELD BAR'S OWN TAB, not just the bar. The tab is drawn
           ABOVE whatever bar it labels, so a gap sized for the bar alone put SHIELD straight
           across the middle of the HP bar - measured at ~10px of overlap. One tab height plus a
           couple of pixels leaves it sitting in clear air between the two. */'''
b='''        /* Position the attached SHIELD nameplate below the boss gauge. */'''
assert s.count(a)==1,s.count(a);s=s.replace(a,b,1)
a='''/* ⚠ THE SHIELD HAS ITS OWN BAR (Mike, 0916: "Shield should get it's own shield like boss bar, not
   the same as the boss bar"). `bmbar_frame_shield` is the boss frame hue-ROTATED to ice - the same
   object in a second livery, so its rails, rivets, lamp and hazard block still line up and its well
   geometry is BMBAR.boss unchanged. Its well also carries a faint hex lattice, so an EMPTY shield
   bar still reads as a field rather than as an empty hp bar. It falls back to the boss frame only
   while the new plate is decoding. */'''
b='''/* The separate rectangular shield frame has a connected, centered SHIELD nameplate.
   Fill clips against the straight well, independent of the boss health gauge. */'''
assert s.count(a)==1,s.count(a);s=s.replace(a,b,1)
p.write_text(s,encoding='utf-8',newline='\n')
