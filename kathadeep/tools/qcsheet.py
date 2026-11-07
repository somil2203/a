import sys,glob,re
from PIL import Image, ImageDraw
fs=sorted(sys.argv[2:], key=lambda f: float(re.search(r"qc_([\d.]+)\.png",f).group(1)))
cols=6; tw,th=360,640; rows=(len(fs)+cols-1)//cols
S=Image.new("RGB",(cols*tw,rows*th))
for i,f in enumerate(fs):
    im=Image.open(f).resize((tw,th)); ImageDraw.Draw(im).text((8,th-20),re.search(r"qc_([\d.]+)",f).group(1),fill="yellow"); S.paste(im,((i%cols)*tw,(i//cols)*th))
S.save(sys.argv[1],quality=88)
