"""

Created on Thu Mar 14, 2024

@author: shriafujilab

Purpose:
    The code privide GUI config

"""

# import standard library
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# import my library
from ..graphics.graphics import Graphics



class MainWindow:
    def __init__(self, root, params):

        """ Get and Init params """

        # Get root frame
        self.root = root

        # Get params (json)
        self.params = params

        # Set paths
        self.paths = self.params["paths"]

        # For simulation, parameters of circuit elements
        self.elements_params = {}

        self.values = {}    # For value part
        self.units = {}     # For unit part (kohm, uF, etc.)

        """ Set widgets """

        self.create_widgets()


    def create_widgets(self):

        """Create and layout the widgets in the main window."""

        # Init root window
        self.root_config()

        # Create control frame for parameter inputs and filter type selection
        self.create_control_frame()

        # Create plot frame for displaying filter response
        self.graphic_results = Graphics(self.root, self.params, self)

        # Create output console
        self.create_output_console()

    def root_config(self):

        # Set title
        self.root.title("Fileter Characteristic Checker")

        # Initial size of the main window
        self.root.geometry("800x600")

        # Minimum size of the main window
        self.root.minsize(800,600)


    def create_control_frame(self):
        # Create control frame for parameter inputs and filter type selection
        self.control_frame = ttk.Frame(self.root, padding = "3 3 12 12")
        self.control_frame.grid(row=0, column=0, sticky="nsew")

        # conlumn setting
        column_config = [20, 20, 40]
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

        """ Create radio buttons for selecting the filter type """

        # Set Title
        self.radio_button_title = ttk.Frame(self.control_frame, padding = "3 3 12 12")
        self.radio_button_title.grid(row=0, column=0, sticky="nsew")
        ttk.Label(self.radio_button_title, text="Select Filter Type").grid(column=0, row=0, sticky= tk.W)

        # Set radio button widgets (Frame)
        self.radio_button_widgets = ttk.Frame(self.control_frame, padding = "3 3 12 12")
        self.radio_button_widgets.grid(row=1, column = 0, sticky="nsew")

        # Set init
        self.filter_type = tk.StringVar(value="LPF")

        # Wrapper
        def wrapper(event = None):
            self.param_change()
            self.create_schematic()

        # Set radio button widgets
        for i, ftype in enumerate(["LPF", "HPF", "BPF"]):
            radiobutton = ttk.Radiobutton(self.radio_button_widgets,
                            text=ftype,
                            variable=self.filter_type,
                            value=ftype)
            radiobutton.grid(column=0, row=i+1, sticky=tk.W)
            radiobutton.bind("<Return>", wrapper)


    def param_change(self, event=None):
            self.graphic_results.calculate_and_plot()


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
            entry.insert(0, str(self.params["params_elements"][param])) # default
            entry.bind("<Return>", self.param_change)
            self.values[param] = entry

            unit_options = ["kohm", "ohm"] if "R" in param else ["uF", "F", "nF", "pF"]
            combo = ttk.Combobox(self.param_box_widgets, values=unit_options, width=5)
            combo.grid(column = 2, row=i)
            combo.set(self.params["params_elements"][param + "_scale"])  #default
            combo.bind("<Return>", self.param_change)
            self.units[param] = combo


    def create_schematic(self):

        # Create a schematic for easy understanding
        self.schematic_frame = ttk.Frame(self.root)
        self.schematic_frame.grid(row=0, column=3, sticky="nw")

        # Select graphics for filter_type
        filter_type = self.filter_type.get()
        if filter_type == "LPF":
            image_path = self.paths["lpf_path"]
        elif filter_type == "HPF":
            image_path = self.paths["hpf_path"]
        elif filter_type == "BPF":
            image_path = self.paths["bpf_path"]

        # Import and resize image
        original_image = Image.open(image_path)
        base_width = 300
        wpercent = (base_width/float(original_image.size[0]))
        hsize = int((float(original_image.size[1]) * float(wpercent)))
        image = original_image.resize((base_width, hsize), Image.ANTIALIAS)

        self.photo = ImageTk.PhotoImage(image)

        label = tk.Label(self.schematic_frame, image = self.photo)
        label.pack()



    def create_output_console(self):

        # Create output console frame
        self.console_widget = ttk.Frame(self.root, padding = "3 3 12 12")
        self.console_widget.grid(row = 4, column = 0, columnspan = 4)

        # Create output console
        self.output_console = tk.Text(self.console_widget, height=2, state=tk.DISABLED)
        self.output_console.grid(row=0, column=0)


    def get_parameter_values(self):
        """Calculate entry and combo values"""
        for param, entry in self.values.items():
            base_value = float(entry.get())
            unit = self.units[param].get()

            # Comvert according to units
            factor = {"ohm":1, "kohm": 1e3, "Mohm":1e6,
                      "F":1, "uF":1e-6, "nF":1e-9, "pF":1e-12}.get(unit, 1)
            self.params[param] = base_value * factor

        return self.params


