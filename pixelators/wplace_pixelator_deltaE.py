from PIL import Image, ImageOps, ImageEnhance
import numpy as np
from colorcompare import detlaE_fit
from tqdm import tqdm


#put file path of image here:
#im = Image.open(r"file path here")


def color_avg(region):
    region_pix = np.array(region.getdata()).reshape(region.size[0], region.size[1], 3)
    return [np.mean(region_pix[:,:,0]), np.mean(region_pix[:,:,1]), np.mean(region_pix[:,:,2])] # returns average RGB value of the image



def wplace_pixelate(im,pixel_size): # returns a pixelated version with only wplace colors
    im = im.convert("RGB")
    n_pixels = [im.size[0]//pixel_size, im.size[1]//pixel_size] #how many pixels per axis, rounded down -> small los at edges
    mean_array = np.zeros((n_pixels[1],n_pixels[0],3), dtype=np.uint8)
    fitted_array = mean_array.copy() 
    n_steps = n_pixels[0] * n_pixels[1]
    pbar = tqdm(total = n_steps)
    for ny in range(n_pixels[1]):
        for nx in range(n_pixels[0]): #take small part of im and avg the color
            region_box = (nx*pixel_size, ny*pixel_size, nx*pixel_size + pixel_size, ny*pixel_size + pixel_size)
            region = im.crop(region_box)
            desried_color = color_avg(region)
            #print("want",desried_color)
            fitted_color = detlaE_fit(desried_color)
            #print("got",fitted_color)
            fitted_array[ny,nx] = fitted_color
            mean_array[ny,nx] = desried_color # store the color
            pbar.update(1)
    mean_im = Image.fromarray(mean_array)
    fitted_im = Image.fromarray(fitted_array)
    scaled_fitted_im = ImageOps.scale(fitted_im, im.size[0] / mean_im.size[0], Image.NEAREST) #rescale to original size
    scaled_mean_im  = ImageOps.scale(mean_im, im.size[0] / mean_im.size[0], Image.NEAREST) #rescale to original size
    return scaled_mean_im, scaled_fitted_im, n_pixels


