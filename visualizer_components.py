import librosa.display
import numpy as np
import pygame

# min_height = 10
# max_height = 100
# min_decibel = -80
# max_decibel = 0

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
        self.spectrogram = None  # a matrix that contains decibel values according to frequency and time indexes

    def load(self, filename):
        # getting information from the file
        # y, 1D array, represents the time when each sample was taken.
        # sample_rate is how much samples are taken per period.
        y, sample_rate = librosa.load(filename)

        # The Short-time Fourier transform (STFT), is a Fourier-related transform used to determine the sinusoidal
        # frequency and phase content of local sections of a signal as it changes over time.(Wikipedia)

        # getting a matrix which contains amplitude values according to frequency and time indices
        stft = np.abs(librosa.stft(y, hop_length=HOP_LENGTH, n_fft=N_FFT))

        # converting the matrix to decibel matrix
        self.spectrogram = librosa.amplitude_to_db(stft, ref=np.max)

        freqs = librosa.core.fft_frequencies(n_fft=N_FFT)  # getting an array of frequencies

        # getting an array of time periodic
        times = librosa.core.frames_to_time(np.arange(self.spectrogram.shape[1]), sr=sample_rate, hop_length=HOP_LENGTH,
                                            n_fft=N_FFT)

        self.time_idx_ratio = len(times) / times[len(times) - 1]
        self.freq_idx_ratio = len(freqs) / freqs[len(freqs) - 1]

    # returning the current decibel according to the indices
    def get_decibel(self, target_time, freq):
        return self.spectrogram[int(freq * self.freq_idx_ratio)][int(target_time * self.time_idx_ratio)]


class BasicBar:  # -> AudioBar
    def __init__(self, x, y, freq, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = min_height  # initial height

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

    def show_bar(self, window):
        rect = (self.x, self.y + self.max_height - self.height, self.width, self.height)
        pygame.draw.rect(window, self.color, rect)


class SimpleBar(BasicBar):
    def __init__(self, x, y, rng, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        super().__init__(x, y, 0, color, width, min_height, max_height, min_decibel, max_decibel)

        self.rng = rng
        self.avg = 0

    def update_all(self, delta_time, time, analyzer):
        self.avg = 0
        for i in self.rng:
            self.avg += analyzer.get_decibel(time, i)

        self.avg /= len(self.rng)
        self.update_bar(delta_time, self.avg)


class RotatedBar(SimpleBar):
    # There needs to be a default value for the width and the .... etc
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

        # four corners of the rectangle
        self.points = []
        self.origin = [self.width / 2, 0]
        self.offset = [self.origin[0] + x, self.origin[1] + y]

        self.rotate_rectangle(0)

    def rotate_rectangle(self, angle):
        template = [
            (-self.origin[0], self.origin[1]),
            (-self.origin[0] + self.width, self.origin[1]),
            (-self.origin[0] + self.width, self.origin[1] - self.height),
            (-self.origin[0], self.origin[1] - self.height)
        ]

        self.points = [convert(rotate_matrix(point, np.radians(angle)), self.offset) for point in template]

    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 0), self.points)
