#!/usr/bin/env python
"""
Simulation of harmonic radar
"""
import numpy as np
from scipy.signal import welch
from matplotlib.pyplot import figure,show
#%% user parameters
fc = 917e6 #[Hz]
bm = 1e6 #[Hz]
tm = 1e-3 #[sec]
fs = 6e9 #[Hz]
range_m = 100
Atarg=1
nlfm=0
#%% simulation
t = np.arange(0,tm,1/fs)

x = np.cos(2*np.pi*fc*t)
#%% ideal diode--perfect one-way current flow
x[x<0] = 0. 

#%% plots

if 0:
    ax=figure().gca()
    ax.plot(t,x)
    ax.set_xlabel('time [sec.]')

f,Pxx = welch(x,fs,nperseg=1000000)

ax = figure().gca()
ax.plot(f,20*np.log10(Pxx))
ax.set_xlabel('frequency [Hz]')
ax.set_ylabel('amplitude [dB]')
ax.set_ylim(-130,-100)

