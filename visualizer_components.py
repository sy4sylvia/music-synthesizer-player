import librosa.display
import numpy as np
import pygame

HOP_LENGTH = 512
N_FFT = 2048 * 4


def rotate_matrix(coordinate, angle):
    return (coordinate[0] * np.cos(angle) - coordinate[1] * np.sin(angle),
            coordinate[0] * np.sin(angle) + coordinate[1] * np.cos(angle))


def convert(coordinate, offset):
    return coordinate[0] + offset[0], coordinate[1] + offset[1]


def clip(min_val, max_val, val):
    if val < min_val:
        return min_val
    elif val > max_val:
        return max_val
    else:
        return val


class MusicAnalyzer:

    def __init__(self):
        self.freq_idx_ratio = 0  # array for frequencies
        self.time_idx_ratio = 0  # array of time periods
        # a matrix that contains decibel values according to frequency and time indices, dB-scaled spectrogram
        self.spectrogram = None

    def load(self, filename):
        # y is an 1D array that represents the time when each sample was taken.
        # sample_rate is how much samples are taken per period.
        y, sample_rate = librosa.load(filename)

        # TODO: delete this line from Wiki after the report is complete
        # The Short-time Fourier transform (STFT), is a Fourier-related transform used to determine the sinusoidal
        # frequency and phase content of local sections of a signal as it changes over time -- Wikipedia

        # getting a matrix which contains amplitude values according to frequency and time indices
        amplitude_spectrogram = np.abs(librosa.stft(y, hop_length=HOP_LENGTH, n_fft=N_FFT))

        # converts the amplitude spectrogram to dB-scaled spectrogram
        self.spectrogram = librosa.amplitude_to_db(amplitude_spectrogram, ref=np.max)

        freqs = librosa.core.fft_frequencies(n_fft=N_FFT)

        cur_frames = np.arange(self.spectrogram.shape[1])
        times = librosa.core.frames_to_time(cur_frames, sr=sample_rate, hop_length=HOP_LENGTH, n_fft=N_FFT)

        self.time_idx_ratio = len(times) / times[len(times) - 1]
        self.freq_idx_ratio = len(freqs) / freqs[len(freqs) - 1]

    # returning the current decibel from the dB-scaled spectrogram according to the indices
    def get_decibel(self, target_time, freq):
        row = int(freq * self.freq_idx_ratio)
        col = int(target_time * self.time_idx_ratio)
        return self.spectrogram[row][col]


# The frequency bar
class BasicBar:
    def __init__(self, x, y, freq, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        self.x = x
        self.y = y
        self.width = width
        # set the initial height to be the min height in case no signal has this frequency
        self.height = min_height

        self.color = color
        self.freq = freq

        self.min_decibel = min_decibel
        self.max_decibel = max_decibel

        self.min_height = min_height
        self.max_height = max_height
        # TODO: what to do with this ratio?
        self.ratio = (self.max_height - self.min_height) / (self.max_decibel - self.min_decibel)

    def update_bar(self, delta_time, decibel):
        # delta_time is the time differences between two updates
        new_height = decibel * self.ratio + self.max_height
        speed = (new_height - self.height) / 0.1
        self.height += speed * delta_time
        self.height = clip(self.min_height, self.max_height, self.height)


class SimpleBar(BasicBar):
    def __init__(self, x, y, rng, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        super().__init__(x, y, 0, color, width, min_height, max_height, min_decibel, max_decibel)

        self.rng = rng
        self.db = 0

    def update_all(self, delta_time, time, analyzer):
        self.db = 0
        for freq in self.rng:
            self.db += analyzer.get_decibel(time, freq)

        self.db /= len(self.rng)
        self.update_bar(delta_time, self.db)


class RotatedBar(SimpleBar):
    # default values are added in case these parameters are eliminated
    def __init__(self, x, y, rng, color, angle=0, width=8, min_height=10, max_height=370, min_decibel=-80,
                 max_decibel=0):
        super().__init__(x, y, 0, color, width, min_height, max_height, min_decibel, max_decibel)
        self.rng = rng
        self.rect = None
        self.angle = angle

    def update_rect(self):
        self.rect = Rectangle(self.x, self.y, self.width, self.height)
        self.rect.rotate_rectangle(self.angle)


class Rectangle:
    def __init__(self, x, y, width, height):
        # axis
        self.x = x
        self.y = y

        self.width = width
        self.height = height

        # four corners of the rectangle, later used to draw the polygon
        self.points = []
        self.origin = [self.width / 2, 0]
        self.offset = [self.origin[0] + x, self.origin[1] + y]

        self.rotate_rectangle(0)

    def rotate_rectangle(self, angle):
        patterns = [(-self.origin[0], self.origin[1]), (-self.origin[0] + self.width, self.origin[1]),
                    (-self.origin[0] + self.width, self.origin[1] - self.height),
                    (-self.origin[0], self.origin[1] - self.height)]

        self.points = [convert(rotate_matrix(point, np.radians(angle)), self.offset) for point in patterns]
