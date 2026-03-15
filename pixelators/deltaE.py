from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import numpy as np

def rgb_to_Lab(RGB):
    RGB = sRGBColor(RGB[0], RGB[1], RGB[2], is_upscaled=True)
    if not hasattr(np, "asscalar"):#?? numpy magic
        np.asscalar = lambda a: a.item()
    return convert_color(RGB, LabColor)


rgb = np.array([0,0,0])
lab = rgb_to_Lab(rgb)
rgb2 = np.array([255,123,10])
lab2 = rgb_to_Lab(rgb2)

diff = delta_e_cie2000(lab,lab2)
print(diff)



'''def rgb_to_Lab(RGB_list):
    lab_list = np.zeros((len(RGB_list)))
    for i in range(len(RGB_list)):
        RGB_list[i] = sRGBColor(RGB_list[i,0], RGB_list[i,1],RGB_list[i,2], is_upscaled=True)
        if not hasattr(np, "asscalar"):#?? numpy magic
            np.asscalar = lambda a: a.item()
        lab_list[i] = convert_color(RGB_list[i], LabColor)
    return '''

