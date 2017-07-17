import numpy as np
import scipy.signal as signal
#
from .plots import plots, plotlf, plotif
from tincanradar.fwdmodel import chirprx,friis

c=299792458 #[m/s]


def noisepower(nf,bw):
    """
    Compute noise power for receiver in dBm
    Note: we are talking power not PSD.
    nf: noise figure [dB] cascaded for the entire receiver
    bw: receiver bandwidth [Hz] this is the bandwidth of the final filter in the system
    """
    k=1.38064852e-23
    T=290 #[K] by convention

    Pthermal = 10*np.log10(k*T*bw)+30 #+30 for dBW to dBm

    return Pthermal + nf  #[dBm] DSB

def harmonicradar_sim(P,range_m,scfs):
    fs = 4*P['bm'] # [Hz] sampling frequency of RF simulation

    t = np.arange(0, P['tm'], 1/fs)

    if 'cw' == P['mode']:
        rx = harmonicradar_cw(t,fs,P['fc'])
    if 'fmcw' == P['mode']:
        rx = harmonicradar_fmcw(t,fs,P,range_m,scfs)

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

def harmonicradar_fmcw(t,fs,P,range_m,scfs):
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

