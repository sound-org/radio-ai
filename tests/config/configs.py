
# Sample data for testing
valid_speaker_config = {
    "name": "Speaker1",
    "voice": "Voice1",
    "TTS": "ELEVENLABS",
    "personality": "Friendly"
}

valid_channel_config = {
    "id": 1,
    "name": "Channel1",
    "description": "This is channel 1",
    "music_theme": "Rock",
    "speaker": valid_speaker_config
}

valid_radio_config = {
    "channels": [valid_channel_config]
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