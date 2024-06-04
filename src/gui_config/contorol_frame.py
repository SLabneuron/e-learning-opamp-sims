# -*- coding: utf-8 -*-

"""

Created on Thu Mar 14, 2024

@author: shirafujilab

Purpose:
    ControlPanel:
        - Root directory
        - Get init parameters
        - Mainloop

"""

# Import standard library
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from ..graphics.graphics import Graphics
from ..gui_config.utils.image_utils import load_image

class ControlFrame:

    def __init__(self, main_window):

        """ Initialize parameters """

        # Get Parent Class
        self.main_window = main_window

        # Uniform
        self.main_window.params["dynamic_params"] = {}
        self.main_window.params["dynamic_sim_params"] = {}

        # Set Frame
        self.create_control_frame()


    def create_control_frame(self):
        # Create control frame for parameter inputs and filter type selection
        self.control_frame = ttk.Frame(self.main_window.root, padding = "3 3 12 12")
        self.control_frame.grid(row=0, column=0, sticky="nsew")

        # Create filter select
        self.create_filter_type()

        # Create parameter select
        self.create_param_box()

        # Create simulation config
        self.create_sim_box()

        # Create schematic corresponding to filter select
        self.create_schematic()


    def create_filter_type(self):

        """ Create radio buttons for selecting the filter type """

        # Set Title
        self.radio_button_title = ttk.Frame(self.control_frame, padding = "3 3 12 12")
        self.radio_button_title.grid(row=0, column=0, sticky="nsew")
        ttk.Label(self.radio_button_title, text="Select Filter Type").grid(column=0, row=0, sticky= tk.W)

        # Set radio button widgets (Frame)
        self.radio_button_widgets = ttk.Frame(self.control_frame, padding = "3 3 12 12")
        self.radio_button_widgets.grid(row=1, column = 0, sticky="nsew")

        # Set init
        self.main_window.params["dynamic_params"]["filter_type"] = tk.StringVar(value="LPF")

        # Set radio button widgets
        for i, ftype in enumerate(["LPF", "HPF", "BPF"]):
            radiobutton = ttk.Radiobutton(self.radio_button_widgets,
                            text=ftype,
                            variable=self.main_window.params["dynamic_params"]["filter_type"],
                            value=ftype)
            radiobutton.grid(column=0, row=i+1, sticky=tk.W)
            radiobutton.bind("<Return>", self.create_schematic)


    def create_schematic(self, event = None):

        # Create a schematic for easy understanding
        self.schematic_frame = ttk.Frame(self.main_window.root)
        self.schematic_frame.grid(row=0, column=3, sticky="nw")

        # Select graphics for filter_type
        filter_type = self.main_window.params["dynamic_params"]["filter_type"].get()

        # Get path
        image_path = self.main_window.params["paths"][filter_type + "_path"]

        # Get Clipping Image
        self.image = ImageTk.PhotoImage(load_image(image_path))

        label = tk.Label(self.schematic_frame, image = self.image)
        label.pack()


    def create_param_box(self):

        """ Create labels and entries for filter parameters(value) """

        # Set Title
        self.param_box_title = ttk.Frame(self.control_frame, padding = "3 3 12 12")
        self.param_box_title.grid(row=0, column=1, sticky="nsew")
        ttk.Label(self.param_box_title, text="Parameters").grid(column=0, row=0, sticky = tk.W)

        # Set param box widgets (Frame)
        self.param_box_widgets = ttk.Frame(self.control_frame, padding = "3 3 12 12")
        self.param_box_widgets.grid(row=1, column = 1, sticky="nsew")

        # Set param box widgets
        for i, param in enumerate(["R1", "R2", "C1", "C2"]):
            ttk.Label(self.param_box_widgets, text=param).grid(column=0, row=i, sticky=tk.E)

            entry = ttk.Entry(self.param_box_widgets, width=8)
            entry.grid(column = 1, row=i, sticky=tk.W+tk.E)
            entry.insert(0, str(self.main_window.params["params_elements"][param])) # default
            self.main_window.params["dynamic_params"][param] = entry

            unit_options = ["kohm", "ohm"] if "R" in param else ["uF", "F", "nF", "pF"]
            combo = ttk.Combobox(self.param_box_widgets, values=unit_options, width=5)
            combo.grid(column = 2, row=i)
            combo.set(self.main_window.params["params_elements"][param + "_scale"])  #default
            self.main_window.params["dynamic_params"][param + "_scale"] = combo


    def create_sim_box(self):

        """ Create labels and entries for filter parameters(value) """

        # Set Title
        self.sim_box_title = ttk.Frame(self.control_frame, padding = "3 3 12 12")
        self.sim_box_title.grid(row=0, column=2, sticky="nsew")
        ttk.Label(self.sim_box_title, text="Parameters2").grid(column=0, row=0, sticky = tk.W)

        # Set param box widgets (Frame)
        self.sim_box_widgets = ttk.Frame(self.control_frame, padding = "3 3 12 12")
        self.sim_box_widgets.grid(row=1, column = 2, sticky="nsew")

        # Set param box widgets
        for i, param in enumerate(["freq_l", "freq_r", "haxis", "vaxis"]):
            ttk.Label(self.sim_box_widgets, text=param).grid(column=0, row=i, sticky=tk.E)

            entry = ttk.Entry(self.sim_box_widgets, width=8)
            entry.grid(column = 1, row=i, sticky=tk.W+tk.E)
            entry.insert(0, str(self.main_window.params["sim_params"][param])) # default
            self.main_window.params["dynamic_sim_params"][param] = entry