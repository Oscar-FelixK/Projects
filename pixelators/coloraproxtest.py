from PIL import Image, ImageOps
import numpy as np

#put file path of image here:
#im = Image.open(r"file path here")
frog = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\Image_pix\images\flatfrog.jpg")
demon = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\image_pix\images\extreme.png")
puffer = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\image_pix\images\pufferfish.jpeg")

def color_avg(region):
    region_pix = np.array(region.getdata()).reshape(region.size[0], region.size[1], 3)
    return [np.mean(region_pix[:,:,0]), np.mean(region_pix[:,:,1]), np.mean(region_pix[:,:,2])] # returns average RGB value of the image

def pixelate(im,pixel_size): # returns a pixelated version of (about) the same size
    im = im.convert("RGB")
    n_pixels = [im.size[0]//pixel_size, im.size[1]//pixel_size] #how many pixels per axis, rounded down -> small los at edges
    mean_array = np.zeros((n_pixels[1],n_pixels[0],3), dtype=np.uint8) 
    for ny in range(n_pixels[1]):
        for nx in range(n_pixels[0]): #take small part of im and avg the color
            region_box = (nx*pixel_size, ny*pixel_size, nx*pixel_size + pixel_size, ny*pixel_size + pixel_size)
            region = im.crop(region_box)
            mean_array[ny,nx] = color_avg(region) # store the color
    mean_im = Image.fromarray(mean_array)
    scaled_im  = ImageOps.scale(mean_im, im.size[0] / mean_im.size[0], Image.NEAREST) #rescale to original size
    return scaled_im


pixel_frog = pixelate(frog,10)
pixel_frog.show()


