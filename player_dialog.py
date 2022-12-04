import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


class OpenFile:
    def __init__(self):
        root = tk.Tk()
        root.title('Open Music File Dialog')
        root.resizable(False, False)
        root.geometry('300x150')
        open_button = ttk.Button(
            root,
            text='Open a wav file',
            command=self.select_file
        )
        open_button.pack(expand=True)
        # set the edfault wav file
        self.file = "wavefiles/sample-12s.wav"
        root.mainloop()

    def select_file(self):
        filetypes = (('wave files', '*.wav'),)

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        showinfo(message='Please close the window to play the wav file you selected.')
        self.file = filename
