"""Measure physical eye lamps before accepting the actual generated head turns."""
from pathlib import Path
import json,math
import numpy as np
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/volcano_head_1019';O=R/'_shots/overnight_combat_1019/volcano'
P=np.array([[54.,70.],[71.,70.]])-64
def lamp(im,expected):
 a=np.asarray(im);yy,xx=np.indices(a.shape[:2]);distance=(xx-expected[0])**2+(yy-expected[1])**2
 m=(a[:,:,0]>175)&(a[:,:,1]>35)&(a[:,:,2]<190)&(a[:,:,3]>180)&(distance<7**2)
 weight=np.where(m,(7-np.sqrt(distance)).clip(0)**2*np.maximum(1,a[:,:,0].astype(float)-150),0)
 assert weight.sum()>0,('lamp missing',expected.tolist())
 return np.array([(weight*xx).sum()/weight.sum(),(weight*yy).sum()/weight.sum()])
def register(im,angle):
 c,s=math.cos(angle),math.sin(angle);rot=np.array([[c,s],[-s,c]])
 Q=np.array([lamp(im,64+p@rot) for p in P]);q=Q-Q.mean(0);p=P-P.mean(0)
 angle=math.atan2(float(np.sum(p[:,0]*q[:,1]-p[:,1]*q[:,0])),float(np.sum(p*q)))
 c,s=math.cos(angle),math.sin(angle);rot=np.array([[c,s],[-s,c]])
 center=(Q-P@rot).mean(0);error=float(np.sqrt(np.mean(np.sum((center+P@rot-Q)**2,axis=1))))
 return dict(angle=angle%(math.pi*2),center=center.tolist(),eyes=Q.tolist(),error=error,eyeSpan=float(np.linalg.norm(Q[1]-Q[0])))
reference=Image.open(S/'reference.png').convert('RGBA')
P=np.array([lamp(reference,p+64) for p in P])-64
rows=[];sheet=Image.new('RGBA',(1024,4*148),(8,13,23,255));d=ImageDraw.Draw(sheet)
for quarter in range(4):
 for step in range(1,9):
  # PixelLab returns an unchanged input at index0. Accept only generated
  # drawings1..8 from each quarter, with no duplicated input holds.
  im=Image.open(S/f'turn-{quarter}/frame_{step:02}.png').convert('RGBA');expected=(quarter+step/8)*math.pi/2
  reg=register(im,expected);i=len(rows);x=i%8*128;y=i//8*148;sheet.alpha_composite(im,(x,y))
  for lx,ly in reg['eyes']:d.ellipse((x+lx-2,y+ly-2,x+lx+2,y+ly+2),outline='#37ffb0')
  d.line((x+61,y+64,x+67,y+64),fill='#50aaff');d.line((x+64,y+61,x+64,y+67),fill='#50aaff')
  d.text((x+3,y+128),f'{i}: {reg["angle"]*180/math.pi:.0f} / {reg["eyeSpan"]:.1f}',fill='white')
  rows.append(dict(index=i,quarter=quarter,step=step,expected=expected,source=f'turn-{quarter}/frame_{step:02}.png',**reg))
sheet.save(O/'turns-registration.png');(S/'measured.json').write_text(json.dumps(dict(referenceEyes=(P+64).tolist(),rows=rows),indent=2)+'\n')
print(json.dumps(dict(frames=len(rows),maxCenterDrift=max(math.dist(r['center'],[64,64]) for r in rows),spanRange=[min(r['eyeSpan'] for r in rows),max(r['eyeSpan'] for r in rows)],maxFit=max(r['error'] for r in rows))))
