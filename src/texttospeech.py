import os
from typing import List, Tuple

import vlc
from google.cloud import texttospeech_v1beta1 as texttospeech
from google.cloud.texttospeech_v1beta1.types.cloud_tts import (
    SynthesizeSpeechRequest
)

from . import credentials
from .subtitle import generate_subtitle_file
from .utils import words_length


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials.GOOGLE_JSON_PATH


def _audio_play_finished_event(media: vlc.MediaPlayer, audio_file_path: str):
    def audio_play_finished(_):
        print("------------------------------------------------------")
        media.stop()
        media.release()
        os.remove(audio_file_path)

    return audio_play_finished


def _play_audio(audio_filename: str):
    dir_path = os.environ["BASE_DIR_PATH"]
    audio_file_path = f"{dir_path}/{audio_filename}"
    media = vlc.MediaPlayer(audio_file_path)
    event_manager = media.event_manager()
    event_manager.event_attach(
        vlc.EventType.MediaPlayerEndReached,
        _audio_play_finished_event(media, audio_file_path),
    )
    media.play()


def _config_texttospeech_request(
    text_to_transform_to_audio: str,
) -> Tuple[SynthesizeSpeechRequest, List[str]]:
    ssml_text = "<speak>"
    response_counter = 0
    mark_array: List[str] = []
    for s in text_to_transform_to_audio.split(" "):
        ssml_text += f'<mark name="{response_counter}"/>{s}'
        mark_array.append(s)
        response_counter += 1
    ssml_text += "</speak>"

    input_text = texttospeech.SynthesisInput(ssml=ssml_text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="es-US",
        name="es-US-Neural2-A",
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        pitch=4,
        speaking_rate=1.05,
    )

    return (
        {
            "input": input_text,
            "voice": voice,
            "audio_config": audio_config,
            "enable_time_pointing": ["SSML_MARK"],
        },
        mark_array,
    )


def generate_audio_and_subtitle(
    user_question: str, bot_response: str, audio_filename="audio.mp3"
):
    text_to_transform_to_audio = user_question + "? " + bot_response

    print(f"Character length = {len(text_to_transform_to_audio)}")
    print(f"Words length = {words_length(text_to_transform_to_audio)}")

    client = texttospeech.TextToSpeechClient()
    request, mark_array = _config_texttospeech_request(
        text_to_transform_to_audio
    )
    response = client.synthesize_speech(request=request)

    # The response's audio_content is binary.
    with open(audio_filename, "wb") as out:
        out.write(response.audio_content)

    _play_audio(audio_filename)
    generate_subtitle_file(response.timepoints, mark_array)
