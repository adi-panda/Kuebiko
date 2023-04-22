import os
from src.twitchbot import Bot


os.environ["BASE_DIR_PATH"] = os.path.dirname(os.path.realpath(__file__))

bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until
# stopped or closed.
