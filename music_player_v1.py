# music_player_v1.py

import os
import threading
import tkinter.ttk as ttk
import wave
from tkinter import *
from tkinter import filedialog

import pyaudio
import struct
from matplotlib import pyplot
from pygame import *


class MusicPlayer:
    def __init__(self, window):
        window.geometry('500x480')
        window.title('Music Player')
        window.resizable(0, 0)

        # create the playlist
        self.playlist = Listbox(window, height=10, width=60)
        self.playlist.grid(row=0, column=0)

        # create the horizontal scrollbar to get a better view of the playlist
        self.scrollbar = Scrollbar(Frame(self.playlist), orient=VERTICAL, command=self.playlist.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.playlist['yscrollcommand'] = self.scrollbar.set
        # TODO: check if the scrollbar is functional
        self.scrollbar.grid(row=20, column=2, sticky=(N, S))
        self.playlist.pack()

        quit_button = Button(window, text='Quit', width=7, command=root.quit)
        open_file_button = Button(window, text='Open File', width=10, command=self.load_file)
        open_folder_button = Button(window, text='Open Dir', width=10, command=self.load_folder)
        play_button = Button(window, text='Play', width=10, command=self.play)
        pause_button = Button(window, text='Pause / Resume', width=10, command=self.pause)
        stop_button = Button(window, text='Stop', width=10, command=self.stop)
        prev_song_button = Button(window, text='<<', width=5, command=self.prev_song)
        next_song_button = Button(window, text='>>', width=5, command=self.next_song)
        # TODO: progress bar not working
        self.progress_bar = ttk.Progressbar(window, orient=HORIZONTAL, length=100, mode='determinate')
        self.progress_bar.pack()

        # at the top of the GUI window: open file and folder buttons
        open_file_button.place(x=100, y=20)
        open_folder_button.place(x=300, y=20)

        # the second row of the GUI window
        play_button.place(x=60, y=60)
        pause_button.place(x=200, y=60)
        stop_button.place(x=340, y=60)

        # the third row of the GUI window

        prev_song_button.place(x=100, y=100)
        next_song_button.place(x=350, y=100)

        quit_button.place(x=200, y=400)

        self.playlist.place(x=5, y=160)
        self.progress_bar.place(x=20, y=340)
        self.music_file = False
        self.playing_state = False
        self.lst_pos = 1
        self.musicdirs = []
        mixer.init()

    # def checkNextSong:
    # 	if mixer.music.get_endevent()==1 and self.lst.get(self.lst.curselection()):
    # 		self.music_file=self.lst.get(self.lst.curselection())
    # 		mixer.music.load(self.music_file)
    # 		mixer.music.play()

    def load_file(self):
        self.playlist.insert(self.lst_pos, filedialog.askopenfilename())
        print('music file from the loading', self.music_file)
        # self.lst.insert(self.music_file)

    def load_folder(self):
        source_path = filedialog.askdirectory()
        self.dirs = os.listdir(source_path)
        self.lst_pos = self.playlist.size()
        for file in self.dirs:
            if file:
                if file.endswith('.wav'):
                    self.playlist.insert(self.lst_pos, source_path + '/' + file)
                    self.musicdirs.append(source_path + '/' + file)
                    self.lst_pos = self.lst_pos + 1
        self.scrollbar.config(command=self.playlist.yview)
        # self.lst.insert(self.music_file)

    def play(self):
        if self.playlist.curselection():
            if self.playlist.get(self.playlist.curselection()):
                self.lst_pos = self.playlist.curselection()
                self.music_file = self.playlist.get(self.playlist.curselection())

                mixer.music.load(self.music_file)
                print('music_file from the playing button', self.music_file)
                # mixer.music.play()
                self.playing_state = True

                wavfile = self.music_file
                # Open wave file
                wf = wave.open(wavfile, 'rb')

                # Read wave file properties
                RATE = wf.getframerate()  # Frame rate (frames/second)
                WIDTH = wf.getsampwidth()  # Number of bytes per sample
                CHANNELS = wf.getnchannels()  # Number of channels
                BLOCKLEN = 1000  # Blocksize

                # Set up plotting...
                pyplot.ion()  # Turn on interactive mode so plot gets updated
                [g1] = pyplot.plot([], [])

                g1.set_xdata(range(BLOCKLEN))
                pyplot.ylim(-32000, 32000)
                pyplot.xlim(0, BLOCKLEN)

                # Open the audio output stream
                p = pyaudio.PyAudio()

                PA_FORMAT = p.get_format_from_width(WIDTH)  # WIDTH = 2 because it is a 16-bit sample wavefile
                stream = p.open(
                    format=PA_FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=False,
                    output=True,
                    frames_per_buffer=1024)
                # low latency so that plot and output audio are synchronized
                # choose frames_per_buffer=1024 so that the computer could keep up with the latency caused by pyaudio

                # Get block of samples from wave file
                input_bytes = wf.readframes(BLOCKLEN)  # binary data

                while self.playing_state and len(input_bytes) >= BLOCKLEN * WIDTH:
                    # Convert binary data to number sequence (tuple) - numeric data
                    signal_block = struct.unpack('h' * BLOCKLEN, input_bytes)

                    g1.set_ydata(signal_block)
                    pyplot.pause(0.0001)

                    # Write binary data to audio output stream
                    stream.write(input_bytes, BLOCKLEN)

                    # Get block of samples from wave file
                    input_bytes = wf.readframes(BLOCKLEN)

                stream.stop_stream()
                stream.close()
                p.terminate()

                wf.close()

                pyplot.ioff()  # Turn off interactive mode
                pyplot.show()  # Keep plot showing at end of program
                pyplot.close()
                print('* Finished')

    # else:
    # 	thread = threading.Thread(target=self.playAll())
    # 	thread.daemon = True
    # 	thread.start()
    # p.start()
    def prev_song(self):
        if self.playlist.curselection() and self.playing_state == True:
            if self.playlist.get(self.playlist.curselection()[0]):
                self.lst_pos = self.playlist.curselection()[0] - 1
                if self.lst_pos < 0:
                    self.lst_pos = self.playlist.size() - 1
                print(self.lst_pos)
                self.playlist.selection_clear(0, END)
                self.playlist.selection_set(first=self.lst_pos)
                self.playlist.activate(self.lst_pos)
                self.playlist.index(self.lst_pos)
                self.music_file = self.playlist.get(self.playlist.curselection())
                mixer.music.load(self.music_file)
                mixer.music.play()
                self.playing_state = True

    def next_song(self):
        if self.playlist.curselection():
            if self.playlist.get(self.playlist.curselection()[0]) and self.playing_state == True:
                self.lst_pos = self.playlist.curselection()[0] + 1
                if self.lst_pos > self.playlist.size() - 1:
                    self.lst_pos = 0
                print(self.lst_pos)
                self.playlist.selection_clear(0, END)
                self.playlist.selection_set(first=self.lst_pos)
                self.playlist.activate(self.lst_pos)
                self.playlist.index(self.lst_pos)
                self.music_file = self.playlist.get(self.playlist.curselection())
                mixer.music.load(self.music_file)
                mixer.music.play()
                self.playing_state = True  # else:

    def pause(self):
        if self.playing_state:
            mixer.music.pause()
            self.playing_state = False
        else:
            mixer.music.unpause()
            self.playing_state = True
            mixer.music.play()
            # self.play()

    def stop(self):
        mixer.music.stop()
        self.playing_state = False


if __name__ == '__main__':
    root = Tk()
    app = MusicPlayer(root)
    barThread = threading.Thread(target=1, args=(1,))
    # set thread as daemon (thread will die if parent is killed)
    barThread.daemon = True
    # Start thread, could also use root.after(50, barThread.start()) if desired
    barThread.start()
    root.mainloop()
