import json

from mido import MidiFile
from music_generator import MusicClip
from converter import converter

from player_dialog import *
import tkinter as tk

from music_visualizer import generate_visualizer

if __name__ == '__main__':
    params_file = open("config/setting.json", "r")
    params = json.load(params_file)
    params_file.close()

    my_music_clip = MusicClip()
    mid_file_name = "output.mid"
    my_music_clip.create_midi_file(mid_file_name)

    mid = MidiFile(mid_file_name)
    converter(mid)

    root = tk.Tk()
    dialog = OpenFile(root)
    root.mainloop()

    filename = dialog.file
    print('Opened file: ', filename)

    generate_visualizer(filename)

    print('Finished visualizing the music clip')
