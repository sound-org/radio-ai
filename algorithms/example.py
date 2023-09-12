from midiutil import MIDIFile
from utils import *

# Same program as the one in "tutorial" folder using own classes

def toNote(pitch:str) -> Note:
    note = Note()
    note.pitch = pitch
    note.duration = Duration.Quarter
    return note

chord_progression = ["Cmaj7", "Cmaj7", "Fmaj7", "Gdom7"]
notes_melody = notes_melody = Melody.chords_to_notes(chord_progression)
notes = [toNote(n) for n in notes_melody]

file = MIDIFile(1)
file.addTempo(track=0, time=0, tempo=120)

melody = Melody()

melody.notes = notes

melody.notes_to_midi(file)

save_midi_file(file, "test2")