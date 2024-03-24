from asyncio import Queue
import asyncio
import threading
import websockets
from twitchio.ext import commands
from twitchio import ChannelInfo
from chat import *
import time
import random
import creds
import json
from json_handler import *
from logger import Logger


CONVERSATION_LIMIT = 40

class CustomMessage:
    author:str
    content:str
    plattform:str
    answer:bool
    
    def __init__(self,author:str,content:str, plattform:str) -> None:
        self.author = author
        self.content = content
        self.plattform = plattform
        self.answer = False
        pass


class QueueConsumer:
    
    
    def __init__(self, logger:Logger, speaker_bot_port:int = 7580, speaker_alias:str = 'Default', no_command:bool = False, verbose:bool = False, answer_rate:int = 30) -> None:
        
        self.l = logger
        self.l.passing('Spawning Consumer')
        self.verbose = verbose
        self.nick = ''
        self.system_prompt = { 'role': 'system', 'content': open_file('prompt_chat.txt') }
        self.conversation = list()
        self.queue = Queue()
        self.no_command = no_command
        self.port = speaker_bot_port
        self.speaker_alias = speaker_alias
        self.answer_rate = answer_rate
        pass
    
    def run(self):
        self.l.passing('starting consumer')
        asyncio.run(self.main())
    
    async def main(self):
        self.l.passing('consumer started')
        
        bad_words = read_json_file('filter.json')['blacklist']
        ignored_users = read_json_file('filter.json')['ignored_users']
        
        try:
            while (True):
                
                if not self.queue.empty():
                    message: CustomMessage = await self.queue.get()
                    if any(bad_word in message.content for bad_word in bad_words):
                        self.l.warning(f'Found blacklisted word in message {message.content} from {message.author} on {message.plattform}')
                        continue
                    if any( user == message.author for user in ignored_users):
                        self.l.warning(f'Found blacklisted word in message {message.content} from {message.author} on {message.plattform}')
                        continue
                    
                    if not await self.check_completion(message): #checks for already answered messages
                        await self.request_completion(message) #requests chatGPT completion
                        await asyncio.sleep(len(message.content)/10)
                        continue
                await self.youtube_chat() #check for new Youtube chat messages
                await self.voice_control() #check for new Voice commands
                    
        except Exception as e:
            self.l.fail(f'Exception in main loop: {e}')
            
            
    async def voice_control(self):
        
        await self.file2queue('streamer_exchange.txt', 'Stream')       
            
    async def youtube_chat(self):
        
        await self.file2queue('chat_exchange.txt', 'YouTube')
        
    async def file2queue(self,file_uri:str, plattform:str):
        file_contents = open_file(file_uri)
        if len(file_contents) < 1:
            return
        lines = file_contents.split('\n')
        for line in lines:
            if len(line) <1:
                continue
            contents = line.split(';msg:')
            msg = CustomMessage(contents[0], contents[1], plattform)
            msg.answer = await self.response_decision(msg)
            await self.queue.put(msg)
            
        self.delete_file_contents(file_uri)
        
        self.l.userReply(msg.author,msg.plattform , msg.content)  
        
    def delete_file_contents(self, file_path):
        try:
            # Open the file in write mode, which truncates the file
            with open(file_path, 'w'):
                pass  # Using pass to do nothing inside the with block
            self.l.passing("Contents of '{}' have been deleted.".format(file_path))
        except IOError:
            self.l.error("Unable to delete contents of '{}'.".format(file_path))
            
            
    async def put_message(self, message): # Only for twitch Message Objects! Not custom message
        author = message.author.name
        msg = message.content
        
        new_msg = CustomMessage(author, msg, 'Twitch')
        new_msg.answer = await self.response_decision(new_msg)
        await self.queue.put(new_msg)
        
    async def reload_prompt(self):
        self.l.passingblue('Reloading Prompt')
        self.system_prompt = { 'role': 'system', 'content': open_file('prompt_chat.txt') }
    
    async def toggle_verbosity(self):
        self.verbose = not self.verbose
        self.l.passingblue(f'Verbosity is now: {self.verbose}')
    
    async def clear_conv(self):
        self.l.passingblue('Clearing Conversations')
        self.conversation = list()
        
    async def check_completion(self, message: CustomMessage):
        
        for c in self.conversation:
            if c['content'] == message.content:
                return True
            
        return False
                
    async def request_completion(self, message: CustomMessage):
        
        
        
        # Check if the message is too long or short
        if len(message.content) > 150:
            self.l.warning('Message ignored: Too long')
            return
        if len(message.content) < 6:
            self.l.warning('Message ignored: Too short')
            return
        
        self.l.warning('--------------\nMessage being processed')
        self.l.userReply(message.author, message.plattform, message.content)
        self.l.info(self.conversation, printout = self.verbose)
        n:str = message.author
        cleaned_name = n.replace('_',' ')

        content = message.content.encode(encoding='ASCII',errors='ignore').decode()
        self.conversation.append({ 'role': 'user', 'content': f'{cleaned_name} on {message.plattform}: {content}' })
        
        self.l.info(content, printout = self.verbose)

        if not message.answer:
            self.l.info('Message appended, not answering', printout = self.verbose)
            return
        response:str = gpt3_completion(self.system_prompt , self.conversation, self.l, verbose = self.verbose)
        response = response.replace('_', ' ') # replace _ with SPACE to make TTS less jarring
        
        #All of the following checks are dependend on your prompt
        if response.startswith(f'{self.speaker_alias}:'):
            response = response.replace(f'{self.speaker_alias}', '') # sometimes Sally: shows up
        if response.startswith(f'{self.speaker_alias} on Twitch:'):
            response = response.replace(f'{self.speaker_alias} on Twitch:', '') # don't even...
        if response.startswith(f'{self.speaker_alias} on YouTube:'):
            response = response.replace(f'{self.speaker_alias} on YouTube:', '') 
        if response.startswith(f'{self.speaker_alias} on Stream:'):
            response = response.replace(f'{self.speaker_alias} on Stream:', '')
            
        self.l.botReply(self.speaker_alias,response)

        await self.speak(response)

        if(self.conversation.count({ 'role': 'assistant', 'content': response }) == 0):
            self.conversation.append({ 'role': 'assistant', 'content': response })
        
        if len(self.conversation) > CONVERSATION_LIMIT:
            self.conversation = self.conversation[1:]
        
        time.sleep(len(response)/10)
        
        self.l.warning('Cooldown ended, waiting for next message...\n--------------')
        
    async def response_decision(self, msg:CustomMessage) -> bool:
        if self.no_command:
            self.l.info("No Command flag set")
            return True
        
        if self.speaker_alias in msg.content.lower():
            self.l.info(f"{self.speaker_alias} in msg")
            return True
        
        if '!response' in msg.content.lower():
            self.l.info("Command in msg")
            return True
        
        if random.randint(1,100)<self.answer_rate: #respond to 30% of messages anyway 
            self.l.info("Random trigger")
            return True
        
        if self.nick in msg.author:
            self.l.info(f"{self.nick} in msg")
            return True
        
        self.l.warning('Discarding message')
        return False
        

    

    
    def setStreamInfo(self, game, title):
        self.l.passing(f'Setting stream info to "{title}" playing "{game}"')
        self.system_prompt['content'] = self.system_prompt['content'].replace(
            'STREAM_TITLE', title
            ).replace('GAME_NAME', game)
        
    async def speak(self, message):
        
        id = random.randrange(10000,99999)
        
        data = {
            "request": "Speak",
            "id": f"{id}",
            "voice": f"{self.speaker_alias}",
            "message": f"{message}"
            }
        
        self.l.info(f"Sending Packet with ID {id}")
        
        await self.send_json_via_websocket(data)
        

    async def send_json_via_websocket(self, json_data):
        async with websockets.connect((f'ws://localhost:{self.port}')) as websocket:
            # Convert JSON data to string
            json_string = json.dumps(json_data)
            
            # Send JSON string via WebSocket
            await websocket.send(json_string)
            self.l.info(f"Sent JSON data")
            if self.verbose:
                self.l.info(json_string)
            await websocket.close()
              


class Bot(commands.Bot):

    

    def __init__(self, consumer: QueueConsumer, logger: Logger, no_command:bool = False):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        self.l = logger
        self.l.passingblue('Spawning Bot')
        self.queueConsumer = consumer
        self.no_command = no_command
        super().__init__(token= creds.TWITCH_TOKEN, prefix='?', initial_channels=[creds.TWITCH_CHANNEL])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        self.l.passing(f'Logged in as | {self.nick}')
        self.queueConsumer.nick = self.nick
        await self.updateStreamInfo()
        
        
        
    #returns true if response should be given
    
    async def updateStreamInfo(self):
        ch:ChannelInfo  = await self.fetch_channel(self.nick)
        game = ch.game_name
        title_parts = ch.title.split('|')
        title = title_parts[0]
        self.queueConsumer.setStreamInfo(game, title)    

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        self.l.info(f'Message recieved:')
        
        #if message.echo:
        #    return
        if message.author.name == self.nick:
        
            if '!reload_prompt' in message.content:
                self.l.warning('Reloading prompt')
                
                await self.queueConsumer.reload_prompt()
                return
            
            if '!toggle_verbose' in message.content:
                self.l.warning('Toggling Verbosity')
                
                await self.queueConsumer.toggle_verbosity()
                return
            
            if '!clear_conv' in message.content:
                self.l.warning('Clearing Conversation')
                
                await self.queueConsumer.clear_conv()
                return
            
            if '!update_info'in message.content:
                self.l.warning('Updating Info')
                await self.updateStreamInfo()
                await self.queueConsumer.reload_prompt()
                return
            
            if '!reload_all'in message.content:
                self.l.warning('Reloading everything')
                await self.updateStreamInfo()
                await self.queueConsumer.reload_prompt()
                await self.queueConsumer.clear_conv()
                return
                
        
        msg: str = f'{message.author.name}:  {message.content}'    
        self.l.info(msg)
        await self.queueConsumer.put_message(message)
        
        
        
        await self.handle_commands(message)
        
        
        

  

if __name__ == '__main__':


    l = Logger(console_log=True, file_logging=True, file_URI='logs/logger.txt', override=True)
    
    consumer = QueueConsumer(logger=l, verbose=True, answer_rate=20)
    bot = Bot(consumer, l)
    process = threading.Thread(target=consumer.run)
    process.start()
    


    bot.run()
    process.join()



