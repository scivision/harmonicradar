#!/usr/bin/env python
import numpy as np
import scipy.signal as signal
from matplotlib.pyplot import figure,show,subplots
import seaborn as sns
sns.set_context('talk')
#
from tincanradar.fwdmodel import chirprx,chirptx
#
try:
    import pygame as smod
except ImportError:
    smod = None
#
scfs = 48e3

def harmonicradar_sim(P,range_m):
    fs = 4*P['bm'] # [Hz] sampling frequency of RF simulation 

    t = np.arange(0, P['tm'], 1/fs)

    if 'cw' == P['mode']:
        rx = harmonicradar_cw(t,fs,P['fc'])
    if 'fmcw' == P['mode']:
        rx = harmonicradar_fmcw(t,fs,P,range_m)
        
    return rx

def harmonicradar_cw(t,fs,fc):
    ttxt = f'CW: {fc} Hz'
    #%% input
    tx = np.sin(2*np.pi*fc*t)
    _,Pxx = signal.welch(tx,fs)
    #%% diode
    d = (signal.square(2*np.pi*fc*t))
    d[d<0] = 0.
    #%% output of diode
    rx = tx * d
    #y = x; y[y<0]=0. #shorthand way to say it, same result
    fax,Pyy = signal.periodogram(rx,fs)
#%% results
    plotlf(t,tx,d,rx,ttxt)
    plots(fax,Pxx,Pyy,fc,ttxt)
    
    return rx

def harmonicradar_fmcw(t,fs,P,range_m):
    ttxt = f'FMCW: {P["f0"]} -> {P["f1"]} Hz'
    #x = chirp(t,f0,t[-1],f1,'linear') #radar transmit waveform
#%% target harmonic radar tag
    # note, receive RF frequency is at the Nth harmonic--but bx is baseband in radar receiver after downconversion
    #tx = chirptx(P['bm'],P['tm'], t, nlfm=0.)
    
    bx,tx = chirprx(P['bm'],P['tm'],t,range_m,Atarg=1,nlfm=0.)

    f,Pxx = signal.welch(tx,fs,return_onesided=False)
    f,Pyy = signal.welch(bx,fs,return_onesided=False)

    plots(f,Pxx,Pyy,None,ttxt)
#%% radar received waveform (homodyne)
    rx = bx * tx.conjugate() # tag transmit waveform
#%% antialias filter & resample
    b = signal.firwin(numtaps=100, cutoff=fs/4., nyq=fs/2.) # LPF
    rxf = signal.lfilter( b, 1., rx)
    rxf,tr = signal.resample(rxf,int(rxf.size * scfs / fs),t)
    f,Pzz = signal.welch(rxf,scfs,detrend=False,return_onesided=False)

    plotif(tr,rxf,f,Pzz)

    return rxf


def plotif(t,x,f,Pzz,fc=None):
    fg,axs = subplots(2,1)
    ax=axs[0]
    ax.plot(t,x)
    ax.set_xlabel('time [sec]')

    ax=axs[1]
    ax.plot(f,Pzz)
    ax.set_xlabel('frequency [Hz]')
    
    if fc is not None:
        ax.set_xlim(0,6*fc)


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

    ax=axs[0]
    ax.plot(fax,10*np.log10(Pxx))
    ax.set_ylabel('$P_{tx}$')
    ax.set_title('Transmit Spectrum')
    ax.set_ylim(-120,None)

    ax=axs[1]
    ax.plot(fax,10*np.log10(Pyy))
    ax.set_xlabel('frequency [Hz]')
    ax.set_ylabel('$P_{rx}$')
    ax.set_title('Receive Spectrum')
    ax.set_ylim(-120,None)
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
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('range_m',help='range to target [m]',type=float,default=100.)
    p.add_argument('-tm',help='chirp length [sec]',type=float,default=0.01)
    p.add_argument('-m','--mode',help='radar mode (cw,fmcw)',default='fmcw')
    p.add_argument('-fc',help='freqeuncy of baseband carrier (CW only)',type=float,default=1000.)
    p.add_argument('-f',help='start stop frequency of chirp (FMCW only)',nargs=2,type=float,default=(902e6,928e6))
    p = p.parse_args()
    
    P = {'bm':p.f[1]-p.f[0],
         'f1':p.f[1],
         'f0':p.f[0],
         'fc':p.fc,
         'tm':p.tm,
         'mode':p.mode,
    }


    rx = harmonicradar_sim(P, p.range_m)
    
    sounds(rx)

    show()
