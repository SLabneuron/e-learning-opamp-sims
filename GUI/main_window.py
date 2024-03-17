"""

Created on Thu Mar 14, 2024

@author: shriafujilab

Purpose:
    The code privide GUI config

"""

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class MainWindow:
    def __init__(self, params, root):
        """Initialize the main window"""
        self.params = params
        self.root = root
        self.units ={}
        self.create_widgets()


    def create_widgets(self):
        """Create and layout the widgets in the main window."""
        self.root.title("fileter Characteristic Checker")

        # Create control frame for parameter inputs and filter type selection
        self.control_frame = ttk.Frame(self.root, padding = "3 3 12 12")
        self.control_frame.grid(row=0, column=0, sticky="nsew")

        # Create plot frame for displaying filter response
        plot_frame = ttk.Frame(self.root, padding="3 3 12 12")
        plot_frame.grid(row=0, column=1, sticky="nsew")

        # Initialize a dictionary to hold parameter entries
        self.parameters = {}
        # Create labels and entries for filter parameters(value)
        for i, param in enumerate(["R1", "R2", "C1", "C2"]):
            ttk.Label(self.control_frame, text=param).grid(column=0, row=i, sticky=tk.W)

            entry = ttk.Entry(self.control_frame, width=7)
            entry.grid(column=1,  row=i, sticky=(tk.W, tk.E))
            entry.insert(0, str(self.params[param]["value"]))
            self.parameters[param] = entry

            unit_options = ["kohm", "ohm"] if "R" in param else ["uF", "F", "nF", "pF"]
            combo = ttk.Combobox(self.control_frame, values=unit_options, width=5)
            combo.grid(column=2, row=i, sticky=tk.W)
            combo.set(self.params[param]["unit"])  #default
            self.units[param] = combo

        # Create radio buttons for selecting the filter type
        self.filter_type = tk.StringVar(value="LPF")
        for i, ftype in enumerate(["LPF", "HPF", "BPF"]):
            ttk.Radiobutton(self.control_frame,
                            text=ftype,
                            variable=self.filter_type,
                            value=ftype
                            ).grid(column=3, row=i, sticky=tk.W)

        # Configure window resizing behavior
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)


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


def main():
    """For debag, Create the TK root"""
    root = tk.Tk()
    root.geometry("800x600") # set initial size of the main window
    root.minsize(800, 600)   # Set minimum size of the main window
    MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()