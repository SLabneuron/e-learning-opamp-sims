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
import numpy as np
from tkinter import ttk
from tkinter import filedialog

# import my library
from ..graphics.graphics import Graphics
from .control_frame import ControlFrame
from .output_console import OutputConsole
from ..sims.lpf import LPF
from ..sims.hpf import HPF
from ..sims.bpf import BPF
from .utils.save_files import save_files



class MainWindow:
    def __init__(self, root, params):

        """ Get and Init params """

        # Get root frame
        self.root = root

        # Get params (json)
        self.params = params

        # Dynamic Arrays for widgets, and results
        self.params["dynamic_params"] = {}
        self.params["dynamic_sim_params"] = {}
        self.params["results"] = {}

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
        self.output_console = OutputConsole(self)

        # Create Foot Note (3,0)
        self.foot_note()


    def button_config(self):

        # Enter
        self.root.bind("<Return>", self.button_enter)

        # Ctrl + s
        self.root.bind("<Control-s>", lambda event: save_files(self.params["paths"]["save_path"],self.root))


    def button_enter(self, event=None):

        """ Calculate and Output result (fig, console) """

        self.calculate()
        self.graphic_results.plots(self.params)
        self.output_console.update_log()


    def calculate(self):

        # Set_parameters
        freq_l = float(self.params["dynamic_sim_params"]["freq_l"].get())
        freq_r = float(self.params["dynamic_sim_params"]["freq_r"].get())
        freq = np.arange(freq_l, freq_r, 1)
        filter_type = self.params["dynamic_params"]["filter_type"].get()

        # Calculate with filter types
        if filter_type == "LPF": results_amp, results_phase = LPF.calculate_response_lpf(self.params, freq)
        elif filter_type == "HPF": results_amp, results_phase = HPF.calculate_response_hpf(self.params, freq)
        elif filter_type == "BPF": results_amp, results_phase = BPF.calculate_response_bpf(self.params, freq)

        # Save Results
        self.params["results"]["freq"] = freq
        self.params["results"]["amp"] = results_amp
        self.params["results"]["phase"] = results_phase


    def foot_note(self):

        """ Operation Manual"""

        tk.Label(self.root,text = " 'Enter': Calculation and Plot").grid(row=5, column=0, sticky= tk.E)
        tk.Label(self.root,text = " 'ctrl + s': Save").grid(row=6, column=0, sticky = tk.E)


    def root_config(self):

        # Set title
        self.root.title("Fileter Characteristic Checker")

        # Initial size of the main window
        self.root.geometry("800x600+100+100")

        # Minimum size of the main window
        self.root.minsize(800,600)