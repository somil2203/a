import sys
from PIL import Image, ImageDraw, ImageFont
f=ImageFont.truetype("/home/user/a/kathadeep/fonts/SpaceMono-Bold.ttf",16)
out=sys.argv[1]; ids=sys.argv[2:]; tiles=[]
for i in ids:
    im=Image.open(f"full/{i}.jpg").convert("RGB"); s=560/max(im.size); im=im.resize((int(im.width*s),int(im.height*s)))
    d=ImageDraw.Draw(im)
    for k in range(1,10):
        x=im.width*k/10; y=im.height*k/10
        d.line((x,0,x,im.height),fill=(0,255,255),width=1); d.line((0,y,im.width,y),fill=(0,255,255),width=1)
        d.text((x+2,2),str(k),fill=(255,255,0),font=f); d.text((2,y+2),str(k),fill=(255,255,0),font=f)
    c=Image.new("RGB",(580,600),(30,30,30)); c.paste(im,(10,30)); ImageDraw.Draw(c).text((10,5),f"{i} {im.width}x{im.height}",fill="white",font=f); tiles.append(c)
cols=3; rows=(len(tiles)+cols-1)//cols; S=Image.new("RGB",(580*cols,600*rows))
for k,t in enumerate(tiles): S.paste(t,((k%cols)*580,(k//cols)*600))
S.save(out,quality=88)
