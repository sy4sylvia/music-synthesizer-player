# note_generator.py generates a note randomly
import random


class Note(object):
    def __init__(self, octave, lower, upper):
        self.prev_note = 0
        self.notes = octave  # a list of notes
        self.lower = lower
        self.upper = upper

    def generate_note(self):
        octave_range = range(1, len(self.notes) + 1)

        while True:
            cur_note = random.choice(octave_range)
            random_lower = random.choice(self.lower)
            random_upper = random.choice(self.upper)

            if self.prev_note != 0:
                break
            elif random_lower <= abs(cur_note - self.prev_note) <= random_upper:
                break

        self.prev_note = cur_note
        return self.notes[cur_note - 1]

    def reset(self):
        self.prev_note = 0  # reset the prev note
