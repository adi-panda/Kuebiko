from twitchio.ext import commands
from chat import *
from google.cloud import texttospeech_v1beta1 as texttospeech
import vlc
import os 
import time
import nltk



class Bot(commands.Bot):

    conversation = list()

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        
        super().__init__(token='', prefix='!', initial_channels=[''])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # download the words corpus
        nltk.download('words')

        # Check if the message contains english words
        if not any(word in message.content for word in nltk.corpus.words.words()):
            return
        # Check if the message is too long
        if len(message.content) > 70:
            return
        print('------------------------------------------------------')
        print(message.content)
        print(message.author.name)
        print(Bot.conversation)

        Bot.conversation.append(f'CHATTER: {message.content}')
        text_block = '\n'.join(Bot.conversation)
        prompt = open_file('prompt_chat.txt').replace('<<BLOCK>>', text_block)
        prompt = prompt + '\nDOGGIEBRO:'
        print(prompt)
        response = gpt3_completion(prompt)
        print('DOGGIEBRO:' , response)
        if(Bot.conversation.count('DOGGIEBRO: ' + response) == 0):
            Bot.conversation.append(f'DOGGIEBRO: {response}')
        
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

        audio_file = os.path.dirname(__file__) + '\output.mp3'
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

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ''
bot = Bot()
bot.run()
# bot.run() is blocking and will stop execution of any below code here until stopped or closed.



