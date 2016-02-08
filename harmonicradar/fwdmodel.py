from numpy import pi,log10
from numpy.testing import assert_allclose
#
from tincanradar.fwdmodel import friis

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

    Pthermal = 10*log10(k*T*bw)+30 #+30 for dBW to dBm

    return Pthermal + nf  #[dBm] DSB

if __name__ == '__main__':
    assert_allclose(noisepower(8,25e3),-121.995788617)
    assert_allclose(friis(1e3,144e6), 75.6150330638)