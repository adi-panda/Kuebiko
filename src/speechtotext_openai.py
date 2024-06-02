import os
from .openai import openai


def generate_text_by_audio(audio_filename="audio.mp3"):
    dir_path = os.environ["BASE_DIR_PATH"]
    audio_file_path = f"{dir_path}/{audio_filename}"
    audio_file = open(audio_file_path, "rb")
    transcription = openai.audio.transcriptions.create(
        model="whisper-1", file=audio_file
    )
    print("transcripcion = " + transcription.text)
