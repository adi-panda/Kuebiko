from enum import Enum
from creds import *




class Mode(Enum):
    VLC_CLOUD = 1 # Use the legacy system, with VLC and direct Google Could TTS, will be phased out over time
    SPEAKER = 2 # Use the newer system, utilizing Speaker.bot, will be phased out over time
    STREAMER = 3 # Use the newest system, utilizing both Speaker and Streamer bot for better contextuality and YouTube Support

mode = Mode.STREAMER #Recommended Mode

if __name__ == '__main__':
    
    
    
    if mode == Mode.VLC_CLOUD:
        import os
        from vlc_based import Bot
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_JSON_PATH
        bot = Bot()
        bot.run()
        
    elif mode == Mode.SPEAKER:
        import os
        from vlc_based import Bot
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_JSON_PATH
        bot = Bot(speaker_bot=True)
        bot.run()
    
    elif mode == Mode.STREAMER:
        import threading
        from logger import Logger
        from speaker_bot_based import QueueConsumer, Bot
        
        l = Logger(console_log=True, file_logging=True, file_URI='logs/log.txt', override=True)
    
        consumer = QueueConsumer(logger=l, verbose=True, answer_rate=20)
        bot = Bot(consumer, l)
        process = threading.Thread(target=consumer.run)
        process.start()
        


        bot.run()
        process.join()