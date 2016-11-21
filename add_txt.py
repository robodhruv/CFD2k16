from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import urllib
import numpy as np

#r = urllib.urlopen('http://gotravelaz.com/wp-content/uploads/images/Valley_31193.jpg')
#arr = np.asarray(bytearray(r.read()), dtype=np.uint8)

msg="infiiiiii Machaya CFD DAK ne macha diya New CSe"
img = Image.open("wolf.jpg")
draw = ImageDraw.Draw(img)
W, H = img.size
font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf", int(W/(len(msg)-5)))
w, h = font.getsize(msg)
draw.text(((W-w)/2, h/2),msg,(255,255,255),font=font)
img.save('sample-out.jpg')