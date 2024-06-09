from .generate_audio import play_audio
from .openai import openai


def generate_audio_and_subtitle(
    user_question: str, bot_response: str, audio_filename="audio.mp3"
):
    text_to_transform_to_audio = user_question + "? " + bot_response
    response = openai.audio.speech.create(
        model="tts-1", voice="nova", input=text_to_transform_to_audio
    )
    play_audio(audio_filename, response.content)
