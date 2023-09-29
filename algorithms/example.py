from midiutil import MIDIFile
from utils import *
from mingus.core import chords
from accord_lead_generator import Generator

# Same program as the one in "tutorial" folder using own classes with custom generated melody

def toNote(pitch:str) -> Note:
    note = Note()
    note.pitch = pitch
    note.duration = Duration.Quarter
    return note

chord_progression = Generator.get_random_simple_progression_chords(key='A', addon=7)
notes_melody = Melody.chords_to_notes(chord_progression)
notes = [toNote(n) for n in notes_melody]

file = MIDIFile(1)
file.addTempo(track=0, time=0, tempo=120)

melody = Melody()

melody.notes = notes

melody.notes_to_midi(file)

save_midi_file(file, "test2")