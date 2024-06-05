# -*- coding: utf-8 -*-

"""

Created on Thu Mar 14, 2024

@author: shirafujilab

Purpose:
    save_files:
        - save

"""

# Import standard library
import os
import tkinter as tk
from PIL import ImageGrab
import time


def save_files(path, root):

    # Get axis info
    geom = root.geometry().split('+')
    size = geom[0].split('x')
    x, y = int(geom[1]), int(geom[2])
    width, height = int(size[0]), int(size[1])


    # Get Image
    img = ImageGrab.grab()

    # Save screenshot
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    save_path = os.path.join(path, f"screenshot_{timestamp}.jpg")
    img.save(save_path, "JPEG")