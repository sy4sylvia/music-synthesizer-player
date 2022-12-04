from midiutil.MidiFile import MIDIFile
import json
from note_generator import Note


class MusicClip(object):
    def __init__(self):
        notes_attributes_file = open("config/notes.json", "r")
        settings_file = open("config/setting.json", "r")

        notes_attributes = json.load(notes_attributes_file)
        settings = json.load(settings_file)

        notes_attributes_file.close()
        settings_file.close()

        self.chords = notes_attributes["chords"]
        self.tones = notes_attributes["tones"]
        self.beats = notes_attributes["beats"]

        self.notes = Note(notes_attributes["degrees"], notes_attributes["lower"], notes_attributes["upper"])

        self.duration = settings["duration"]
        self.tempo = settings["tempo"]

        self.MyMIDI = MIDIFile(2)  # Create 2 tracks for the music piece, basic and chord.
        self.cur_track_idx = 0

    # create_sequence adds the pitch and the duration of each note inside a sequence
    def create_sequence(self):
        sequence = []
        for i in range(self.duration):
            for tone in self.tones:
                self.notes.reset()
                for duration in tone:
                    sequence.append((self.notes.generate_note(), duration))
        return sequence

    # initialize_single_track assigns the track name, add a tempo and a program change event
    def initialize_single_track(self, name):
        self.MyMIDI.addTrackName(track=self.cur_track_idx, time=0, trackName=name)
        self.MyMIDI.addTempo(track=self.cur_track_idx, time=0, tempo=self.tempo)
        self.MyMIDI.addProgramChange(tracknum=self.cur_track_idx, channel=0, time=0, program=0)

    def create_basic_track(self):
        cur_sequence = self.create_sequence()
        self.initialize_single_track("basic")

        cur_time_stamp = 0
        volume = self.beats["moderate"]
        # determine the beats according to the relative position of current note
        for pitch, duration in cur_sequence:
            relative_time_stamp = cur_time_stamp % 4
            if 0 <= relative_time_stamp < 1:
                volume = self.beats["weak"]
            elif 1 <= relative_time_stamp < 2:
                volume = self.beats["strong"]

            self.MyMIDI.addNote(
                track=self.cur_track_idx,
                channel=0,
                pitch=pitch,
                time=cur_time_stamp,
                duration=duration,
                volume=volume)

            if relative_time_stamp in [0, 2]:
                # add two channel control events
                self.MyMIDI.addControllerEvent(
                    track=self.cur_track_idx,
                    channel=0,
                    time=cur_time_stamp,
                    controller_number=64,
                    parameter=127)
                self.MyMIDI.addControllerEvent(
                    track=self.cur_track_idx,
                    channel=0,
                    time=cur_time_stamp + 1.96875,
                    controller_number=64,
                    parameter=0)
            cur_time_stamp += duration

        self.cur_track_idx += 1

    # TODO: put a pin on the chord, does not sound good
    def create_chord_track(self):
        self.initialize_single_track("chords")
        cur_time_stamp = 0

        while cur_time_stamp < self.duration * 16:
            for pitches in self.chords:
                for pitch in pitches:
                    self.MyMIDI.addControllerEvent(
                        track=self.cur_track_idx,
                        channel=0, time=cur_time_stamp, controller_number=64, parameter=127)
                    self.MyMIDI.addControllerEvent(
                        track=self.cur_track_idx,
                        channel=0, time=cur_time_stamp + 1.96875, controller_number=64, parameter=0)
                    self.MyMIDI.addNote(
                        track=self.cur_track_idx,
                        channel=0, pitch=pitch, time=cur_time_stamp, duration=2, volume=76)
                    # why 76

                    self.MyMIDI.addControllerEvent(
                        track=self.cur_track_idx,
                        channel=0, time=cur_time_stamp + 2, controller_number=64, parameter=127)
                    self.MyMIDI.addControllerEvent(
                        track=self.cur_track_idx,
                        channel=0, time=cur_time_stamp + 3.96875, controller_number=64, parameter=0)
                    self.MyMIDI.addNote(
                        track=self.cur_track_idx,
                        channel=0, pitch=pitch, time=cur_time_stamp + 2, duration=2, volume=68)
            cur_time_stamp += 4

        self.cur_track_idx = 1

    def create_midi_file(self, filename):
        self.create_basic_track()
        self.create_chord_track()

        # self.create_chord_track()
        with open(filename, "wb") as midi_file:
            self.MyMIDI.writeFile(midi_file)
