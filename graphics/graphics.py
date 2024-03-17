# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18, 2024

@author: shirafujilab
"""

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.gridspec as gridspec


class Graphics:
    def __init__(self, master):
        """
        Initialize Graphics
        master: widget of Tkinter
        """

        self.master = master
        self.initialize_figure()


    def initialize_figure(self):
        self.fig = Figure(figsize=(10, 8), dpi = 100)
        self.gs = gridspec.GridSpec(2, 1, figure = self.fig)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew")
        self.ax1 = self.fig.add_subplot(self.gs[0, 0])
        self.ax2 = self.fig.add_subplot(self.gs[1, 0])
        self.canvas.draw()


    def plot_results_amp(self, config, freq, amp_response):

        """
        Graphic amplotude characteristics
        config = {
            "scale": "normal" or "log",
            "freq_mode": "normal" or "log",
            "amp_mode": "normal" or "dB",
        }
        freq: numpy array
        amp_resoponse: numpy array
        """


        self.ax1.clear()
        if config["scale"] == "dB":
            amp_response = 20*np.log10(amp_response)
            
        self.ax1.plot(freq, amp_response)
        # Set horizontal scale
        if config["freq_mode"] == "normal":
            pass
        elif config["freq_mode"] == "log":
            self.ax1.set_xscale(config["freq_mode"])

        # Set vertical scale
        if config["scale"] == "normal":
            pass
        elif config["scale"] == "dB":
            pass
            #self.ax1.set_yscale("log")

        # Name each labels
        self.ax1.set_xlabel("Frequency (Hz)")
        if config["scale"] == "normal":
            self.ax1.set_ylabel("Amplitude")
        elif config["scale"] == "dB":
            self.ax1.set_ylabel("Amplitude (dB)")

        self.ax1.set_title("Amplitude Response")
        self.canvas.draw()


    def plot_results_phase(self, config, freq, ph_response):

        """
        Graphic amplotude characteristics
        config: same as results_amp
        freq: numpy array
        amp_resoponse: numpy array
        """

        self.ax2.clear()
        self.ax2.plot(freq, ph_response)

        # Set horizontal scale (for fitting results_amp)
        if config["freq_mode"] == "normal":
            pass
        elif config["freq_mode"] == "log":
            self.ax2.set_xscale(config["freq_mode"])

        # Name each labels
        self.ax2.set_xlabel("Frequency (Hz)")
        self.ax2.set_ylabel("Phase (degrees)")

        self.ax2.set_title("Phase Response")
        self.canvas.draw()