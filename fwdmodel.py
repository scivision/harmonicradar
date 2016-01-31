from numpy import pi,log10

LIGHTSPEED=299792458 #[m/s]

def friis(dist_m,freq_hz):
    """
    free space path loss [dB]
    dist_m: Distance between radar and tag in meters (one-way)
    freq: carrier frequency of the radar in Hz
    """
    return 20*log10(4*pi * dist_m * freq_hz / LIGHTSPEED) #[dB]

def noisepower(nf,bw):

    """
    Compute noise power for receiver in dBm
    Note: we are talking power not PSD.
    nf: noise figure [dB] cascaded for the entire receiver
    bw: receiver bandwidth [Hz] this is the bandwidth of the final filter in the system
    """
    k=1.38064852e-23
    T=290 #[K] by convention

  
    return 10*log10(k*T*bw) + nf  #[dBm] DSB
