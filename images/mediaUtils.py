# This Python 3 module contains utility functions for identifying and
# manipulating media files.

import os
from PIL import Image, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


def is_image_file(filename):
    return (filename.lower().endswith('.jpg') or
            filename.lower().endswith('.jpeg') or
            filename.lower().endswith('.png'))

def is_media_file(filename):
    return is_image_file(filename) or \
            filename.lower().endswith('.mov') or \
            filename.lower().endswith('.mp4') or \
            filename.lower().endswith('.avi')

def get_dimensions(filename):
    with open(filename, 'rb') as f:
        with Image.open(f) as image:
            width = image.size[0]
            height = image.size[1]
            return (width, height)

def resize_dimensions(filename, width, height):
    """Resize image to a certain width and height"""
    if width < 1 or height < 1:
        print("Width and height must be greater than 0.")
        exit(1)
    with open(filename, 'rb') as f:
        with Image.open(f) as image:
            new = resizeimage.resize_contain(image, [width, height])
            new = new.convert('RGB')
            new.save(filename, image.format)
            print(filename + ' resized to ' +
                    str(width) + ' x ' + str(height))

def resize_percent(filename, pct):
    """Resize image to a certain relative percentage"""
    if pct < 1 or pct > 500:
        print("Percent must be between 1 and 500.")
        exit(1)
    pct *= 0.01

    with open(filename, 'rb') as f:
        with Image.open(f) as image:
            width_orig = image.size[0]
            height_orig = image.size[1]
    resize_dimensions(filename, int(width_orig * pct), int(height_orig * pct))
