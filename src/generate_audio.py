import os

import vlc


def _audio_play_finished_event(media: vlc.MediaPlayer, audio_file_path: str):
    def audio_play_finished(_):
        print("------------------------------------------------------")
        media.stop()
        media.release()
        os.remove(audio_file_path)

    return audio_play_finished


def play_audio(audio_filename: str, audio_content: str):
    # The response's audio_content is binary.
    with open(audio_filename, "wb") as out:
        out.write(audio_content)

    dir_path = os.environ["BASE_DIR_PATH"]
    audio_file_path = f"{dir_path}/{audio_filename}"
    media = vlc.MediaPlayer(audio_file_path)
    event_manager = media.event_manager()
    event_manager.event_attach(
        vlc.EventType.MediaPlayerEndReached,
        _audio_play_finished_event(media, audio_file_path),
    )
    media.play()
