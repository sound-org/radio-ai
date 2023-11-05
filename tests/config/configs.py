# Sample data for testing
valid_speaker_config = {
    "name": "Speaker1",
    "voice": "Voice1",
    "TTS": "ELEVENLABS",
    "personality": "Friendly",
    "output_dir": "output_dir",
}

valid_channel_config = {
    "id": 1,
    "name": "Channel1",
    "description": "This is channel 1",
    "broadcast_output_dir": "broadcast_output_dir",
    "streaming_output_dir": "streaming_output_dir",
    "speaker": valid_speaker_config,
    "music": {"theme": "Theme1", "output_dir": "output_dir"},
}

valid_radio_config = {"channels": [valid_channel_config]}

incomplete_speaker_config = {
    "name": "Speaker1"
    # Missing other fields
}

incomplete_channel_config = {
    "id": 1,
    "name": "Channel1"
    # Missing other fields
}
