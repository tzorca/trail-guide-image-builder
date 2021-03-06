import re
from PIL import Image
import os
from datetime import datetime
import json
import math


# Sourced from http://stackoverflow.com/a/27058505
class DateTimeEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


# Sourced from http://stackoverflow.com/a/1526089
def get_date_modified(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)


# Partially sourced from http://stackoverflow.com/a/23064792
def get_date_photo_taken(filepath):
    img = Image.open(filepath)
    if not img:
        return None

    exif = img._getexif()
    if not exif:
        return None

    exif_str_val = exif[36867]

    exif_datetime_val = datetime.strptime(exif_str_val, '%Y:%m:%d %H:%M:%S')
    return exif_datetime_val


def get_full_filepaths_in_tree(root_dir_path):
    filepaths = []
    for (dirpath, dirnames, filenames) in os.walk(root_dir_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            filepaths.append(full_path)
    return filepaths


def get_numeric_part_from_string(text):
    found_numbers = re.findall(r'\d+', text)
    return (''.join(found_numbers))


def add_to_filename_without_extension(filepath, addition):
    filename_without_ext = os.path.splitext(filepath)[0]
    filename_ext = os.path.splitext(filepath)[1]

    dirpath = os.path.dirname(filepath)

    return os.path.join(dirpath, filename_without_ext +
                        addition + filename_ext)


def resize_fill_image(img, min_image_width, min_image_height, resample_mode):
    img_width = img.size[0]
    img_height = img.size[1]
    old_ratio = img_width / img_height
    new_ratio = min_image_width / min_image_height
    print('old_ratio=' + str(old_ratio) + ', new_ratio=' + str(new_ratio))

    if old_ratio <= new_ratio:
        new_image_width = min_image_width
        new_image_height = new_image_width / old_ratio
    else:
        new_image_height = min_image_height
        new_image_width = new_image_height * old_ratio

    new_image_size = (
        int(new_image_width),
        int(new_image_height)
    )

    return img.resize(size=new_image_size, resample=resample_mode)


# Partially sourced from http://stackoverflow.com/a/27784150
def canvas_resize_image(img, canvas_width, canvas_height):
    """Resize the canvas of old_image_path. Center the image on the new canvas.
    """

    old_width, old_height = img.size

    # Center the image
    x1 = int(math.floor((canvas_width - old_width) / 2))
    y1 = int(math.floor((canvas_height - old_height) / 2))

    mode = img.mode
    if len(mode) == 1:  # L, 1
        new_background = (255)
    if len(mode) == 3:  # RGB
        new_background = (255, 255, 255)
    if len(mode) == 4:  # RGBA, CMYK
        new_background = (255, 255, 255, 255)

    newImage = Image.new(mode, (canvas_width, canvas_height), new_background)
    newImage.paste(img, (x1, y1, x1 + old_width, y1 + old_height))

    return newImage


# Sourced from http://stackoverflow.com/a/7716358
def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
