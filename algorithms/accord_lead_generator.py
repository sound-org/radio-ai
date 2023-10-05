from mingus.core import chords
import random

class Generator:

    def __create_diatonic_map(key:str) -> list[str]:
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
            chords.vii(key)[0]
            ]
    
    def apply_addons(diatonic_chords:list[str], addon:int=0) -> None:
        
        switch = {
            3: ["M","m","m","M","M","m","m"],
            7: ["M7","m7","m7","M7","M7","m7","m7"],
            6: ["M6","m6","m6","M6","M6","m6","m6"],
            9: ["M9","m9","m9","M9","M9","m9","m9"],
        }

        suffixes = switch.get(addon, ["","m","m","","","m","m"])

        for index, suffix in enumerate(suffixes):
            diatonic_chords[index]+=suffix        
        

    def __get_from_progression(key:str, progression:list[int], addon:int) -> list[str]:
        diatonic_map = Generator.__create_diatonic_map(key)
        Generator.apply_addons(diatonic_chords=diatonic_map, addon=addon)
        return [diatonic_map[index-1] for index in progression]

    def get_axis_progression_chords(key:str, addon:int=0) -> list[str]:
        """"
        Generates simple Axis progression for said key:

        Chords:
        | I | V | vi | IV |
        """
        return Generator.__get_from_progression(key=key, progression=[1,5,6,4], addon=addon)
    
    def get_other_axis_progression_chords(key:str, addon:int=0) -> list[str]:
        """"
        Generates simple OTHER Axis progression for said key:

        Chords:
        | vi | IV | I | V |
        """
        
        return Generator.__get_from_progression(key=key, progression=[6,4,1,5], addon=addon)
    
    def get_doo_wop_progression_chords(key:str, addon:int=0) -> list[str]:
        """"
        Generates simple Doo-wop progression for said key:

        Chords:
        | I | vi | IV | V |
        """
        
        return Generator.__get_from_progression(key=key, progression=[1,6,4,5], addon=addon)

    def get_blue_moon_progression_chords(key:str, addon:int=0) -> list[str]:
        """"
        Generates simple Blue Moon progression for said key:

        Chords:
        | I | vi | ii | V |
        """
        
        return Generator.__get_from_progression(key=key, progression=[1,6,2,5], addon=addon)

    def get_major_scale_vamp_progression_chords(key:str, addon:int=0) -> list[str]:
        """"
        Generates simple Major Scale Vamp progression for said key:

        Chords:
        | I | V | IV | V |
        """
        
        return Generator.__get_from_progression(key=key, progression=[1,5,4,5], addon=addon)
    
    def get_random_simple_progression_chords(key:str, addon:int=0) -> list[str]:
        """
        Generates random simple chord progression

        Rules:
        1. Use only 4 measures of chords (4 whole notes for whole piece)
        2. Start with 1st chord
        3. Last chords should be 4th or 5th 
        4. Do not use 7th cord
        """
        middle = [1,2,3,4,5,6]
        ending = [4,5]
        progression = [1, random.choice(middle), random.choice(middle), random.choice(ending)]
        print(progression)

        return Generator.__get_from_progression(key=key, progression=progression, addon=addon)

#TODO : Add andalusian chord progressions
