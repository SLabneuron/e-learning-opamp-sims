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
import os
import json
import tkinter as tk

# import my library
from src.gui_config.main_window import MainWindow  # Main GUI window configuration


class Simulator:

    def __init__(self, init_params):

        """ Initialize parameters """

        # init parameter
        self.params = init_params

        # Get Image Path
        self.get_path()

        # Set GUI
        self.set_gui()


    def run(self):

        """ GUI Loop """

        self.root.mainloop()



    def set_gui(self):

        """ Set GUI """

        # Init tkinter
        self.root = tk.Tk()

        # Set widgets
        MainWindow(self.root, self.params)


    def get_path(self):

        """ Get Path  """

        # get current directory
        cur_dir = os.path.dirname(os.path.abspath(__file__))

        # get paths
        lpf_path = os.path.join(cur_dir, "data", "image", "lpf.jpg")
        hpf_path = os.path.join(cur_dir, "data", "image", "hpf.jpg")
        bpf_path = os.path.join(cur_dir, "data", "image", "bpf.jpg")

        # set path
        self.paths = {
            "LPF_path" : os.path.abspath(lpf_path),
            "HPF_path" : os.path.abspath(hpf_path),
            "BPF_path" : os.path.abspath(bpf_path),
        }

        self.params["paths"] = self.paths


if __name__ == "__main__":

    # Get current path
    cur_dir = os.path.dirname(os.path.abspath(__file__))

    # Get param path
    params_path = os.path.join("data", "params.json")

    # Set init params
    with open(params_path, "r") as j:
        params = json.load(j)

    # Create an Instance of ControlPanel
    control_panel = Simulator(params)

    # Execute Simulator
    control_panel.run()