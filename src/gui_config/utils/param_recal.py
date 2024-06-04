# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15, 2024

@author: shirafujilab

Puropose:
    This code calculate first order low-pass filter (LPF)
"""



def recalculate(params, keys):

    # Init return dicts
    dicts = {}

    for key in keys:

        base_value = float(params["dynamic_params"][key].get())
        scale = params["dynamic_params"][key + "_scale"].get()

        factor = {"ohm":1, "kohm": 1e3, "Mohm":1e6,
                    "F":1, "uF":1e-6, "nF":1e-9, "pF":1e-12}.get(scale, 1)

        dicts[key] = base_value * factor

    return dicts