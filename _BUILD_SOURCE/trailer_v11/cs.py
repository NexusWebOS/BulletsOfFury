import sys
from PIL import Image
ts=sys.argv[2:]; ims=[Image.open('takes10/%s/contact.jpg'%t) for t in ts]
ims=[i.resize((1200,int(i.height*0.75))) for i in ims]
W=Image.new('RGB',(1200,sum(i.height for i in ims)));y=0
for i in ims: W.paste(i,(0,y)); y+=i.height
W.save('/tmp/claude-0/-home-user-BulletsOfFury/8c13c194-12a8-5d1b-bf6e-85b8c00fc9ae/scratchpad/%s.jpg'%sys.argv[1])
