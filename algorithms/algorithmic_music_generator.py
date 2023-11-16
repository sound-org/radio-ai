import random

from midiutil import MIDIFile
import utils as utils
from algorithms.accord_lead_generator import Generator


def create_random_melody(key, addon, no_of_chords):
    chord_progression = Generator.get_random_simple_progression_chords(key=key, addon=addon, chords_num=no_of_chords)
    return utils.chords_to_notes(chord_progression)


def main():
    keys = ["C", "D", "E", "F", "G", "A", "B"]
    addon = [0, 3, 6, 7, 9]
    primary_key = random.choice(keys)
    secondary_key = random.choice(keys)
    base_len: int = 32

    # main line --> quarter notes
    notes_melody = create_random_melody(primary_key, 0, no_of_chords=base_len)
    print(notes_melody)

    # bass line --> whole notes
    notes_bass = create_random_melody(secondary_key, 0, no_of_chords=base_len//4)
    print(notes_bass)

    # additional line --> eight notes with offset
    additional_notes = create_random_melody("C", 0, no_of_chords=base_len*2*3//4)
    print(additional_notes)

    myMIDI = MIDIFile(1)
    myMIDI.addTempo(track=0, time=0, tempo=60)

    utils.notes_to_midi(file=myMIDI, array_of_notes=notes_melody, octave=4, track=0,
                        notes_duration=[1 for _ in notes_melody])
    utils.notes_to_midi(file=myMIDI, array_of_notes=notes_bass, octave=2, track=0,
                        notes_duration=[4 for _ in notes_bass])
    utils.notes_to_midi(file=myMIDI, array_of_notes=additional_notes, octave=5, track=0,
                        notes_duration=[0.5 for _ in additional_notes], start_time=len(notes_melody)/8)

    utils.save_midi_file(myMIDI, "algorithmic-music")


if __name__ == "__main__":
    main()
