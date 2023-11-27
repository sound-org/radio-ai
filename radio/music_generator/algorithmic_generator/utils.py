from enum import Enum

from midiutil import MIDIFile
from mingus.core import chords

errors = {"notes": "Bad input :(\n", "length": "Incorrect length of the input list\n"}

NOTES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)


def __swap_accidentals(note):
    if note == "Db":
        return "C#"
    if note == "D#":
        return "Eb"
    if note == "E#":
        return "F"
    if note == "Gb":
        return "F#"
    if note == "G#":
        return "Ab"
    if note == "A#":
        return "Bb"
    if note == "B#":
        return "C"
    return note


class Instruments:
    class Piano(Enum):
        Acoustic_Grand = 0
        Bright_Acoustic = 1
        Electric_Grand = 2
        Honkytonk = 3
        Rhodes = 4
        Chorused = 5
        Harpsichord = 6
        Clavinet = 7

    class Chromatic_Percussion(Enum):
        Celesta = 8
        Glockenspiel = 9
        Music_box = 10
        Vibraphone = 11
        Marimba = 12
        Xylophone = 13
        Tubular_Bells = 14
        Dulcimer = 15

    class Organ(Enum):
        Hammond = 16
        Percussive = 17
        Rock = 18
        Church = 19
        Reed = 20
        Accordion = 21
        Harmonica = 22
        Tango_Accordion = 23

    class Guitar(Enum):
        Acoustic_Nylon = 24
        Acoustic_Steel = 25
        Electric_Jazz = 26
        Electric_Clean = 27
        Electric_Muted = 28
        Overdriven = 29
        Distortion = 30
        Harmonics = 31

    class Bass(Enum):
        Acoustic = 32
        Electric_Finger = 33
        Electric_Pick = 34
        Fretless = 35
        Slap_1 = 36
        Slap_2 = 37
        Synth_1 = 38
        Synth_2 = 39

    class Strings(Enum):
        Violin = 40
        Viola = 41
        Cello = 42
        Contrabass = 43
        Tremolo = 44
        Pizzicato = 45
        Orchestral_Harp = 46
        Timpani = 47

    class Ensemble(Enum):
        String_1 = 48
        String_Ensemble_2 = 49
        Synth_1 = 50
        Synth_2 = 51
        Choir_Aahs = 52
        Voice_Oohs = 53
        Synth_Voice = 54
        Orchestra_Hit = 55

    class Brass(Enum):
        Trumpet = 56
        Trombone = 57
        Tuba = 58
        Muted_Trumpet = 59
        French_Horn = 60
        Brass_Section = 61
        Synth_1 = 62
        Synth_2 = 63

    class Reed(Enum):
        Soprano_Sax = 64
        Alto_Sax = 65
        Tenor_Sax = 66
        Baritone_Sax = 67
        Oboe = 68
        English_Horne = 69
        Bassoon = 70
        Clarinet = 71

    class Pipe(Enum):
        Piccolo = 72
        Flute = 73
        Recorder = 74
        Pan_Flute = 75
        Bottle_Blow = 76
        Shakuhachi = 77
        Whistle = 78
        Ocarina = 79

    class Synth_Lead(Enum):
        Square = 80
        Sawtooth = 81
        Calliope_Lead = 82
        Chiffer_Lead = 83
        Charang = 84
        Voice = 85
        Fifths = 86
        Brass_And_Lead = 87

    class Synth_Pad(Enum):
        New_Age = 88
        Warm = 89
        Polysynth = 90
        Choir = 91
        Bowed = 92
        Metallic = 93
        Halo = 94
        Sweep = 95

    class FX(Enum):
        Rain = 96
        Soundtrack = 97
        Crystal = 98
        Atmosphhere = 99
        Brightmess = 100
        Goblins = 101
        Echoes = 102
        Sci_Fi = 103

    class Ethnic(Enum):
        Sitar = 104
        Banjo = 105
        Shamisen = 106
        Koto = 107
        Kalimba = 108
        Bagpipe = 109
        Fiddle = 110
        Shana = 111

    class Percussive(Enum):
        Tinkle_Bell = 112
        Agogo = 113
        Steel_Drums = 114
        Woodblock = 115
        Taiko_Drum = 116
        Melodic_Tom = 117
        Synth_Drum = 118
        Reverse_Cymbal = 119

    class Sound_Effects(Enum):
        Guitar_Fret_Noise = 120
        Breath_Noise = 121
        Seashore = 122
        Bird_Tweet = 123
        Telephone_Ring = 124
        Helicopter = 125
        Applause = 126
        Gunshot = 127


class Duration(Enum):
    # Enum represents length of each note in beats
    Whole = 4
    Half = 2
    Quarter = 1
    Eighth = 0.5
    Sixteenth = 0.25


class Note:
    NOTES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    OCTAVES = list(range(11))
    NOTES_IN_OCTAVE = len(NOTES)

    def __init__(self) -> None:
        self.pitch = ""
        self.octave = 4
        self.duration = Duration.Whole

    def __swap_accidentals(note: str) -> str:
        if note == "Db":
            return "C#"
        if note == "D#":
            return "Eb"
        if note == "E#":
            return "F"
        if note == "Gb":
            return "F#"
        if note == "G#":
            return "Ab"
        if note == "A#":
            return "Bb"
        if note == "B#":
            return "C"
        return note

    def note_to_number(n) -> int:
        """Returns numeric value of note as specified in midi format. Pauses (empty) notes are treated as -1"""

        if n.pitch == "":
            # We treat empty pitch as pause
            return -1

        note = Note.__swap_accidentals(n.pitch)
        assert note in Note.NOTES, errors["notes"]
        assert n.octave in Note.OCTAVES, errors["notes"]

        note = Note.NOTES.index(note)
        note += Note.NOTES_IN_OCTAVE * n.octave

        assert 0 <= note <= 127, errors["notes"]
        return note


class Melody:
    def __init__(self) -> None:
        self.notes = []
        self.track = 0
        self.channel = 0
        self.volume = 100
        self.start_time = 0

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

    def notes_to_midi(self, file: MIDIFile) -> None:
        """Save the sequence of notes in the MIDI file"""

        array_of_notes_numbers = []
        notes_duration = [note.duration.value for note in self.notes]
        for note in self.notes:
            array_of_notes_numbers.append(Note.note_to_number(note))

        for i, pitch in enumerate(array_of_notes_numbers):
            if pitch > -1:
                # we skip in adding pause as midi does not have such concept
                file.addNote(
                    self.track,
                    self.channel,
                    pitch,
                    self.start_time + Melody.__get_time_offset(notes_duration, i),
                    self.notes[i].duration.value,
                    self.volume,
                )


def chords_to_notes(chord_progression: list[str], onlyFirst=False) -> list[str]:
    """Encode list of chords as notes"""

    array_of_notes = []
    for chord in chord_progression:
        if onlyFirst:
            array_of_notes.append(chords.from_shorthand(chord)[0])
        else:
            array_of_notes.extend(chords.from_shorthand(chord))
    return array_of_notes


def __note_to_number(note: str, octave: int) -> int:
    note = __swap_accidentals(note)
    assert note in NOTES, errors["notes"]
    assert octave in OCTAVES, errors["notes"]

    note = NOTES.index(note)
    note += NOTES_IN_OCTAVE * octave

    assert 0 <= note <= 127, errors["notes"]
    return note


def __get_time_offset(notes_duration: list[int], index: int) -> int:
    return sum(notes_duration[:index])


def notes_to_midi(
    file: MIDIFile,
    array_of_notes: list[str],
    notes_duration: list[float],
    octave=4,
    start_time=0,
    track=0,
    channel=0,
    volume=100,
) -> None:
    """Save the sequence of notes in the MIDI file"""

    assert len(array_of_notes) == len(notes_duration), errors["length"]

    array_of_notes_numbers = []
    for note in array_of_notes:
        array_of_notes_numbers.append(__note_to_number(note, octave=octave))

    for i, pitch in enumerate(array_of_notes_numbers):
        file.addNote(
            track,
            channel,
            pitch,
            start_time + __get_time_offset(notes_duration, i),
            notes_duration[i],
            volume,
        )


import os
import subprocess


def save_midi_as_mp3(
    midi_file: MIDIFile, midi_filename: str, mp3_filename: str
) -> None:
    """Convert the MIDI file to an MP3 file and save on disk, then delete the MIDI file."""
    soundfont_path = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
    with open(midi_filename, "wb") as output_file:
        midi_file.writeFile(output_file)

    # fluidsynth_command = f"fluidsynth -ni {soundfont_path} {midi_filename} -F - | ffmpeg -f s32le -i - {mp3_filename}"
    fluidsynth_command = f"fluidsynth -ni {soundfont_path} {midi_filename} -F temp.wav"
    ffmpeg_command = f"ffmpeg -i temp.wav {mp3_filename}"

    subprocess.run(fluidsynth_command, shell=True, check=True)
    subprocess.run(ffmpeg_command, shell=True, check=True)
    os.remove(midi_filename)
    os.remove("temp.wav")
