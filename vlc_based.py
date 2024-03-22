from asyncio import Queue
import asyncio
import json
import random
import threading
from logger import Logger
from twitchio.ext import commands
import websockets
from chat import *
from twitchio import ChannelInfo
from google.cloud import texttospeech_v1beta1 as texttospeech
import vlc
import os 
import time
import nltk
import creds


CONVERSATION_LIMIT = 20


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
    
    
    def __init__(self, logger:Logger, speaker_alias = 'Default', speaker_bot_port:int = 7580, no_command:bool = False, verbose:bool = False, answer_rate:int = 30) -> None:
        
        self.l = logger
        self.l.passing('Spawning Consumer')
        self.verbose = verbose
        self.system_prompt = { 'role': 'system', 'content': open_file('prompt_chat.txt') }
        self.conversation = list()
        self.queue = Queue()
        self.speaker_alias = speaker_alias
        self.no_command = no_command
        self.port = speaker_bot_port
        self.answer_rate = answer_rate
        pass
    
    def run(self):
        self.l.passing('starting consumer')
        asyncio.run(self.main())
    
    async def main(self):
        self.l.passing('consumer started')
        
        try:
            while (True):
                
                if not self.queue.empty():
                    message = await self.queue.get()
                    
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
        if response.startswith('Sally:'):
            response = response.replace('Sally:', '') # sometimes Sally: shows up
        if response.startswith('Sally on Twitch:'):
            response = response.replace('Sally on Twitch:', '') # don't even...
        if response.startswith('Sally on YouTube:'):
            response = response.replace('Sally on YouTube:', '') 
        if response.startswith('Sally on Stream:'):
            response = response.replace('Sally on Stream:', '')
            
        self.l.botReply("Sally",response)

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
        
        if 'sally' in msg.content.lower():
            self.l.info("Sally in msg")
            return True
        
        if '?response' in msg.content.lower():
            self.l.info("Command in msg")
            return True
        
        if random.randint(1,100)<self.answer_rate: #respond to 30% of messages anyway 
            self.l.info("Random trigger")
            return True
        
        if 'caesarlp' in msg.author:
            self.l.info("CaesarLP in msg")
            return True
        
        if 'Caesar LP' in msg.author:
            self.l.info("Caesar LP in msg")
            return True
        if 'CaesarLP' in msg.author:
            self.l.info("Caesar talked")
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

    conversation = list()

    def __init__(self, consumer: QueueConsumer, logger: Logger, no_command:bool = False, speaker_bot = False):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        self.l = logger
        self.l.passingblue('Spawning Bot')
        self.queueConsumer = consumer
        self.no_command = no_command
        self.speaker_bot = speaker_bot
        super().__init__(token= creds.TWITCH_TOKEN, prefix='!', initial_channels=[creds.TWITCH_CHANNEL])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if self.speaker_bot:
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
                return
        if message.echo:
            return

        # download the words corpus
        nltk.download('words')

        # Check if the message contains english words
        if not any(word in message.content for word in nltk.corpus.words.words()):
            return
        
        # Check if the message is too long or short
        if len(message.content) > 70 or len(message.content) < 3:
            return
        
        print('------------------------------------------------------')
        print(message.content)
        print(message.author.name)
        print(Bot.conversation)

        content = message.content.encode(encoding='ASCII',errors='ignore').decode()
        Bot.conversation.append({ 'role': 'user', 'content': content })
        print(content)

        response = gpt3_completion(Bot.conversation)
        print('DOGGIEBRO:' , response)

        if(Bot.conversation.count({ 'role': 'assistant', 'content': response }) == 0):
            Bot.conversation.append({ 'role': 'assistant', 'content': response })
        
        if len(Bot.conversation) > CONVERSATION_LIMIT:
            Bot.conversation = Bot.conversation[1:]
        
        if self.speaker_bot: #if speakerbot flag is set, skip everything else, just send message to sb
            self.send_to_speaker_bot(response)
            await self.handle_commands(message)
            return
        
        client = texttospeech.TextToSpeechClient()

        response = message.content + "? " + response
        ssml_text = '<speak>'
        response_counter = 0
        mark_array = []
        for s in response.split(' '):
            ssml_text += f'<mark name="{response_counter}"/>{s}'
            mark_array.append(s)
            response_counter += 1
        ssml_text += '</speak>'

        input_text = texttospeech.SynthesisInput(ssml = ssml_text)

        # Note: the voice can also be specified by name.
        # Names of voices can be retrieved with client.list_voices().
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-GB",
            name= "en-GB-Wavenet-B",
            ssml_gender=texttospeech.SsmlVoiceGender.MALE,
        )

        audio_config = texttospeech.AudioConfig(    
            audio_encoding=texttospeech.AudioEncoding.MP3,
        )
        

        response = client.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config, "enable_time_pointing": ["SSML_MARK"]}
        )


        # The response's audio_content is binary.
        with open("output.mp3", "wb") as out:
            out.write(response.audio_content)

        audio_file = os.path.dirname(__file__) + '/output.mp3'
        media = vlc.MediaPlayer(audio_file)
        media.play()
        #playsound(audio_file, winsound.SND_ASYNC)


        count = 0
        current = 0
        for i in range(len(response.timepoints)):
            count += 1
            current += 1
            with open("output.txt", "a", encoding="utf-8") as out:
                out.write(mark_array[int(response.timepoints[i].mark_name)] + " ")
            if i != len(response.timepoints) - 1:
                total_time = response.timepoints[i + 1].time_seconds
                time.sleep(total_time - response.timepoints[i].time_seconds)
            if current == 25:
                    open('output.txt', 'w', encoding="utf-8").close()
                    current = 0
                    count = 0
            elif count % 7 == 0:
                with open("output.txt", "a", encoding="utf-8") as out:
                    out.write("\n")
        time.sleep(2)
        open('output.txt', 'w').close()



        # Print the contents of our message to console...
        
        print('------------------------------------------------------')
        os.remove(audio_file)

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'Hello {ctx.author.name}!')
        
    async def updateStreamInfo(self):
        ch:ChannelInfo  = await self.fetch_channel(self.nick)
        game = ch.game_name
        title_parts = ch.title.split('|')
        title = title_parts[0]
        self.queueConsumer.setStreamInfo(game, title)
    




if __name__ == '__main__':

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds.GOOGLE_JSON_PATH

    l = Logger(console_log=True, file_logging=True, file_URI='logs/logger.txt', override=True)
    
    consumer = QueueConsumer(logger=l, verbose=True, answer_rate=20)
    bot = Bot(consumer, l)
    process = threading.Thread(target=consumer.run)
    process.start()
    


    bot.run()
    process.join()
