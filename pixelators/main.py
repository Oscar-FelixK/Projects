from PIL import Image, ImageOps, ImageEnhance
import numpy as np
from colorcompare import detlaE_fit
from wplace_pixelator_deltaE import wplace_pixelate
from mahlennachzahlen import numerator

#put file path of image here:
#im = Image.open(r"file path here")
frog = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\Image_pix\images\flatfrog.jpg")
demon = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\image_pix\images\extreme.png")
puffer = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\image_pix\images\pufferfish.jpeg")
hampter = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\image_pix\images\hampter.png")
hampter2 = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\image_pix\images\hampter2.jpg")
hampter3 = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\image_pix\images\hampter3.png")
hank = Image.open(r"images/Hank_Pin-Happy.png")
hank2 = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\image_pix\images\gooonn.png")
hankfinal = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\image_pix\images\600px-Brawl_Hank.png")
lace = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\image_pix\images\lacehronet.png")
hollowknight = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\image_pix\images\hk.png")
hollowknightknight = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\image_pix\images\hkbasic.png")
gitgud = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\image_pix\images\gitguuud.png")
pixel_im, wplace_im, pixel_res = wplace_pixelate(gitgud,30)
pixel_im.show()
wplace_im.show()
print("done")
print("size:", pixel_res)
numerated_im = numerator(wplace_im,pixel_res)
numerated_im.show()
