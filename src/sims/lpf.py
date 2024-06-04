# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15, 2024

@author: shirafujilab

Puropose:
    This code calculate first order low-pass filter (LPF)
"""

# import standard library
import numpy as np

# import my library
from ..gui_config.utils.param_recal import recalculate


class LPF:
    def calculate_response_lpf(params, freq):

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
        frac1 = R2
        frac2 = R1 + 1j*omega*(R1*R2*C2)
        transfer_function = -frac1/frac2

        # Calculate for amplitude response
        amplitude_response = np.abs(transfer_function)

        # Calculate for phase response
        phase_response = np.angle(transfer_function)*180/np.pi

        max_gain = np.max(amplitude_response)
        cutoff_gain = max_gain*np.sqrt(1/2)
        cutoff_freq_index = np.argmin(np.abs(amplitude_response - cutoff_gain))
        cutoff_freq = freq[cutoff_freq_index]

        return amplitude_response, phase_response, cutoff_freq
