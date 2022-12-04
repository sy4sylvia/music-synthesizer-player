import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


class OpenFile:
    def __init__(self, window):
        window.title('Open Music File Dialog')
        window.geometry('300x150')
        open_button = ttk.Button(window,text='Open a wav file',command=self.select_file)
        open_button.pack(expand=True)
        # set the default wav file
        self.file = "music_clips/major-scale.wav"

    def select_file(self):
        filetypes = (('wave files', '*.wav'),)

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        showinfo(message='Please close the dialog window to play the wav file you selected.')

        self.file = filename
