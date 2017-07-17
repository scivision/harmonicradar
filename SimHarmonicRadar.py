#!/usr/bin/env python
import numpy as np
import seaborn as sns
sns.set_context('talk')
from matplotlib.pyplot import show
#
from harmonicradar import harmonicradar_sim
#
try:
    import pygame as smod
except ImportError:
    smod = None
#
scfs = 48e3


def sounds(x):
#%% playback
    """
    Note: You must SCALE and convert your data to signed 16-bit integers,
    that's what your sound card uses.
    """
    if smod is not None:
        smod.mixer.pre_init(int(scfs), size=-16, channels=1)
        smod.mixer.init()
        sound = smod.sndarray.make_sound((x*32768/8).real.astype('int16'))
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


    rx = harmonicradar_sim(P, p.range_m,scfs)

    sounds(rx)

    show()
