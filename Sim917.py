#!/usr/bin/env pythone
"""
Simulation of harmonic radar
"""
from numpy import arange,exp,pi,cos,log10
from matplotlib.pyplot import figure,show
#
from tincanradar.estimation import psd

fc = 917e6 #[Hz]
bm = 1e6 #[Hz]
tm = 1e-3 #[sec]
fs = 6e9 #[Hz]
range_m = 100
Atarg=1
nlfm=0

t = arange(0,tm,1/fs)

x = cos(2*pi*fc*t)
x[x<0] = 0.

Pxx,fax = psd(x,fs)

#ax=figure(1).gca()
#ax.plot(t,x)
#ax.set_xlabel('time [sec.]')

ax = figure(2).gca()
ax.plot(fax,20*log10(Pxx))
ax.set_xlabel('frequency [Hz]')
ax.set_ylabel('amplitude [dB]')
ax.set_ylim(-130,-100)
show()