import numpy as np
from PIL import Image, ImageDraw, ImageFont
 #1. get target image and split into desired amount of squares
#2. calculate the averga rgb (or others) value for each sqaure ->(gpu??)

example_image = Image.open(r"C:\Users\oscar\Projects-3\images\seapig.jpg")
def image_partition_avg_rgb(partition_size, im):
    pass

#get starting image and do the same

#compare the avg values and find best match for each by magic
#easy way: check diff between all valkues and then chose that (con: missing better matches for alter pixels)
#gpu!!

#animta transformation??