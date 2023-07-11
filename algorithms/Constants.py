from enum import Enum

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
