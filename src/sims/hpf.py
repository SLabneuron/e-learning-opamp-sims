# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15, 2024

@author: shirafujilab

Puropose:
    This code calculate first order high-pass filter (HPF)
"""

# import standard library
import numpy as np

# import my library
from ..gui_config.utils.param_recal import recalculate

class HPF:
    def calculate_response_hpf(params, freq):

        """ Init """

        # Elements
        elements = ["R1", "R2", "C1", "C2"]

        # Recalculate parameters
        dicts = recalculate(params, elements)

        # Declare recalculate parameters
        for key in dicts: globals()[key] = dicts[key]

        """ Calculation """

        # Calculate transfer function
        omega = 2*np.pi*freq
        frac1 = 1j * omega * R2 * C1
        frac2 = 1 + 1j  * omega * R1 * C1
        transfer_function = -frac1/frac2

        # Calculate for amplitude response
        amplitude_response = np.abs(transfer_function)

        # Calculate for phase response
        phase_response = np.angle(transfer_function)*180/np.pi

        return amplitude_response, phase_response