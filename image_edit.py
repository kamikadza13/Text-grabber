import os
from os.path import exists as file_exists
from math import sqrt
from PIL import Image
from os.path import expanduser
import shutil


def add_custom_labe_on_preview(img_background_path: str, img_label_path: str, Position_of_image: str, Position_of_image_offset_x: int, Position_of_image_offset_y: int):

    img = Image.open(img_label_path, 'r').convert("RGBA")
    img_w, img_h = img.size
    background = Image.open(img_background_path, 'r').convert("RGBA")
    bg_w, bg_h = background.size
    if bg_w * bg_h >= 262144:
        ratio = sqrt(bg_w * bg_h // 262144)
        background = background.resize((int(bg_w // ratio), int(bg_h // ratio)))
    bg_w, bg_h = background.size
    upper_right_corner = (bg_w - img_w, 0)
    upper_left_corner = (0, 0)
    lower_right_corner = (bg_w - img_w, bg_h - img_h)
    lower_left_corner = (0, bg_h - img_h)
    center = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    match Position_of_image:
        case "UR":
            position = upper_right_corner
        case "Top right":
            position = upper_right_corner
        case "UL":
            position = upper_left_corner
        case "Top left":
            position = upper_left_corner
        case "LR":
            position = lower_right_corner
        case "Bottom right":
            position = lower_right_corner
        case "LL":
            position = lower_left_corner
        case "Bottom left":
            position = lower_left_corner
        case "C":
            position = center
        case "Center":
            position = center
        case _:
            position = upper_right_corner

    Position_of_image_offset_x = int(Position_of_image_offset_x * bg_w / 100)
    Position_of_image_offset_y = int(Position_of_image_offset_y * bg_h / 100)

    background.paste(img, (position[0] + Position_of_image_offset_x, position[1] + Position_of_image_offset_y), img)
    return background



def main(Custom_Preview_image_path, Position_of_image, Position_of_image_offset_x, Position_of_image_offset_y):


    img = Image.open(Custom_Preview_image_path, 'r').convert("RGBA")

    img_w, img_h = img.size
    a = r'About\Preview.png'
    if file_exists(a):
        background = Image.open(r'About\Preview.png', 'r').convert("RGBA")
    else:
        background = Image.new(mode="RGB", size=(400, 280), color=(204, 204, 204))
    bg_w, bg_h = background.size

    if bg_w * bg_h >= 262144:
        ratio = sqrt(bg_w * bg_h // 262144)
        background = background.resize((int(bg_w // ratio), int(bg_h // ratio)))
    bg_w, bg_h = background.size
    upper_right_corner = (bg_w - img_w, 0)
    upper_left_corner = (0, 0)
    lower_right_corner = (bg_w - img_w, bg_h - img_h)
    lower_left_corner = (0, bg_h - img_h)
    center = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)

    Position_of_image_offset_x = int(Position_of_image_offset_x * bg_w / 100)
    Position_of_image_offset_y = int(Position_of_image_offset_y * bg_h / 100)

    match Position_of_image:
        case "UR":
            position = upper_right_corner
        case "Top right":
            position = upper_right_corner
        case "UL":
            position = upper_left_corner
        case "Top left":
            position = upper_left_corner
        case "LR":
            position = lower_right_corner
        case "Bottom right":
            position = lower_right_corner
        case "LL":
            position = lower_left_corner
        case "Bottom left":
            position = lower_left_corner
        case "C":
            position = center
        case "Center":
            position = center
        case _:
            position = upper_right_corner


    background.paste(img, (position[0] + Position_of_image_offset_x, position[1] + Position_of_image_offset_y), img)
    os.makedirs(r'_Translation\About', exist_ok=True)
    background.save(r'_Translation\About\Preview.png')


if __name__ == '__main__':
    main("UR", 0, 0)
