from PIL import Image, ImageOps, ImageColor, ImageMath
import numpy as np
import scipy
from pathlib import Path
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
from PIL import Image, ImageDraw, ImageFont

all_colors_hex = np.array([
  "#000000",
  "#3c3c3c",
  "#787878",
  "#d2d2d2",
  "#ffffff",
  "#600018",
  "#ed1c24",
  "#ff7f27",
  "#f6aa09",
  "#f9dd3b",
  "#fffabc",
  "#0eb968",
  "#13e67b",
  "#87ff5e",
  "#0c816e",
  "#10aea6",
  "#13e1be",
  "#60f7f2",
  "#28509e",
  "#4093e4",
  "#6b50f6",
  "#99b1fb",
  "#780c99",
  "#aa38b9",
  "#e09ff9",
  "#cb007a",
  "#ec1f80",
  "#f38da9",
  "#684634",
  "#95682a",
  "#f8b277",
  "#aaaaaa",
  "#a50e1e",
  "#fa8072",
  "#e45c1a",
  "#9c8431",
  "#c5ad31",
  "#e8d45f",
  "#4a6b3a",
  "#5a944a",
  "#84c573",
  "#0f799f",
  "#bbfaf2",
  "#7dc7ff",
  "#4d31b8",
  "#4a4284",
  "#7a71c4",
  "#b5aef1",
  "#9b5249",
  "#d18078",
  "#fab6a4",
  "#dba463",
  "#7b6352",
  "#9c846b",
  "#d6b594",
  "#d18b51",
  "#ffc5a5",
  "#6d643f",
  "#948c6b",
  "#cdc59e",
  "#333941",
  "#6d758d",
  "#b3b9d1"
])

all_color_names = [
    # --- Free ---
    "Black", "Dark Gray", "Gray", "Light Gray", "White",
    "Deep Red", "Red", "Orange", "Gold", "Yellow", "Light Yellow",
    "Dark Green", "Green", "Light Green",
    "Dark Teal", "Teal", "Light Teal", "Cyan",
    "Dark Blue", "Blue", "Indigo", "Light Indigo",
    "Dark Purple", "Purple", "Light Purple",
    "Dark Pink", "Pink", "Light Pink",
    "Dark Brown", "Brown", "Beige",
    # --- Premium ---
    "Medium Gray", "Dark Red", "Light Red",
    "Dark Orange", "Dark Goldenrod", "Goldenrod", "Light Goldenrod",
    "Dark Olive", "Olive", "Light Olive",
    "Dark Cyan", "Light Cyan", "Light Blue",
    "Dark Indigo", "Dark Slate Blue", "Slate Blue", "Light Slate Blue",
    "Dark Peach", "Peach", "Light Peach",
    "Light Brown", "Dark Tan", "Tan", "Light Tan",
    "Dark Beige", "Light Beige",
    "Dark Stone", "Stone", "Light Stone",
    "Dark Slate", "Slate", "Light Slate"
]


def hex_to_rgb(hex_list):
    rgb_list = np.zeros((len(hex_list),3), dtype=int)
    for i in range(len(hex_list)):
        rgb_list[i] = ImageColor.getrgb(hex_list[i])
    return rgb_list

def rgb_to_Lab(RGB):
    RGB = sRGBColor(RGB[0], RGB[1], RGB[2], is_upscaled=True)
    if not hasattr(np, "asscalar"):#?? numpy magic
        np.asscalar = lambda a: a.item()
    return convert_color(RGB, LabColor)

wplace_all_rgb = hex_to_rgb(all_colors_hex)

wplace_labs = []
for rgb in wplace_all_rgb:
    wplace_labs.append(rgb_to_Lab(rgb))


def detlaE_fit(desired_RGB):
    desired_lab = rgb_to_Lab(desired_RGB)
    all_dE2000 = []
    for test_lab in wplace_labs:
        all_dE2000.append(delta_e_cie2000(desired_lab,test_lab))
    index_best_Match = np.argmin(all_dE2000)
    return wplace_all_rgb[index_best_Match]

def fit_color_all(original_RGB):
    vecotr_distances = scipy.spatial.distance.cdist(original_RGB, wplace_all_rgb, 'euclidean')
    index_best_Match = np.argmin(vecotr_distances)
    return(wplace_all_rgb[index_best_Match])


rgb = np.array([0,0,0])
lab = rgb_to_Lab(rgb)
rgb2 = np.array([255,123,10])
lab2 = rgb_to_Lab(rgb2)



# get a font
fnt = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size=20)


def create_legend():
    n_colors = len(all_colors_hex)
    out = Image.new("RGB", (210,20+30*n_colors+5), (255, 255, 255))
    d = ImageDraw.Draw(out)
    for color_index in range(n_colors):
        d.text([35,20*color_index+10*color_index,30,20+30*color_index], str(color_index) + " " + all_color_names[color_index], font=fnt, fill=(0,0,0))
        rgb_tuple = (wplace_all_rgb[color_index,0], wplace_all_rgb[color_index, 1], wplace_all_rgb[color_index, 2])
        d.rectangle([10,20*color_index+10*color_index,30,20+30*color_index], fill = rgb_tuple)
    return out

