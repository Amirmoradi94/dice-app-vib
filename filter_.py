
import numpy as np
from scipy import signal



#"""
def _initindex(f, fr, g, b):
    if b % 2:  # ODD ('x' solve from ANSI s1.11, eq. 3)
        return np.round(
                (b * np.log(f / fr) + 30 * np.log(g)) / np.log(g)
                )
    else:  # EVEN ('x' solve from ANSI s1.11, eq. 4)
        return np.round((2 * b * np.log(f / fr) + 59 * np.log(g)) / (2 * np.log(g)))  


def _ratio(g, x, b):
    if b % 2:  # ODD (ANSI s1.11, eq. 3)
        return g ** ((x - 30) / b)
    else:  # EVEN (ANSI s1.11, eq. 4)
        return g ** ((2 * x - 59) / (2 * b))

def _bandedge(g, b):
    # Band-edge ratio (ANSI s1.11, 3.7, pg. 3)
    return g ** (1 / (2 * b))


def getansifrequencies(fraction, limits=None):

    if limits is None:
        limits = [4, 2000]

    g = 10 ** (3 / 10)  # Or g = 2
    fr = 1000
    
    # Get starting index 'x' and first center frequency
    x = _initindex(limits[0], fr, g, fraction)
    freq = _ratio(g, x, fraction) * fr
    
    # Get each frequency until reach maximum frequency
    freq_x = 0
    while freq_x * _bandedge(g, fraction) < limits[1]:
        # Increase index
        x = x + 1
        # New frequency
        freq_x = _ratio(g, x, fraction) * fr
        # Store new frequency
        freq = np.append(freq, freq_x)
    # Get band-edges
    freq_d = freq / _bandedge(g, fraction)
    freq_u = freq * _bandedge(g, fraction)
    return freq.tolist(), freq_d.tolist(), freq_u.tolist()    


def _deleteouters(freq, freq_d, freq_u, fs):
    idx = np.asarray(np.where(np.array(freq_u) > fs / 2))
    if any(idx[0]):
        #_printwarn('Low sampling rate, frequencies above fs/2 will be removed')
        freq = np.delete(freq, idx).tolist()
        freq_d = np.delete(freq_d, idx).tolist()
        freq_u = np.delete(freq_u, idx).tolist()
    return freq, freq_d, freq_u


def _genfreqs(limits, fraction, fs):
    # Generate frequencies
    freq, freq_d, freq_u = getansifrequencies(fraction, limits)
    
    # Remove outer frequency to prevent filter error (fs/2 < freq)
    freq, freq_d, freq_u = _deleteouters(freq, freq_d, freq_u, fs)
    
    return freq, freq_d, freq_u


def _thirdoctave():
    return [4, 5, 6.3, 8, 10, 12.5, 16, 20, 25, 31.5, 40, 50, 63, 80, 100, 
            125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000]



def _downsamplingfactor(freq, fs):
    guard = 0.10
    factor = (np.floor((fs / (2+guard)) / np.array(freq))).astype('int')
    for idx in range(len(factor)):
        # Factor between 1<factor<50
        factor[idx] = max(min(factor[idx], 50), 1)
    return factor


def octavefilter(x, fs=4500, fraction=3, order=6, limits=[4, 2000]):
    
    octave_weights = [0.375, 0.545, 0.727, 0.873, 0.951, 0.958, 0.896, 0.782, 0.647, 0.519, 0.411, 0.324, 0.256, 0.202, 0.160, 0.127, 0.101, 0.0799, 0.0634, 0.0503, 0.0398, 0.0314, 0.0245, 0.0186, 0.0135, 0.00894, 0.00536, 0.00295]

    
    if limits is None:
        limits = [4, 2000]
    
    freq, freq_d, freq_u = _genfreqs(limits, fraction, fs)
    
    factor = _downsamplingfactor(freq_u, fs)
    
    
    sos = [[[]] for i in range(len(freq))]
    
    
    for idx, (lower, upper) in enumerate(zip(freq_d, freq_u)):
        
        fsd = fs / factor[idx]  # New sampling rate
        sos[idx] = signal.butter(N = order, 
                      Wn = np.array([lower, upper]) / (fsd / 2), 
                      btype = 'bandpass', 
                      fs = 4500,
                      output='sos')
    

    # Create array with SPL for each frequency band
    spl = np.zeros([len(freq)])
    for idx in range(len(freq)):
        sd = signal.decimate(x, factor[idx])
        
        y = signal.sosfilt(sos[idx], sd)
        
        spl[idx] = np.sqrt(np.mean(np.square(y)))
    
    weighted_output = np.array(octave_weights) * np.array(spl)
    
    return np.sqrt(np.sum(np.square(weighted_output)))
