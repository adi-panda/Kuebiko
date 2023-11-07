from twitchio.ext import commands
from twitchio.ext import pubsub
from chat import *
from google.cloud import texttospeech_v1beta1 as texttospeech
import vlc
import os 
import time
import nltk
import creds
import re
import requests
# from profanityfiltermaster import *
from profanityfiltermaster import profanity_filter as profanityfilter
from twitchchatmaster.twitch_chat import *
import threading
REDEEM_ID = 'REDEEMID'  # The ID of the specific redemption you want to monitor
AINAME = 'AINAME' # The name that will be printed in chat messages.
 
CONVERSATION_LIMIT = 10 # Higher amounts will cost more
AINAME_FIXED=AINAME+":"

class Bot(commands.Bot):
 
    conversations = {}
 
    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
 
        self.context_string = open_file('prompt_chat.txt');
        super().__init__(token= creds.TWITCH_TOKEN, prefix='!', initial_channels=[creds.TWITCH_CHANNEL])
 
    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'(Version 1.0.0 - Logged in as | {self.nick}')
        
    def detect_cheer(self, text):
        pattern = r'cheer(\d+)' #detect messages with cheering in iy
        matches = re.findall(pattern, text, re.IGNORECASE) #look for all cases of cheer messages   
        amount = 0 #Reset to 0 so that we ensure proper number counting
        for match in matches:
            if match:
                amount += int(match)  # Add the bits from this amount to the total
        has_message = bool(re.sub(pattern, '', text, flags=re.IGNORECASE).strip())  #Boolean Check if there's non-cheer text
        return amount, has_message
        
    def split_messages(self, messageChat):
        max_length = 500
        messages = []
        current_message = [AINAME_FIXED]
        words = messageChat.split()

        for word in words:
            if len(" ".join(current_message + [word])) <= max_length:
                current_message.append(word)
            else:
                messages.append(" ".join(current_message))
                current_message = [AINAME_FIXED, word]

        # Adding the last message
        if len(" ".join(current_message)) > len(AINAME_FIXED):
            messages.append(" ".join(current_message))

        return messages

    def send_messages_to_chat(self, textresponse):
        sendMessage = True
        my_chat = TwitchChat(oauth=creds.BOT_ACCOUNT_TWITCH_OAUTH, bot_name=creds.BOT_ACCOUNT_TWITCH_CHANNEL, channel_name=creds.SENDMESSAGE_TO_THIS_CHANNEL)
        messages = self.split_messages(textresponse)
    
        if sendMessage:
            [my_chat.send_to_chat(messageChat) for messageChat in messages]

    def generate_speech(self, response, user_context, CONVERSATION_LIMIT):
        if user_context.count({ 'role': 'assistant', 'content': response }) == 0:
            user_context.append({ 'role': 'assistant', 'content': response })

        if len(user_context) > CONVERSATION_LIMIT:
            try:
                user_context.pop(1) #Pull the SECOND element only. Must be at least 1, so that AI keeps context
            except IndexError:
                print("IndexError on pop of user context")
            

        # Initialize the TextToSpeechClient from the Text-to-Speech API.

        client = texttospeech.TextToSpeechClient()

        # Process the response text to create SSML for speech synthesis.
        ssml_text = '<speak>'
        response_counter = 0
        mark_array = []
        for s in response.split(' '):
            ssml_text += f'<mark name="{response_counter}"/>{s}'
            mark_array.append(s)
            response_counter += 1
        ssml_text += '</speak>'

        input_text = texttospeech.SynthesisInput(ssml=ssml_text)

        # Configure the voice for the speech synthesis.
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Polyglot-1",
            ssml_gender=texttospeech.SsmlVoiceGender.MALE,
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
        )

        # Use the Text-to-Speech client to synthesize speech from the input text.
        response = client.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config, "enable_time_pointing": ["SSML_MARK"]}
        )

        # Save the generated audio content to a file and play it using VLC.

        with open("output.mp3", "wb") as out:
            out.write(response.audio_content)

        audio_file = os.path.dirname(__file__) + '/output.mp3'
        media = vlc.MediaPlayer(audio_file)
        media.play()

        # Generate and save a transcript of the speech with timing information.

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

        # Remove the generated audio file and print some information.

        print('------------------------------------------------------')
        os.remove(audio_file)
        
    def run_methods_concurrently(self, textresponse, response, user_context, CONVERSATION_LIMIT):
        thread1 = threading.Thread(target=self.generate_speech, args=(response, user_context, CONVERSATION_LIMIT,))
        thread2 = threading.Thread(target=self.send_messages_to_chat, args=(textresponse,))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

 
    async def event_message(self, message):
        bitsAmount, has_message = self.detect_cheer(message.content)
        pfilter = profanityfilter.ProfanityFilter()
        doFilter = True # Should the profanity filter run?
        if message.echo:
            return
        if doFilter and pfilter.isProfane(message.content):
            # This only runs if Filter is true
            print("Filter went off by "+message.author.name+": "+message.content) #Log the user and message that triggered the profanity filter
            return
        if (message.tags.get('custom-reward-id') == REDEEM_ID) or (bitsAmount >= 100 and has_message):
            # Check if redeem or bits donation of 100 or more with message attached
            theusername = message.author.name
            themessage = message.content
            print(f'Redemption by {message.author.name}: {message.content}')
            # download the words corpus
            nltk.download('words')
    
            # Check if the message contains english words
            #if not any(word in message.content for word in nltk.corpus.words.words()):
            #    return
            
            # Check if the message is too long or short
            if len(message.content) > 470 or len(message.content) < 3:
                return
            
            print('------------------------------------------------------')
            print(message.content)
            print(message.author.name)
            if message.author.name not in Bot.conversations:
                Bot.conversations[message.author.name] = []
                user_context = Bot.conversations[message.author.name]
                user_context.append({ 'role': 'system', 'content': self.context_string })
            user_context = Bot.conversations[message.author.name]
            
            print(user_context)
    
            content = message.content.encode(encoding='ASCII',errors='ignore').decode()
            user_context.append({ 'role': 'user', 'content': theusername+" said: "+content })
            print(content)
            
            try:
                response = gpt3_completion(user_context)
            except openai.error.OpenAIError as e:
                if "message contains too many tokens" in e:
                    Bot.conversations[message.author.name] = [] #Wipe User Messages
                    user_context = Bot.conversations[message.author.name] #Redeclare
                    user_context.append({ 'role': 'system', 'content': self.context_string }) #Readd context string
                    user_context.append({ 'role': 'user', 'content': theusername+" said: "+content })
                    response = gpt3_completion(user_context) #Retry the question
                
            print(AINAME_FIXED , response)
            
            # Copied for text chat response reasons
            textresponse = response
 
            self.run_methods_concurrently(textresponse, response, user_context, CONVERSATION_LIMIT)
            
            #Text AI in Chat
            # Should The AI send a message in chat?
 
            # Since we have commands and are overriding the default `event_message`
            # We must let the bot know we want to handle and invoke our commands...
            await self.handle_commands(message)
 
    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.
 
        # Send a hello back!
        # Sending a reply back to  the channel is easy... Below is an example.
        await ctx.send(f'Hello {ctx.author.name}!')
 
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds.GOOGLE_JSON_PATH
bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.
 
 
 
 
