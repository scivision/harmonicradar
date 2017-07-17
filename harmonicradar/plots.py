import numpy as np
from matplotlib.pyplot import figure,subplots

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