from enum import Enum


class Mode(Enum):
    VLC_CLOUD = 1  # Use the legacy system, with VLC and direct Google Could TTS, will be phased out over time  # noqa: E501
    SPEAKER = 2  # Use the newer system, utilizing Speaker.bot, will be phased out over time  # noqa: E501
    STREAMER = 3  # Use the newest system, utilizing both Speaker and Streamer bot for better contextuality and YouTube Support  # noqa: E501
