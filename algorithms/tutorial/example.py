from midiutil import MIDIFile
import utils

## tutorial example
chord_progression = ["Cmaj7", "Cmaj7", "Fmaj7", "Gdom7"]
notes_melody = utils.chords_to_notes(chord_progression)
notes_bass = utils.chords_to_notes(chord_progression, onlyFirst=True)

myMIDI = MIDIFile(2)
myMIDI.addTempo(track=0, time=0, tempo=120)
myMIDI.addTempo(track=1, time=0, tempo=120)

utils.notes_to_midi(file=myMIDI, array_of_notes=notes_melody, octave=4, track=0, notes_duration=[1 for _ in notes_melody])
utils.notes_to_midi(file=myMIDI, array_of_notes=notes_bass, octave=3, track=1, notes_duration=[4 for _ in notes_bass])

utils.save_midi_file(myMIDI, "example")