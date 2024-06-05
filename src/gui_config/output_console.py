# -*- coding: utf-8 -*-

"""

Created on Thu Mar 14, 2024

@author: shirafujilab

Purpose:
    Output Console:
        - BandWidth
        - (Peak Freq)

"""

# Import standard library
import tkinter as tk
from tkinter import ttk
import numpy as np


class OutputConsole:

    def __init__(self, main_window):

        """ Initialize parameters """

        # Get Parent Class
        self.main_window = main_window

        # Set Frame
        self.create_output_console()
        self.update_log()


    def create_output_console(self):
        # Create control frame for parameter inputs and filter type selection
        self.output_console_frame = ttk.Frame(self.main_window.root, padding = "3 3 12 12")
        self.output_console_frame.grid(row=4, column=0, columnspan=4)

        # Create output console
        self.output_console = tk.Text(self.output_console_frame, height=2, state=tk.DISABLED)
        self.output_console.grid(row=0, column=0,sticky="nsew")


    def update_log(self):

        # Set values
        filter_type = self.main_window.params["dynamic_params"]["filter_type"].get()
        self.freq_result = self.main_window.params["results"]["freq"]
        self.amp_result = self.main_window.params["results"]["amp"]
        self.phase_result = self.main_window.params["results"]["phase"]

        # Output logs every filter
        if (filter_type == "LPF") or (filter_type == "HPF"):

            # Get results
            self.results_lpf_and_hpf()

            # Outputs
            console_text1 = f"          Filter type : {filter_type}"
            console_text2 = f"-3dB cutoff frequency : {self.cutoff_freq}Hz "

        elif filter_type == "BPF":

            # Get results
            self.results_bpf()

            # Outputs
            console_text1 = f"          Filter type : {filter_type}"
            console_text2 = f"    Bandwidth at -3dB : {self.lower_cutoff_freq}Hz ~ {self.upper_cutoff_freq}Hz"

        self.output_console.config(state=tk.NORMAL) # Enable to edit text widget
        self.output_console.delete("1.0", tk.END)
        self.output_console.insert(tk.END, console_text1 + "\n" + console_text2)
        self.output_console.config(state=tk.DISABLED) # Unable to edit text widget


    def results_lpf_and_hpf(self):

        # Calculate cutoff frequency

        max_gain = np.max(self.amp_result)
        cutoff_gain = max_gain*np.sqrt(1/2)
        cutoff_freq_index = np.argmin(np.abs(self.amp_result - cutoff_gain))
        self.cutoff_freq = int(self.freq_result[cutoff_freq_index])  # Output


    def results_bpf(self):

        # Calculation Cutoff Frequency

        max_gain = np.max(self.amp_result)
        cutoff_gain = max_gain*np.sqrt(1/2)
        max_gain_index = np.argmax(self.amp_result)


        for i in range(max_gain_index, 0, -1):
            if self.amp_result[i] < cutoff_gain:
                self.lower_cutoff_freq = int(self.freq_result[i+1])
                break
            else:
                self.lower_cutoff_freq = None

        for i in range(max_gain_index, len(self.freq_result), 1):
            if self.amp_result[i] <cutoff_gain:
                self.upper_cutoff_freq = int(self.freq_result[i-1])
                break
            else:
                self.upper_cutoff_freq = None