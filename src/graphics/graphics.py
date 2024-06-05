# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18, 2024

@author: shirafujilab

"""

# import standard library
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MultipleLocator
import matplotlib.gridspec as gridspec

# import my library
from ..sims.lpf import LPF
from ..sims.hpf import HPF
from ..sims.bpf import BPF

class Graphics:
    def __init__(self, main_window):

        # Get main_window
        self.main_window = main_window

        # Set Figure
        self.set_figure()

        # Init Plot
        self.calculate_and_plot(self.main_window.params)


    def set_figure(self):

        self.fig = Figure(figsize=(8, 3), dpi = 100)
        self.gs = gridspec.GridSpec(2, 3, height_ratios= [5,1], width_ratios= [6,1,6], figure = self.fig)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_window.root)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan =4, pady=5, sticky="nsew")
        self.canvas.mpl_connect("key_press_event", self.main_window.button_enter)
        self.ax1 = self.fig.add_subplot(self.gs[0, 0])
        self.ax2 = self.fig.add_subplot(self.gs[0, 2])
        self.canvas.draw()


    def calculate_and_plot(self, params):

        # Set Parameters
        freq_l = float(params["dynamic_sim_params"]["freq_l"].get())
        freq_r = float(params["dynamic_sim_params"]["freq_r"].get())
        filter_type = params["dynamic_params"]["filter_type"].get()

        # Make freq
        freq = np.arange(freq_l, freq_r, 1)

        # Calling adequately functions
        if filter_type == "LPF": self.results_amp, self.results_freq, cutoff_freq = LPF.calculate_response_lpf(params, freq)
        elif filter_type == "HPF": self.results_amp, self.results_freq, cutoff_freq = HPF.calculate_response_hpf(params, freq)
        elif filter_type == "BPF": self.results_amp, self.results_freq, lower_cutoff_freq, upper_cutoff_freq  = BPF.calculate_response_bpf(params, freq)

        # self.set_figure()
        self.plot_results_amp(params, freq, self.results_amp)
        self.plot_results_phase(params, freq, self.results_freq)

        # Output logs every filter
        if (filter_type == "LPF") or (filter_type == "HPF"):
            console_text1 = f"          Filter type : {filter_type}"
            console_text2 = f"-3dB cutoff frequency : {cutoff_freq}Hz "
        elif filter_type == "BPF":
            console_text1 = f"          Filter type : {filter_type}"
            console_text2 = f"    Bandwidth at -3dB : {lower_cutoff_freq}Hz ~ {upper_cutoff_freq}Hz"

        #self.output_console.config(state=tk.NORMAL) # Enable to edit text widget
        #self.output_console.delete("1.0", tk.END)
        #self.output_console.insert(tk.END, console_text1 + "\n" + console_text2)
        #self.output_console.config(state=tk.DISABLED) # Unable to edit text widget


    def plot_results_amp(self, params, freq, amp_response):

        # Set Parameters
        haxis = params["dynamic_sim_params"]["haxis"].get()
        vaxis = params["dynamic_sim_params"]["vaxis"].get()
        amp_l = float(params["dynamic_sim_params"]["amp_l"].get())
        amp_h = float(params["dynamic_sim_params"]["amp_h"].get())

        # Transform to "dB"
        if vaxis == "log": amp_response = 20*np.log10(amp_response)

        # clear and plot
        self.ax1.clear()
        self.ax1.plot(freq, amp_response, linewidth = 3)

        # Get horizontal scale
        if haxis == "log": self.ax1.set_xscale("log")
        else: self.ax1.set_xscale("linear")

        # Config of horizontal axis
        self.ax1.set_xlabel("Frequency [Hz]")
        self.ax1.set_xlim(freq[0], freq[-1])

        # Config of vertical axis
        if vaxis == "log":
            self.ax1.set_ylabel("Gain [dB]")
            self.ax1.yaxis.set_major_locator(MultipleLocator(3))
        else:
            self.ax1.set_ylabel("|Vout/Vin|")

        self.ax1.set_ylim(amp_l, amp_h)

        self.ax1.set_title("Amplitude Response")
        self.ax1.grid(color="black", linewidth = 0.2, which="minor", axis="both")
        self.ax1.grid(color="black", linewidth = 0.8, which="major", axis="both")
        self.canvas.draw()


    def plot_results_phase(self, params, freq, ph_response):

        # Set Parameters
        haxis = params["dynamic_sim_params"]["haxis"].get()
        vaxis = params["dynamic_sim_params"]["vaxis"].get()
        filter_type = params["dynamic_params"]["filter_type"].get()

        # clear  and plot
        self.ax2.clear()
        self.ax2.plot(freq, ph_response, "o", markersize = 2)

        # Get horizontal scale
        if haxis == "log": self.ax2.set_xscale("log")
        else: self.ax2.set_xscale("linear")

        # General Config
        self.ax2.set_xlabel("Frequency [Hz]")
        self.ax2.set_xlim(freq[0], freq[-1])
        self.ax2.set_ylabel("Phase [degrees]")
        self.ax2.yaxis.set_major_locator(MultipleLocator(90))
        self.ax2.yaxis.set_minor_locator(MultipleLocator(30))


        if params["dynamic_params"]["filter_type"].get() == "LPF": self.ax2.set_ylim(90, 180)
        elif params["dynamic_params"]["filter_type"].get() == "HPF": self.ax2.set_ylim(-180, -90)
        else: self.ax2.set_ylim(-180,  180)

        self.ax2.set_title("Phase Response")
        self.ax2.grid(color="black", linewidth = 0.2, which="minor", axis="both")
        self.ax2.grid(color="black", linewidth = 0.8, which="major", axis="both")
        self.canvas.draw()

