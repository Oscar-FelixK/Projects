from PIL import Image, ImageMath, ImageOps
import cv2
import numpy as np

im = Image.open(r"C:\Users\oscar\Desktop\Coding Stuff\Image_pix\images\flatfrog.jpg")
#im.show()
im = im.convert("RGB")  # ensure RGB mode
size = im.size
print(size, im.mode)
box = (0, 0, 10, 10)
region = im.crop(box)
#region.show()

def color_avg(region):
    region_size = region.size
    region_pix = np.array(region.getdata()).reshape(region_size[0], region_size[1], 3)
    #print(region_pix[:,:,0])
    rbg_avg = [np.mean(region_pix[:,:,0]),np.mean(region_pix[:,:,1]),np.mean(region_pix[:,:,2])]
    return rbg_avg

color = color_avg(region)
plain = Image.new("RGB",(100,100),(int(color[0]),int(color[1]),int(color[2])))
big = Image.new("RGB", (100, 100), (255, 100, 0))

def pixelate(im,pixel_size):
    size = im.size
    n_pixels = [size[0]//pixel_size,size[1]//pixel_size] #how many pixels per axis
    mean_array = np.zeros((n_pixels[1],n_pixels[0],3), dtype=np.uint8) 
    for ny in range(n_pixels[1]):
        for nx in range(n_pixels[0]):
            #take small part of im and avg the color
            region_box = (nx*pixel_size, ny*pixel_size, nx*pixel_size + pixel_size, ny*pixel_size + pixel_size)
            region = im.crop(region_box)
            color = color_avg(region)
            mean_array[ny,nx] = color
    mean_im = Image.fromarray(mean_array)
    lost_size_factor = size[0] / mean_im.size[0]
    scaled_im  = ImageOps.scale(mean_im, lost_size_factor, Image.NEAREST)
    return scaled_im

    

pixel_frog = pixelate(im,5)
pixel_frog.show()
