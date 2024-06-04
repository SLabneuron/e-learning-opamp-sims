# -*- coding: utf-8 -*-

"""

Created on Tue May 28, 2024

@author: shirafujilab

Purpose
    load_image:
        - resize image
        - return image

"""


from PIL import Image

def load_image(image_path, base_width=300):

    # get image
    original_image = Image.open(image_path)

    # calculate ratios (wpercent, hsize)
    wpercent = (base_width / float(original_image.size[0]))
    hsize = int((float(original_image.size[1]) * float(wpercent)))

    # resize image
    image = original_image.resize((base_width, hsize), Image.ANTIALIAS)

    return image
