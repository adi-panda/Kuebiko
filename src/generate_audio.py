import os

from vlc import EventType, MediaPlayer  # type: ignore


def _audio_play_finished_event(media: MediaPlayer, audio_file_path: str):
    def audio_play_finished(_):
        print("------------------------------------------------------")
        media.stop()
        media.release()
        os.remove(audio_file_path)

    return audio_play_finished


def play_audio(audio_filename: str, audio_content: bytes | None):
    if audio_content is None:
        return
    # The response's audio_content is binary.
    with open(audio_filename, "wb") as out:
        out.write(audio_content)

    dir_path = os.environ["BASE_DIR_PATH"]
    audio_file_path = f"{dir_path}/{audio_filename}"
    media = MediaPlayer(audio_file_path)
    # Added event_manager for aviod end error
    event_manager = media.event_manager()
    event_manager.event_attach(
        EventType.MediaPlayerEndReached,
        _audio_play_finished_event(media, audio_file_path),
    )
    media.play()
