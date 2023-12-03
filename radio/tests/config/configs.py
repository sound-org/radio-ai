# Sample data for testing


incomplete_speaker_config = {
    "name": "Speaker1"
    # Missing other fields
}

incomplete_channel_config = {
    "id": 1,
    "name": "Channel1"
    # Missing other fields
}


invalid_music_config_missing_output_path_for_custom_generator = {
    "music_generators": [
        {
            "type": "ai",
            "theme": "theme1",
            "output_dir": "channels/1/music/ai",
            "num_tracks_to_combine": 2,
        },
        {
            "type": "algorithmic",
            "output_dir": "channels/1/music/algorithmic",
            "num_tracks_to_combine": 2,
        },
        {
            "type": "custom",
            # Missing output_dir
        },
    ]
}

invalid_music_generator_unknown_type = {
    "music_generators": [
        {
            "type": "ai",
            "theme": "theme1",
            "output_dir": "channels/1/music/ai",
            "num_tracks_to_combine": 2,
        },
        {
            "type": "algorithmic",
            "output_dir": "channels/1/music/algorithmic",
            "num_tracks_to_combine": 2,
        },
        {
            "type": "unknown",
            "output_dir": "channels/1/music/custom",
            "num_tracks_to_combine": 2,
        },
    ]
}

valid_muisc_config_with_multiple_ai_generators = {
    "music_generators": [
        {
            "type": "ai",
            "theme": "theme1",
            "output_dir": "channels/1/music/ai",
            "num_tracks_to_combine": 2,
        },
        {
            "type": "ai",
            "theme": "theme2",
            "output_dir": "channels/1/music/ai",
            "num_tracks_to_combine": 2,
        },
        {
            "type": "algorithmic",
            "output_dir": "channels/1/music/algorithmic",
            "num_tracks_to_combine": 2,
        },
        {
            "type": "custom",
            "output_dir": "channels/1/music/custom",
            "num_tracks_to_combine": 2,
        },
    ]
}

valid_music_config_with_single_ai_generator = {
    "music_generators": [
        {
            "type": "ai",
            "theme": "theme1",
            "output_dir": "channels/1/music/ai",
            "num_tracks_to_combine": 2,
        },
    ]
}

valid_ai_generator_config = {
    "type": "ai",
    "theme": "theme1",
    "output_dir": "channels/1/music/ai",
    "num_tracks_to_combine": 2,
}

valid_algorithmic_generator_config = {
    "type": "algorithmic",
    "output_dir": "channels/1/music/algorithmic",
    "num_tracks_to_combine": 2,
}

valid_speaker_config = {
    "name": "Bob",
    "TTS": "PYTTSX3",
    "voice": "english",
    "personality": "You are and radio DJ, you love good hard rock music, the harder the better music, you are definitely crazy",
    "output_dir": "channels/test/speaker",
}

valid_music_config = {
    "music_generators": [
        {
            "type": "ai",
            "theme": "theme1",
            "output_dir": "channels/1/music/ai",
            "num_tracks_to_combine": 2,
        },
        {
            "type": "algorithmic",
            "output_dir": "channels/1/music/algorithmic",
            "num_tracks_to_combine": 2,
        },
        {
            "type": "custom",
            "output_dir": "channels/1/music/custom",
            "num_tracks_to_combine": 2,
        },
    ]
}

valid_channel_config = {
    "id": 1,
    "name": "Channel1",
    "description": "This is channel 1",
    "broadcast_output_dir": "broadcast_output_dir",
    "streaming_output_dir": "streaming_output_dir",
    "speaker": valid_speaker_config,
    "music": {
        "music_generators": [valid_algorithmic_generator_config],
    },
}
valid_radio_config = {"channels": [valid_channel_config]}
