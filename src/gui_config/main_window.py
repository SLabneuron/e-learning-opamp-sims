# -*- coding: utf-8 -*-

"""

Created on Thu Mar 14, 2024

@author: shriafujilab

Purpose:
    MainWindow:
        -

"""

# import standard library
import tkinter as tk
from tkinter import ttk

# import my library
from ..graphics.graphics import Graphics
from ..gui_config.contorol_frame import ControlFrame


class MainWindow:
    def __init__(self, root, params):

        """ Get and Init params """

        # Get root frame
        self.root = root

        # Get params (json)
        self.params = params

        """ Set widgets """

        self.create_widgets()

        self.button_config()


    def create_widgets(self):

        """Create and layout the widgets in the main window."""

        # Init root window
        self.root_config()

        # Create control frame (0,0)
        self.control_frame = ControlFrame(self)

        # Create plot frame (1,0)
        self.graphic_results = Graphics(self)

        # Create output console (2,0)
        self.create_output_console()


    def create_output_console(self):

        # Create output console frame
        self.console_widget = ttk.Frame(self.root, padding = "3 3 12 12")
        self.console_widget.grid(row = 4, column = 0, columnspan = 4)

        # Create output console
        self.output_console = tk.Text(self.console_widget, height=2, state=tk.DISABLED)
        self.output_console.grid(row=0, column=0)


    def button_config(self):

        self.root.bind("<Return>", self.button_enter)


    def button_enter(self, event=None):
        self.graphic_results.calculate_and_plot(self.params)


    def root_config(self):

        # Set title
        self.root.title("Fileter Characteristic Checker")

        # Initial size of the main window
        self.root.geometry("800x600")

        # Minimum size of the main window
        self.root.minsize(800,600)