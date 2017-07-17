function hradar()

range_m = 30; % meters

scfs = 48e3; % Hz sampling frequency of sound card (for audio playback)


P.tm = 0.1; % sec.
P.f1 = 928e6; % Hz
P.f0 = 902e6; % Hz
P.bm = P.f1-P.f0; % Hz bandwidth of FMCW
P.mode='fmcw';

py.harmonicradar.harmonicradar_sim(P,range_m,scfs)


end % function