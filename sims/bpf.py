# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15, 2024

@author: shirafujilab

Puropose:
    This code calculate first order band-pass filter (BPF)
"""

import numpy as np

class BPF:
    def calculate_response_bpf(params, freq):

        # parameters
        for key in params:
            globals()[key] = params[key]

        # Calculate transfer function
        omega = 2*np.pi*freq
        frac1 = 1j * omega* R2 * C1
        frac2 = 1- omega**2 * R1 * R2 * C1* C2 + 1j * omega*(R1 * C1 + R2 * C2)
        transfer_function = -frac1/frac2
        
        # Calculate for amplitude response
        amplitude_response = np.abs(transfer_function)
        
        # Calculate for phase response
        phase_response = np.angle(transfer_function)
        
        return amplitude_response, phase_response