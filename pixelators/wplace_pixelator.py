from PIL import Image, ImageOps, ImageEnhance
import numpy as np
from colorcompare import fit_color_all

print(fit_color_all([[0,0,0]]))
#put file path of image here:
#im = Image.open(r"file path here")
frog = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\Image_pix\images\flatfrog.jpg")
demon = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\image_pix\images\extreme.png")
puffer = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\image_pix\images\pufferfish.jpeg")
hampter = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\image_pix\images\hampter.png")

def color_avg(region):
    region_pix = np.array(region.getdata()).reshape(region.size[0], region.size[1], 3)
    return [np.mean(region_pix[:,:,0]), np.mean(region_pix[:,:,1]), np.mean(region_pix[:,:,2])] # returns average RGB value of the image



def wplace_pixelate(im,pixel_size): # returns a pixelated version with only wplace colors
    im = im.convert("RGB")
    enhancer = ImageEnhance.Brightness(im)
    enhancer.enhance(10)
    im.show()
    n_pixels = [im.size[0]//pixel_size, im.size[1]//pixel_size] #how many pixels per axis, rounded down -> small los at edges
    mean_array = np.zeros((n_pixels[1],n_pixels[0],3), dtype=np.uint8)
    fitted_array = mean_array.copy() 
    for ny in range(n_pixels[1]):
        for nx in range(n_pixels[0]): #take small part of im and avg the color
            region_box = (nx*pixel_size, ny*pixel_size, nx*pixel_size + pixel_size, ny*pixel_size + pixel_size)
            region = im.crop(region_box)
            desried_color = np.array([color_avg(region)])
            fitted_color = fit_color_all(desried_color)
            fitted_array[ny,nx] = fitted_color
            mean_array[ny,nx] = desried_color # store the color
    mean_im = Image.fromarray(mean_array)
    fitted_im = Image.fromarray(fitted_array)
    scaled_fitted_im = ImageOps.scale(fitted_im, im.size[0] / mean_im.size[0], Image.NEAREST) #rescale to original size
    scaled_mean_im  = ImageOps.scale(mean_im, im.size[0] / mean_im.size[0], Image.NEAREST) #rescale to original size
    return scaled_mean_im, scaled_fitted_im


pixel_frog, wplace_frog = wplace_pixelate(hampter,4)
pixel_frog.show()
wplace_frog.show()