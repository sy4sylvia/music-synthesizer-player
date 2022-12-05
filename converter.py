from collections import defaultdict

from pydub import AudioSegment
from pydub.generators import Sine
from datetime import datetime


def note_to_freq(note):
    # https://en.wikipedia.org/wiki/MIDI_tuning_standard#Frequency_values
    base_freq = 440  # Frequency of Note A4
    return (2.0 ** ((note - 69) / 12.0)) * base_freq


def ticks_to_ms(ticks, mid_file):
    tempo = 60  # bpm, remain the same as the generator
    tick_ms = (60000.0 / tempo) / mid_file.ticks_per_beat
    return ticks * tick_ms


def converter(mid_file):
    output = AudioSegment.silent(mid_file.length * 1000.0)
    for track in mid_file.tracks:
        current_time_stamp = 0.0

        current_notes = defaultdict(dict)

        for msg in track:
            current_time_stamp += ticks_to_ms(msg.time, mid_file)

            if msg.type == 'note_on':
                current_notes[msg.channel][msg.note] = (current_time_stamp, msg)

            if msg.type == 'note_off':
                start_pos, start_msg = current_notes[msg.channel].pop(msg.note)

                duration = current_time_stamp - start_pos
                # uses a sine wave generator
                signal_generator = Sine(note_to_freq(msg.note))
                rendered = signal_generator.to_audio_segment(duration=duration - 50, volume=-20).fade_out(100).fade_in(
                    30)

                output = output.overlay(rendered, start_pos)

        # add the date suffix to the name of the output wav file
        date = datetime.now().strftime("%m%d%Y")
        output_file_name = "output_" + date + ".wav"
        # uses the export function from pydub
        output.export('music_clips/' + output_file_name, format="wav")
