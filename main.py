import os

from src.enums import Mode

os.environ["BASE_DIR_PATH"] = os.getcwd()

mode = Mode.VLC_CLOUD  # Recommended Mode


if __name__ == "__main__":

    if mode == Mode.VLC_CLOUD:
        from src.twitchbot import Bot

        bot = Bot()
        bot.run()

    elif mode == Mode.SPEAKER:
        from src.twitchbot import Bot

        bot = Bot(speaker_bot=True)
        bot.run()

    elif mode == Mode.STREAMER:
        import threading

        from src.logger import Logger
        from src.speaker_bot_based import Bot as SpeakerBot
        from src.speaker_bot_based import QueueConsumer

        logger = Logger(
            console_log=True,
            file_logging=True,
            file_URI="logs/log.txt",
            override=True,
        )

        consumer = QueueConsumer(logger=logger, verbose=True, answer_rate=20)
        bot = SpeakerBot(consumer, logger)
        process = threading.Thread(target=consumer.run)
        process.start()

        bot.run()
        process.join()
