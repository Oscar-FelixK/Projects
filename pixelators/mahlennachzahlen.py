from PIL import Image, ImageDraw, ImageFont
from colorcompare import wplace_all_rgb, all_color_names, create_legend
import numpy as np
from PIL import Image, ImageOps, ImageColor, ImageMath
from wplace_pixelator_deltaE import color_avg
from tqdm import tqdm


hank_pixeled = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\image_pix\images\hankpixeled.png")

def get_wplace_index(sample):
    for index, color in enumerate(wplace_all_rgb):
        if np.array_equal(sample, color):
            return index

def numerator(pixel_art, pixel_resolution):
    pixel_art = pixel_art.convert("RGB")
    size = pixel_art.size
    pixel_size = size[0]/pixel_resolution[0]
    desried_pixelsize = 20
    desired_size = desried_pixelsize*pixel_resolution[0]
    strecht_factor = desired_size/size[0]
    pixel_art = ImageOps.scale(pixel_art, strecht_factor , Image.NEAREST)
    size = pixel_art.size
    pixel_size = size[0]/pixel_resolution[0]
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size=pixel_size-2)
    d = ImageDraw.Draw(pixel_art)
    n_steps = pixel_resolution[0] * pixel_resolution[1]
    pbar = tqdm(total = n_steps)
    for ny in range(pixel_resolution[1]):
        for nx in range(pixel_resolution[0]):
            region_box = (nx*pixel_size, ny*pixel_size, nx*pixel_size + pixel_size, ny*pixel_size + pixel_size)
            region = pixel_art.crop(region_box)
            region_array = np.array(region)
            #pixel_color = color_avg(region)
            region_sample = region_array[7,7]
            color_index = get_wplace_index(region_sample)
            pbar.update(1)
            if region_sample.mean() > 128:
                opp_color = (0,0,0)
            else: 
                opp_color = (255,255,255)
            #opp_color = (abs(int(region_sample[0])-228),abs(int(region_sample[1])-228),abs(int(region_sample[2])-228))
            d.text([nx*pixel_size, ny*pixel_size, nx*pixel_size + pixel_size, ny*pixel_size + pixel_size], str(color_index), font=font, fill=opp_color)
    legend_im = create_legend()
    height_factor = size[1] / legend_im .size[1]
    legend_im = ImageOps.scale(legend_im, height_factor , Image.NEAREST)
    out = Image.new("RGBA", (size[0] + legend_im.size[0], size[1]))
    out.paste(pixel_art)
    out.paste(legend_im, (size[0],0))
    print(size, pixel_size)
    return out

