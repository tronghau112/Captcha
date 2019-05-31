import os
from os import listdir
from os.path import join
from PIL import Image, ImageDraw, ImageFont
import random
import glob

OUTPUT_DIR = 'images/'

a = "fonts/"

files = [os.path.join(a,f) for f in os.listdir(a)]
#print("FILE: ",str(files))
# if the output directory does not exist, create it
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

fonts = []
#with open("fonts.txt") as f:
    #content = f.readlines()
for f in files:
    #print("FILEf: ",str(f))
    fnt = ImageFont.truetype(f, 15)
    #print("fnt: ",str(fnt))
    fonts.append(fnt)
words = set()
for font in fonts:
    #print("font",font)
    for i in range(0, 4000):
        word = ""
        for j in range(0, 4):
            word += random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        if word in words:
            continue

        img = Image.new("1", (72, 24))
        img.paste((1), [0, 0, img.size[0], img.size[1]])

        d = ImageDraw.Draw(img)
        #font = random.choice(fonts)
        d.text((16,4), word, font=font, fill=(0))
        img.save(OUTPUT_DIR + word + '.png')
        words.add(word)
        print("Captcha: ",word)
print("DONE")