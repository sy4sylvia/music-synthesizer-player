# converter.py
# converts the MIDI file to wav file

from collections import defaultdict

from pydub import AudioSegment
from pydub.generators import Sine
from datetime import datetime


def converter(mid_file):

    output = AudioSegment.silent(mid_file.length * 1000.0)
    tempo = 60   # bpm, remain the same as the generator
    tick_per_ms = (60000.0 / tempo) / mid_file.ticks_per_beat

    for track in mid_file.tracks:
        current_time_stamp = 0.0

        current_notes = defaultdict(dict)

        for msg in track:

            current_time_stamp += tick_per_ms * msg.time

            if msg.type == 'note_on':
                current_notes[msg.channel][msg.note] = (current_time_stamp, msg)

            if msg.type == 'note_off':
                start_time_stamp, start_msg = current_notes[msg.channel].pop(msg.note)

                duration = current_time_stamp - start_time_stamp

                # uses a sine wave generator
                # frequency converted from the note based on the formula: note = 69 + 12 * log2(f / 440)
                # https://en.wikipedia.org/wiki/MIDI_tuning_standard#Frequency_values
                sine_wave = Sine((2.0 ** ((msg.note - 69) / 12.0)) * 440)
                rendered = sine_wave.to_audio_segment(duration=duration-50, volume=-20).fade_out(100).fade_in(30)
                output = output.overlay(rendered, start_time_stamp)

        # add the date suffix to the name of the output wav file
        date = datetime.now().strftime("%m%d%Y")
        output_file_name = "output_" + date + ".wav"
        # uses the export function from pydub
        output.export('music_clips/' + output_file_name, format="wav")
