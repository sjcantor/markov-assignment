from pychord import Chord
from pretty_midi import note_name_to_number
from markov_model import Markov_Model

# Pyext library only available within PD/pyext environment.
try:
    import pyext
except:
    print("ERROR: This script must be loaded by the PD/Max pyext external")

# Set my working directory to the one where this script is located
import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
print(dname)

# import modules (yours or python's)
# from generator import Generator

# This class represents a pd object
# [pyext my_pd_objects.simple_object]


class simple_object(pyext._class):
    # There is one inlet (the leftmost) and one outlet (the rightmost) by default.
    # Add more here:
    _inlets = 2  # 3 inlets total.
    # The leftmost inlet is used to receive a "reload" message to refresh the object
    # when you chnage the code

    _outlets = 4
    _model = Markov_Model()
    _model.train()
    _nb_chords = 8
    _current_chord = 0
    _sequence = None
    _midi_notes = None

    # This method will be triggered when a "load" message is received on the third inlet
    def load_2(self, *args):
        self._sequence = self._model.generate(self._nb_chords)
        self._midi_notes = [[note_name_to_number(note) for note in Chord(
            chord).components_with_pitch(root_pitch=4)] for chord in self._sequence]
        print(self._midi_notes)

    # This method will be triggered when a "search" message is received on the second inlet

    def search_1(self, *args):
        # DONT USE outlet 0, it is the rightmost outlet and it's used by pyext.
        # self._outlet(0, "whaa")   # DONT.

        nb_notes = min(self._outlets, len(
            self._midi_notes[self._current_chord]))

        for i in range(1, nb_notes + 1):
            note = self._midi_notes[self._current_chord][i - 1]
            print(note)
            self._outlet(i, note)

        if nb_notes != self._outlets:
            self._outlet(self._outlets, 0)  # sssh no one will hear it

        self._current_chord += 1
        self._current_chord = self._current_chord % self._nb_chords


##########################################################################


# This class represents another pd object called generator_pd
# [pyext my_pd_objects.generator_pd]
class generator_pd(pyext._class):
    _inlets = 2
    _outlets = 1

    # When a load message is received, create an instance of Generator
    def load_2(self, *args):
        self.generator = Generator("the_bum")

    def generate_1(self, *args):
        notes = self.generator.generate()
        self._outlet(1, notes)
