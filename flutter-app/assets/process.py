#import numpy
import numpy as np
from scipy import signal




def process():


    #"""
    __all__ = ['octavefilter', 'getansifrequencies', 'normalizedfreq']

    def _buttersosfilter(freq, freq_d, freq_u, fs, order, factor, show=0):
        # Initialize coefficients matrix
        sos = [[[]] for i in range(len(freq))]
        # Generate coefficients for each frequency band
        for idx, (lower, upper) in enumerate(zip(freq_d, freq_u)):
            # Downsampling to improve filter coefficients
            fsd = fs / factor[idx]  # New sampling rate
            # Butterworth Filter with SOS coefficients
            sos[idx] = signal.butter(
                N = order,
                Wn = np.array([lower, upper]) / (fsd / 2),
                btype = 'bandpass',
                analog = False,
                output = 'sos')

        return sos

    def _genfreqs(limits, fraction, fs):
        # Generate frequencies
        freq, freq_d, freq_u = getansifrequencies(fraction, limits)

        # Remove outer frequency to prevent filter error (fs/2 < freq)
        freq, freq_d, freq_u = _deleteouters(freq, freq_d, freq_u, fs)

        return freq, freq_d, freq_u


    def normalizedfreq(fraction):
        predefined = {
            3: _thirdoctave(),
        }
        return predefined[fraction]


    def _thirdoctave():
        # IEC 61260 - 1 - 2014 (added 12.5, 16, 20 Hz)
        return [4, 5, 6.3, 8, 10, 12.5, 16, 20, 25, 31.5, 40, 50, 63, 80, 100,
                125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000]


    def _deleteouters(freq, freq_d, freq_u, fs):
        idx = np.asarray(np.where(np.array(freq_u) > fs / 2))
        if any(idx[0]):
            freq = np.delete(freq, idx).tolist()
            freq_d = np.delete(freq_d, idx).tolist()
            freq_u = np.delete(freq_u, idx).tolist()
        return freq, freq_d, freq_u


    def getansifrequencies(fraction, limits=None):

        if limits is None:
            limits = [4, 2000]

        # Octave ratio g (ANSI s1.11, 3.2, pg. 2)
        g = 10 ** (3 / 10)  # Or g = 2
        # Reference frequency (ANSI s1.11, 3.4, pg. 2)
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


    def _initindex(f, fr, g, b):
        if b % 2:  # ODD ('x' solve from ANSI s1.11, eq. 3)
            return np.round(
                (b * np.log(f / fr) + 30 * np.log(g)) / np.log(g)
            )
        else:  # EVEN ('x' solve from ANSI s1.11, eq. 4)
            return np.round(
                (2 * b * np.log(f / fr) + 59 * np.log(g)) / (2 * np.log(g))
            )


    def _ratio(g, x, b):
        if b % 2:  # ODD (ANSI s1.11, eq. 3)
            return g ** ((x - 30) / b)
        else:  # EVEN (ANSI s1.11, eq. 4)
            return g ** ((2 * x - 59) / (2 * b))


    def _bandedge(g, b):
        # Band-edge ratio (ANSI s1.11, 3.7, pg. 3)
        return g ** (1 / (2 * b))


    def _downsamplingfactor(freq, fs):
        guard = 0.10
        factor = (np.floor((fs / (2+guard)) / np.array(freq))).astype('int')
        for idx in range(len(factor)):
            # Factor between 1<factor<50
            factor[idx] = max(min(factor[idx], 50), 1)
        return factor

    def octavefilter(x, fs, fraction=3, order=6, limits=None, show=0, sigbands =0):

        # Generate frequency array
        freq, freq_d, freq_u = _genfreqs(limits, fraction, fs)

        # Calculate the downsampling factor (array of integers with size [freq])
        factor = _downsamplingfactor(freq_u, fs)

        # Get SOS filter coefficients (3D - matrix with size: [freq,order,6])
        sos = _buttersosfilter(freq, freq_d, freq_u, fs, order, factor, show)

        # Create array with SPL for each frequency band
        spl = np.zeros([len(freq)])
        for idx in range(len(freq)):
            sd = signal.decimate(x, factor[idx])
            y = signal.sosfilt(sos[idx], sd)
            spl[idx] = np.sqrt(np.mean(np.square(y)))
        return spl.tolist()

    x , y, z = [], [], []

    A_hw_rms_x, A_hw_rms_y, A_hw_rms_z = [], [], []

    fs = 4500

    octave_weights = [0.375, 0.545, 0.727, 0.873, 0.951, 0.958, 0.896, 0.782, 0.647, 0.519, 0.411, 0.324, 0.256, 0.202, 0.160, 0.127, 0.101, 0.0799, 0.0634, 0.0503, 0.0398, 0.0314, 0.0245, 0.0186, 0.0135, 0.00894, 0.00536, 0.00295]
    
    for element in dataset:
        x.append(element[0])
        y.append(element[1])
        z.append(element[2])

    # Filter (get spectra and signal in bands)
    A_hi_rms_x = octavefilter(x, fs=fs, fraction=3, order=30, limits=[4, 2000], show=0)
    A_hi_rms_y = octavefilter(y, fs=fs, fraction=3, order=30, limits=[4, 2000], show=0)
    A_hi_rms_z = octavefilter(z, fs=fs, fraction=3, order=30, limits=[4, 2000], show=0)

    for i in range(len(octave_weights)):
        A_hw_rms_x.append(octave_weights[i] * A_hi_rms_x[i])
        A_hw_rms_y.append(octave_weights[i] * A_hi_rms_y[i])
        A_hw_rms_z.append(octave_weights[i] * A_hi_rms_z[i])


    arr_x = np.array(A_hw_rms_x)
    arr_y = np.array(A_hw_rms_y)
    arr_z = np.array(A_hw_rms_z)

    xx = np.sqrt(np.sum(np.square(arr_x)))
    yy = np.sqrt(np.sum(np.square(arr_y)))
    zz = np.sqrt(np.sum(np.square(arr_z)))
    
    np.sqrt(np.sum(xx**2 + yy**2 + zz**2))
    #"""
    return 1