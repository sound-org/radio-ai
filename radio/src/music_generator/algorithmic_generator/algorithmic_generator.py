import logging
import os
import random
import time

from midiutil import MIDIFile
from mingus.core import chords

from src.config.music_config import AlgorithmicMusicConfig

from ..abstract_generator import AbstractMusicGenerator
from . import utils

logger = logging.getLogger(__name__)


class AlgorithmicGenerator(AbstractMusicGenerator):
    def __init__(self, config: AlgorithmicMusicConfig):
        super().__init__(config)

    def generate(self, n: int):
        logger.info("Generating %d songs...", n)
        for _ in range(n):
            self._generate_music()

    def _generate_music(self):
        keys = ["C", "D", "E", "F", "G", "A", "B"]
        addon = [0, 3, 6, 7, 9]
        primary_key = random.choice(keys)
        secondary_key = random.choice(keys)
        base_len: int = 32

        # main line --> quarter notes
        notes_melody = self._create_random_melody(primary_key, 0, no_of_chords=base_len)
        print(notes_melody)

        # bass line --> whole notes
        notes_bass = self._create_random_melody(
            secondary_key, 0, no_of_chords=base_len // 4
        )
        print(notes_bass)

        # additional line --> eight notes with offset
        additional_notes = self._create_random_melody(
            "C", 0, no_of_chords=base_len * 2 * 3 // 4
        )
        print(additional_notes)

        myMIDI = MIDIFile(1)
        myMIDI.addTempo(track=0, time=0, tempo=60)

        utils.notes_to_midi(
            file=myMIDI,
            array_of_notes=notes_melody,
            octave=4,
            track=0,
            notes_duration=[1 for _ in notes_melody],
        )
        utils.notes_to_midi(
            file=myMIDI,
            array_of_notes=notes_bass,
            octave=2,
            track=0,
            notes_duration=[4 for _ in notes_bass],
        )
        utils.notes_to_midi(
            file=myMIDI,
            array_of_notes=additional_notes,
            octave=5,
            track=0,
            notes_duration=[0.5 for _ in additional_notes],
            start_time=len(notes_melody) / 8,
        )

        name = str(
            int(time.time() * 100)
        )  # take first two decimal place, so we can have 100 songs per second
        midi_file = os.path.join(self.output_dir, name + ".midi")
        mp3_file = os.path.join(self.output_dir, name + ".mp3")
        utils.save_midi_as_mp3(myMIDI, midi_file, mp3_file)

    def _create_diatonic_map(self, key: str) -> list[str]:
        """
        Returns array of 7 cords in a diatonic scale with given key as tonic.
        """

        return [
            chords.I(key)[0],
            chords.ii(key)[0],
            chords.iii(key)[0],
            chords.IV(key)[0],
            chords.V(key)[0],
            chords.vi(key)[0],
            chords.vii(key)[0],
        ]

    def _apply_addons(self, diatonic_chords: list[str], addon: int = 0) -> None:
        switch = {
            3: ["M", "m", "m", "M", "M", "m", "m"],
            7: ["M7", "m7", "m7", "M7", "M7", "m7", "m7"],
            6: ["M6", "m6", "m6", "M6", "M6", "m6", "m6"],
            9: ["M9", "m9", "m9", "M9", "M9", "m9", "m9"],
        }

        suffixes = switch.get(addon, ["", "m", "m", "", "", "m", "m"])

        for index, suffix in enumerate(suffixes):
            diatonic_chords[index] += suffix

    def _get_from_progression(
        self, key: str, progression: list[int], addon: int
    ) -> list[str]:
        diatonic_map = self._create_diatonic_map(key)
        self._apply_addons(diatonic_chords=diatonic_map, addon=addon)
        return [diatonic_map[index - 1] for index in progression]

    def _get_axis_progression_chords(self, key: str, addon: int = 0) -> list[str]:
        """ "
        Generates simple Axis progression for said key:

        Chords:
        | I | V | vi | IV |
        """
        return self._get_from_progression(
            key=key, progression=[1, 5, 6, 4], addon=addon
        )

    def _get_other_axis_progression_chords(self, key: str, addon: int = 0) -> list[str]:
        """ "
        Generates simple OTHER Axis progression for said key:

        Chords:
        | vi | IV | I | V |
        """

        return self._get_from_progression(
            key=key, progression=[6, 4, 1, 5], addon=addon
        )

    def _get_doo_wop_progression_chords(self, key: str, addon: int = 0) -> list[str]:
        """ "
        Generates simple Doo-wop progression for said key:

        Chords:
        | I | vi | IV | V |
        """

        return self._get_from_progression(
            key=key, progression=[1, 6, 4, 5], addon=addon
        )

    def _get_blue_moon_progression_chords(self, key: str, addon: int = 0) -> list[str]:
        """ "
        Generates simple Blue Moon progression for said key:

        Chords:
        | I | vi | ii | V |
        """

        return self._get_from_progression(
            key=key, progression=[1, 6, 2, 5], addon=addon
        )

    def _get_major_scale_vamp_progression_chords(
        self, key: str, addon: int = 0
    ) -> list[str]:
        """ "
        Generates simple Major Scale Vamp progression for said key:

        Chords:
        | I | V | IV | V |
        """

        return self._get_from_progression(
            key=key, progression=[1, 5, 4, 5], addon=addon
        )

    def _get_random_simple_progression_chords(
        self, key: str, addon: int = 0, chords_num: int = 4
    ) -> list[str]:
        """
        Generates random simple chord progression

        Rules:
        1. Use only 4 measures of chords (4 whole notes for whole piece)
        2. Start with 1st chord
        3. Last chords should be 4th or 5th
        4. Do not use 7th cord
        """
        middle = [1, 2, 3, 4, 5, 6]
        ending = [4, 5]
        progression = (
            [1]
            + [random.choice(middle) for _ in range(chords_num - 2)]
            + [random.choice(ending)]
        )
        print(progression)

        return self._get_from_progression(key=key, progression=progression, addon=addon)

    def _create_random_melody(self, key, addon, no_of_chords):
        chord_progression = self._get_random_simple_progression_chords(
            key=key, addon=addon, chords_num=no_of_chords
        )
        return utils.chords_to_notes(chord_progression)  # noqa: F821
