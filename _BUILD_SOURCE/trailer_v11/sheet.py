import sys, glob
from PIL import Image
d=sys.argv[1]; fs=sorted(glob.glob(d+'/f*.png'))[:int(sys.argv[2]) if len(sys.argv)>2 else 12]
c=6; ims=[Image.open(f).convert('RGB').resize((240,256)) for f in fs]
W=Image.new('RGB',(240*c,256*((len(ims)+c-1)//c)))
for i,im in enumerate(ims): W.paste(im,((i%c)*240,(i//c)*256))
W.save(d+'/sheet.png'); print(fs)
