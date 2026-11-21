import os
from math import sqrt

from PIL import Image


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


    base_dir = r'About'
    # Ищем файл в порядке приоритета: PNG, JPG, JPEG
    possible_filenames = ['Preview.png', 'Preview.jpg', 'Preview.jpeg']
    background = None

    for filename in possible_filenames:
        path = os.path.join(base_dir, filename)
        if os.path.exists(path):
            try:
                # Конвертируем в RGBA, чтобы поддержать прозрачность при наложении
                background = Image.open(path, 'r').convert("RGBA")
                break
            except Exception as e:
                print(f"Ошибка при открытии {filename}: {e}")
                continue

    if background is None:
        background = Image.new(mode="RGB", size=(400, 280), color=(204, 204, 204))
    bg_w, bg_h = background.size

    if bg_w * bg_h >= 262144:
        ratio = sqrt(bg_w * bg_h // 262144)
        background = background.resize((int(bg_w // ratio), int(bg_h // ratio)))
    bg_w, bg_h = background.size

    positions = {
        "UR": (bg_w - img_w, 0),
        "Top right": (bg_w - img_w, 0),
        "UL": (0, 0),
        "Top left": (0, 0),
        "LR": (bg_w - img_w, bg_h - img_h),
        "Bottom right": (bg_w - img_w, bg_h - img_h),
        "LL": (0, bg_h - img_h),
        "Bottom left": (0, bg_h - img_h),
        "C": ((bg_w - img_w) // 2, (bg_h - img_h) // 2),
        "Center": ((bg_w - img_w) // 2, (bg_h - img_h) // 2),
    }

    # Получаем координаты. Если ключ не найден, используем "UR" (Top right)
    position = positions.get(Position_of_image, positions["UR"])
    position_and_offset = (position[0] + int(Position_of_image_offset_x * bg_w / 100), position[1] + int(Position_of_image_offset_y * bg_h / 100))



    background.paste(img, position_and_offset, img)
    os.makedirs(r'_Translation\About', exist_ok=True)
    background.save(r'_Translation\About\Preview.png')


if __name__ == '__main__':
    main("UR", 0, 0)
