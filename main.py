import json

from mido import MidiFile
from music_generator import MusicClip
from converter import converter

from music_visualizer import generate_visualizer

from player_dialog import *

if __name__ == '__main__':
    params_file = open("config/setting.json", "r")
    params = json.load(params_file)
    params_file.close()

    my_music_clip = MusicClip()
    mid_file_name = "output.mid"
    my_music_clip.create_midi_file(mid_file_name)
    # my_music_clip.create_midi_file("{folder}/output.mid".format(folder="music_clips"))

    mid = MidiFile(mid_file_name)
    converter(mid)

    root = tk.Tk()
    dialog = OpenFile(root)
    root.mainloop()

    filename = dialog.file
    print('opened file, ', filename)

    generate_visualizer(filename)
