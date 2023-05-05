from random import randint
from twitchio.ext import commands
from chat import *
from google.cloud import texttospeech_v1beta1 as texttospeech
import vlc
import os 
import time
import nltk
import creds
import threading
from collections import deque
from message import message_response
# from enum import ENUM
import json 



MESSAGE_LIMIT = 3
ASYNC = False

with open(os.path.expanduser('~') + '/.kuebikoInfo.json') as f:
    data = json.load(f)

print(data.get("OPEN_API_KEY"), flush=True)

#class current_model(Enum):
#    DAVNCI = 1
#    GPTTURBO = 2
#    CUSTOMGPT = 3
#    ALPACA = 4
class Bot(commands.Bot):
    conversation = list()
    current_messages = list()
    previous_responses = list()
    streamer_count = 0
    streamer_messages = list()
    done = [True]

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        
        super().__init__(token= data.get("TWITCH_TOKEN"), prefix='!', initial_channels=[data.get("TWITCH_CHANNEL")])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}', flush=True)

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # download the words corpus
        nltk.download('words')

        # Check if the message contains english words
        # if not any(word in message.content for word in nltk.corpus.words.words()):
        #     return
        # Check if the message is too long
        if len(message.content) > 70:
            return

        if(message.author.name == creds.TWITCH_CHANNEL):
            Bot.streamer_messages.append(message.content)
            Bot.streamer_count += 1

        Bot.current_messages.append(message.content)
        new_message = Bot.current_messages[randint(0, len(Bot.current_messages) - 1)]
        print(new_message, flush= True)

        if(Bot.done[0] == True):
            count = 0
            while((new_message in Bot.previous_responses) and (count <= len(Bot.previous_responses))):
                new_message = Bot.current_messages[randint(0, len(Bot.current_messages) - 1)]
                count += 1

            if(Bot.streamer_count >= 1):
                print(Bot.streamer_messages , flush=True)
                new_message = Bot.streamer_messages[0]
                Bot.streamer_messages = Bot.streamer_messages[1:]
                print(Bot.streamer_messages, flush=True)
                Bot.streamer_count -= 1

                     
            Bot.previous_responses.append(new_message)
            t1 = threading.Thread(target=message_response, 
                                args = (new_message, 
                                        Bot.conversation, 20, Bot.done))
            t1.start()

        if (len(Bot.current_messages) > MESSAGE_LIMIT):
            Bot.current_messages = Bot.current_messages[1:]    

        if (len(Bot.previous_responses) > MESSAGE_LIMIT * 2):
            Bot.previous_responses = Bot.previous_responses[1:]   

        

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

print("Starting Bot", flush=True)
bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.



