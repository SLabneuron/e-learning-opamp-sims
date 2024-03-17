# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 10:09:39 2023

@author: shirafujilab
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


class Graphics:
    def __init__(self, filter_mode, ):

        # graphic spaces
        self.fig = plt.figure(figsize=(6, 4))
        
        


        self.R1 = R1
        self.R2 = R2
        self.C1 = C1
        self.C2 = C2
    



    
    def main(self):
        # プロットする周波数範囲を設定 (ここでは0Hzから5000Hzまでを例とします)
        frequencies = np.linspace(1, 5000, 5000)

        # 各周波数における周波数特性を計算
        amp, phase = self.bpf(frequencies)
        
        # 利得をプロット
        plt.figure(figsize=(10,12))
        gs=gridspec.GridSpec(2,1)
        
        plt.subplot(gs[0,0])
        plt.plot(frequencies, amp)
        plt.xlabel('Amplitude')
        plt.ylabel('phase')
        plt.title('Amplitude Response of the Bandpass Filter')
        plt.grid(True)
        
        plt.subplot(gs[1,0])
        plt.plot(frequencies, np.rad2deg(phase))
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('phase')
        plt.title('Frequency Response of the Bandpass Filter')
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    R1 = 50*1000
    R2 = 10*1000
    C1 = 100*10**(-9)
    C2 = 10*10**(-9)
    
    instance = GainToFrequency(R1, R2, C1, C2)
    instance.main()