import numpy as np
from PIL import Image, ImageDraw, ImageFont

ascii_list_ascending = "`.-':_,^=;><+!rc*/z?sLTv)J7(|Fi}C{fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
ascii_list_descending = ascii_list_ascending[::-1]
def ascii_converter(ascii_list_ordered, lenght, im):
    grey_im = im.convert("L")
    region_size = int(grey_im.size[0]/lenght)
    if region_size < 1:
        region_size = 1
    grey_arr = np.array(grey_im)
    buckets = np.linspace(0,255,len(ascii_list_ordered), dtype=int)
    asci_im = Image.new("L", grey_im.size, 255)
    draw = ImageDraw.Draw(asci_im)
    font = ImageFont.truetype("arial.ttf", region_size)
    for ny in range(int(grey_im.size[1]/region_size)):
        for nx in range(int(grey_im.size[0]/region_size)):
            mean = np.mean(grey_arr[ny*region_size:ny*region_size + region_size, nx*region_size:nx*region_size+ region_size])
            indicie = np.digitize(mean, buckets, right = False) -1
            draw.text((nx*region_size + region_size/2, ny*region_size + region_size/2), ascii_list_descending[indicie], font=font, fill="black")
    asci_im.show()
globe = Image.open(r"C:\Users\oscar\Projects-3\images\seapig.jpg")
ascii_converter(ascii_list_descending, 1000, globe)