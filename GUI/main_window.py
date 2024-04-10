"""

Created on Thu Mar 14, 2024

@author: shriafujilab

Purpose:
    The code privide GUI config

"""

import os

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class MainWindow:
    def __init__(self, params, root, paths):
        """Initialize the main window"""
        self.params = params
        self.root = root
        self.paths = paths
        self.units ={}
        self.create_widgets()


    def create_widgets(self):
        """Create and layout the widgets in the main window."""
        self.root.title("Fileter Characteristic Checker")

        # Create control frame for parameter inputs and filter type selection
        self.create_control_frame()

        # Create plot frame for displaying filter response
        plot_frame = ttk.Frame(self.root, height=40, padding="3 3 12 12")
        plot_frame.grid(row=1, column=0, sticky="nsew")

        # Figure configure
        self.root.rowconfigure(0, weight=2)
        self.root.rowconfigure(1, weight=3)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=1)


    def create_control_frame(self):
        # Create control frame for parameter inputs and filter type selection
        self.control_frame = ttk.Frame(self.root, padding = "3 3 12 12")
        self.control_frame.grid(row=0, column=0, sticky="nsew")

        # conlumn setting
        column_config = [80, 20, 10, 40, 40]
        for index, num in enumerate(column_config):
            self.control_frame.columnconfigure(index, minsize = num)

        # Initialize a dictionary to hold parameter entries
        self.parameters = {}

        # Create filter select
        self.create_filter_type()

        # Create parameter select
        self.create_param_box()

        # Create schematic corresponding to filter select
        self.create_schematic()


    def create_filter_type(self):
        # Create radio buttons for selecting the filter type
        ttk.Label(self.control_frame, text="Select Filter Type").grid(column=0, row=0, sticky= tk.W)
        self.filter_type = tk.StringVar(value="LPF")
        for i, ftype in enumerate(["LPF", "HPF", "BPF"]):
            ttk.Radiobutton(self.control_frame,
                            text=ftype,
                            variable=self.filter_type,
                            value=ftype
                            ).grid(column=0, row=i+1, sticky=tk.W)


    def create_param_box(self):
        # Create labels and entries for filter parameters(value)
        ttk.Label(self.control_frame, text="Param.").grid(column=2, row=0, sticky = tk.W)
        for i, param in enumerate(["R1", "R2", "C1", "C2"]):
            ttk.Label(self.control_frame, text=param).grid(column=2, row=1+i, sticky=tk.E)

            entry = ttk.Entry(self.control_frame, width=8)
            entry.grid(column = 3, row=1+i, sticky=tk.W+tk.E)
            entry.insert(0, str(self.params[param]["value"])) # default
            self.parameters[param] = entry

            unit_options = ["kohm", "ohm"] if "R" in param else ["uF", "F", "nF", "pF"]
            combo = ttk.Combobox(self.control_frame, values=unit_options, width=5)
            combo.grid(column = 4, row=1+i)
            combo.set(self.params[param]["unit"])  #default
            self.units[param] = combo



    def get_parameter_values(self):
        """Calculate entry and combo values"""
        for param, entry in self.parameters.items():
            base_value = float(entry.get())
            unit = self.units[param].get()

            # Comvert according to units
            factor = {"ohm":1, "kohm": 1e3, "Mohm":1e6,
                      "F":1, "uF":1e-6, "nF":1e-9, "pF":1e-12}.get(unit, 1)
            self.params[param] = base_value * factor

        return self.params


    def create_schematic(self):

        # Create a schematic for easy understanding
        self.schematic_frame = ttk.Frame(self.root)
        self.schematic_frame.grid(row=0, column=1, sticky="nw")

        # Select graphics for filter_type
        filter_type = self.filter_type.get()
        if filter_type == "LPF":
            image_path = self.paths["lpf_path"]
        elif filter_type == "HPF":
            image_path = self.paths["hpf_path"]
        elif filter_type == "BPF":
            image_path = self.paths["bpf_path"]
        else:
            print("Unknown filter type.")
            return

        # Import and resize image
        original_image = Image.open(image_path)
        base_width = 300
        wpercent = (base_width/float(original_image.size[0]))
        hsize = int((float(original_image.size[1]) * float(wpercent)))
        image = original_image.resize((base_width, hsize), Image.ANTIALIAS)

        self.photo = ImageTk.PhotoImage(image)

        label = tk.Label(self.schematic_frame, image = self.photo)
        self.image=self.photo
        label.pack()



def main():
    """For debag, Create the TK root"""
    root = tk.Tk()
    root.geometry("800x600") # set initial size of the main window
    root.minsize(800, 600)   # Set minimum size of the main window
    MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()