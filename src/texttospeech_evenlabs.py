import requests

from .credentials import ELEVENLABS_APIKEY, ELEVENLABS_VOICEID
from .generate_audio import play_audio


def get_speech_by_text(
    user_question: str, bot_response: str, audio_filename="audio.mp3"
):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICEID}"

    querystring = {
        "optimize_streaming_latency": "2",
        "output_format": "mp3_44100_32",
    }

    text_to_transform_to_audio = user_question + "? " + bot_response

    payload = {
        "model_id": "eleven_multilingual_v2",
        "text": text_to_transform_to_audio,
        "voice_settings": {
            "similarity_boost": 0.1,
            "stability": 1,
            "style": 0,
            "use_speaker_boost": True,
        },
    }
    headers = {
        "xi-api-key": ELEVENLABS_APIKEY,
        "Content-Type": "application/json",
    }

    response = requests.request(
        "POST", url, json=payload, headers=headers, params=querystring
    )
    play_audio(audio_filename, response._content)
