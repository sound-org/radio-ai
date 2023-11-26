# Sample data for testing
valid_speaker_config = {
    "name": "Speaker1",
    "voice": "Voice1",
    "TTS": "ELEVENLABS",
    "personality": "Friendly",
    "output_dir": "output_dir",
}

incomplete_speaker_config = {
    "name": "Speaker1"
    # Missing other fields
}

incomplete_channel_config = {
    "id": 1,
    "name": "Channel1"
    # Missing other fields
}


valid_music_config = {
    "music_generators": [
        {
            "type": "ai",
            "theme": "theme1",
            "output_dir": "channels/1/music/ai",
        },
        {
            "type": "algorithmic",
            "output_dir": "channels/1/music/algorithmic",
        },
        {
            "type": "custom",
            "output_dir": "channels/1/music/custom",
        },
    ]
}

invalid_music_config_missing_output_path_for_custom_generator = {
    "music_generators": [
        {
            "type": "ai",
            "theme": "theme1",
            "output_dir": "channels/1/music/ai",
        },
        {
            "type": "algorithmic",
            "output_dir": "channels/1/music/algorithmic",
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
        },
        {
            "type": "algorithmic",
            "output_dir": "channels/1/music/algorithmic",
        },
        {
            "type": "unknown",
            "output_dir": "channels/1/music/custom",
        },
    ]
}

valid_muisc_config_with_multiple_ai_generators = {
    "music_generators": [
        {
            "type": "ai",
            "theme": "theme1",
            "output_dir": "channels/1/music/ai",
        },
        {
            "type": "ai",
            "theme": "theme2",
            "output_dir": "channels/1/music/ai",
        },
        {
            "type": "algorithmic",
            "output_dir": "channels/1/music/algorithmic",
        },
        {
            "type": "custom",
            "output_dir": "channels/1/music/custom",
        },
    ]
}

valid_music_config_with_single_ai_generator = {
    "music_generators": [
        {
            "type": "ai",
            "theme": "theme1",
            "output_dir": "channels/1/music/ai",
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
    "music": valid_music_config,  # Updated music field
}
valid_radio_config = {"channels": [valid_channel_config]}
