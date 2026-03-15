import numpy as np
from PIL import Image, ImageDraw, ImageFont
import taichi as ti
ti.init(arch=ti.gpu)
 #1. get target image and split into desired amount of squares
#2. calculate the averga rgb (or others) value for each sqaure ->(gpu??)

@ti.kernel
def avg_rgb_gpu(im_array: ti.types.ndarray(), n_partitions_x: ti.int32, n_partitions_y: ti.int32, partition_size: ti.int32)-> ti.int32:
    psum = 0
    for i, j in ti.ndrange(n_partitions_x, n_partitions_y):
        psum += 1
    return psum
example_image = Image.open(r"C:\Users\oscar\Projects-3\images\seapig.jpg")

def image_partition_avg_rgb(partition_size, im):
    im = im.convert("RGB")
    n_partitions = [im.size[0]//partition_size, im.size[1]//partition_size]
    im_array = np.array(im)
    psum = avg_rgb_gpu(im_array, n_partitions[0], n_partitions[1], partition_size)
    print(psum,n_partitions)


image_partition_avg_rgb(10, example_image)
#get starting image and do the same
#compare the avg values and find best match for each by magic
#easy way: check diff between all valkues and then chose that (con: missing better matches for alter pixels)
#gpu!!

#animta transformation??