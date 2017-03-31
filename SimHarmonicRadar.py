#!/usr/bin/env python
import numpy as np
import scipy.signal as signal
from matplotlib.pyplot import figure,show,subplots
import seaborn as sns
sns.set_context('talk',font_scale=1.25)
#
from tincanradar.fwdmodel import chirp

try:
    import pygame as smod
except ImportError:
    smod = None
scfs = 48e3

def harmonicradar_sim(fs,tm,fc,f0,f1,range_m,mode):
    t = np.arange(0, tm, 1/fs)

    if 'cw' in mode:
        harmonicradar_cw(t,fs,fc)
    if 'fmcw' in mode:
        harmonicradar_fmcw(t,tm,fs,f0,f1,range_m)

def harmonicradar_cw(t,fs,fc):
    ttxt = f'CW: {fc} Hz'
    #%% input
    x = np.sin(2*np.pi*fc*t)
    _,Pxx = signal.periodogram(x,fs)
    #%% diode
    d = (signal.square(2*np.pi*fc*t))
    d[d<0] = 0.
    #%% output of diode
    y = x * d
    #y = x; y[y<0]=0. #shorthand way to say it, same result
    fax,Pyy = signal.periodogram(y,fs)
#%% results
    plotlf(t,x,d,y,ttxt)
    plots(fax,Pxx,Pyy,fc,ttxt)

def harmonicradar_fmcw(t,tm,fs,f0,f1,range_m):
    bm = f1-f0
    ttxt = 'FMCW: {} -> {} Hz'.format(f0,f1)
    #x = chirp(t,f0,t[-1],f1,'linear') #radar transmit waveform
#%% target harmonic radar tag
    #t_targ = 2 * asarray(range_m)/c #round trip time delay due to target distance
    #phase_targ = 2*pi*linspace(f0,f1,x.size)*t_targ
    #y = chirp(t,f0,t[-1],f1,'linear',phi=degrees(phase_targ))
    y,x = chirp(bm,tm,t,range_m, Atarg=1, nlfm=0.)
    #y[y<0]=0. #tag transmit waveform

    fax,Pxx = signal.periodogram(x,fs)
    fax,Pyy = signal.periodogram(y,fs,detrend=False)

    plots(fax,None,Pyy,fc,ttxt)
#%% radar received waveform (homodyne)
    z = y * x.conjugate()#tag transmit waveform
#%% antialias filter & resample
    b = signal.firwin(numtaps=100, cutoff=fs/4., nyq=fs/2.) # LPF
    zf = signal.lfilter( b, 1., z)
    zr,tz = signal.resample(zf,int(zf.size * scfs / fs),t)
    faz,Pzz = signal.periodogram(zr,scfs,detrend=False)

    plotif(tz,zr,faz,Pzz)

    sounds(zr)


def plotif(t,z,fax,Pzz):
    fg,axs = subplots(2,1)
    ax=axs[0]
    ax.plot(t,z)
    ax.set_xlabel('time [sec]')

    ax=axs[1]
    ax.plot(fax,Pzz)
    ax.set_xlim(0,6*fc)
    ax.set_xlabel('frequency [Hz]')

def plotlf(t,x,d,y,ttxt):

    fg = figure()
    ax = fg.gca()
    ax.plot(t,x,label='input')
    if d is not None:
       ax.plot(t,d,label='Diode action')
    if y is not None:
        ax.plot(t,y,label='output')
    ax.legend(loc='lower left')
    ax.set_xlabel('time [sec]')
    ax.set_ylabel('amplitude')
    ax.autoscale(True,tight=True)
    ax.set_title(ttxt)


def plots(fax,Pxx,Pyy,fc,ttxt):
    fg,axs = subplots(2,1,sharex=True)
    fg.suptitle(ttxt + ' spectral power density\nhomodyne reception-zero IF')

    if Pxx is not None:
        ax=axs[0]
        ax.plot(fax,10*np.log10(Pxx))
        ax.set_ylabel('$P_{xx}$')

    ax=axs[1]
    ax.plot(fax,10*np.log10(Pyy))
    ax.set_xlabel('frequency [Hz]')
    ax.set_ylabel('$P_{yy}$')
    #ax.set_xlim(0,6*fc)

 #   for ax in axs:
 #       ax.set_ylim(-60,-10)

def sounds(x):
#%% playback
    """
    Note: You must SCALE and convert your data to signed 16-bit integers,
    that's what your sound card uses.
    """
    if smod is not None:
        smod.mixer.pre_init(int(scfs), size=-16, channels=1)
        smod.mixer.init()
        sound = smod.sndarray.make_sound((x*32768/8).astype('int16'))
        sound.play(loops=0)
        if not np.isclose(sound.get_volume(),1.):
            print('pygame volume level:',sound.get_volume())

if __name__ == '__main__':
    mode=['fmcw']

    tm = 10e-3
    fc = 1000


    f0 = 902e6
    f1 = 928e6

    rfs=4*(f1-f0)

    range_m = 50. #range to target

    harmonicradar_sim(rfs,tm,fc,f0,f1,range_m,mode)

    show()
