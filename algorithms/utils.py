from mingus.core import chords
from midiutil import MIDIFile

NOTES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)

errors = {
    'notes': 'Bad input :(\n',
    'length': 'Incorrect length of the input list\n'
}

def __swap_accidentals(note):
    if note == 'Db':
        return 'C#'
    if note == 'D#':
        return 'Eb'
    if note == 'E#':
        return 'F'
    if note == 'Gb':
        return 'F#'
    if note == 'G#':
        return 'Ab'
    if note == 'A#':
        return 'Bb'
    if note == 'B#':
        return 'C'
    return note

def __note_to_number(note: str, octave: int) -> int:
    note = __swap_accidentals(note)
    assert note in NOTES, errors['notes']
    assert octave in OCTAVES, errors['notes']

    note = NOTES.index(note)
    note += (NOTES_IN_OCTAVE * octave)

    assert 0 <= note <= 127, errors['notes']
    return note

def __get_time_offset(notes_duration: list[int], index: int) -> int:
    return sum(notes_duration[:index])

def chords_to_notes(chord_progression: list[str], onlyFirst=False) -> list[str]:
    """Encode list of chords as notes"""

    array_of_notes = []
    for chord in chord_progression:
        if onlyFirst:
            array_of_notes.append(chords.from_shorthand(chord)[0])
        else:
            array_of_notes.extend(chords.from_shorthand(chord))
    return array_of_notes

def notes_to_midi(file: MIDIFile, array_of_notes: list[str], notes_duration: list[int], octave=4, start_time=0, track=0, channel=0, volume=100) -> None:
    """Save the sequence of notes in the MIDI file"""
    
    assert len(array_of_notes) == len(notes_duration), errors['length']

    array_of_notes_numbers = []
    for note in array_of_notes:
        array_of_notes_numbers.append(__note_to_number(note, octave=octave))

    for i, pitch in enumerate(array_of_notes_numbers):
        file.addNote(track, channel, pitch, start_time + __get_time_offset(notes_duration, i), notes_duration[i], volume)

def save_midi_file(file: MIDIFile, name: str, path="out/") -> None:
    """Save the MIDI file on disk"""

    with open(path + name + ".mid", "wb") as output_file:
        file.writeFile(output_file)

