from pynput import keyboard
import speech_recognition as sr
from Library.twitchchatmaster.twitch_chat import *
import settings
import creds
from chat import *
#from main_userContext import Version as VersionOld
import requests
import os
import vlc
from Library.profanityfiltermaster import profanity_filter as profanityfilter
import threading
from elevenlabs import *
from elevenlabs.client import ElevenLabs
from google.cloud import texttospeech_v1beta1 as texttospeech
import time
from twitchio.ext import commands, pubsub
import re
import asyncio

CONVERSATION_LIMIT = int(settings.CONVERSATION_LIMIT)
AINAME_FIXED=settings.AINAME+":"
Version = "1.2.1"

class KeyPressing(commands.Bot):
    def __init__(self):
        self._http = None
        chat_instance = TwitchChat(creds.TWITCH_CHANNEL, creds.BOT_ACCOUNT_TWITCH_CHANNEL, creds.BOT_ACCOUNT_TWITCH_OAUTH)
        channel_name = chat_instance.channel
        print(f'(Version '+Version+') - Logged in as '+str(channel_name))
        if settings.doVersionCheck:
            self.version_Check(Version)
        self.context_string = open_file('prompt_chat.txt');

    conversations = {}

    def version_Check(self, local_version):
        #Informs if an update is available.
        url = "https://raw.githubusercontent.com/TheSoftDiamond/Kazushin/main/version.txt"
        response = requests.get(url)
        if response.status_code == 200:
            version_online = response.text.strip()
            if local_version > version_online:
                #This case should never be passed
                print("ERROR: Kazushin Build "+Version+" is not supposed to be newer than online version. Please change the version tag back.")
            elif local_version < version_online:
                print("Kazushin Build "+Version+" is older than the online version. Consider updating your bot.")
            else:
                print("Your Kazushin Build is up to date")
        
            return version_online
        else:
            print(f"Failed to retrieve version check link data")
            return None
        
    def minmax(self, value, minvalue, maxvalue):
        #Minmax function
        recalculatedvalue = max(min(value, maxvalue), minvalue)
        return recalculatedvalue
    
    def is_between(self, value, minvalue, maxvalue):
        #Similar to minmax, but we return true or false here, but instead of forcing between two variables, tests if between two variables
        return minvalue <= value <= maxvalue

    async def run_methods_concurrently(self, response, responsetwo, user_context, CONVERSATION_LIMIT, text, author):
        thread1 = threading.Thread(target=self.generate_speech, args=(response, user_context, CONVERSATION_LIMIT, text, author))
        thread2 = threading.Thread(target=self.send_messages_to_chat, args=(response,))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()
    
    ### Begin Message Functions ###

    def split_messages(self, messageChat):
        # Used to split messages for the chat messages that Kazushin responds with
        max_length = self.minmax(int(settings.globalmaximumLength),200,500)
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
        #Send Messages to Chat?
        sendMessage = True
        my_chat = TwitchChat(oauth=creds.BOT_ACCOUNT_TWITCH_OAUTH, bot_name=creds.BOT_ACCOUNT_TWITCH_CHANNEL, channel_name=creds.SENDMESSAGE_TO_THIS_CHANNEL)
        messages = self.split_messages(textresponse)
    
        if sendMessage:
            [my_chat.send_to_chat(messageChat) for messageChat in messages]

    def get_microphone_devices():
        devices = sr.Microphone.list_microphone_names()
        print("Available microphone devices:")
        for i, device in enumerate(devices):
            print(f"{i+1}. {device}")
        return devices
    
    async def listen_for_speech(self):
        pfilter = profanityfilter.ProfanityFilter()
        recognizer = sr.Recognizer()
        microphone = sr.Microphone(device_index=int(settings.useDeviceID))

        # Print the name of the audio device
        print("Audio device:", microphone.list_microphone_names()[int(settings.useDeviceID)])

        with microphone as source:
            print("Listening...")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio) 
                print("You said:", text)

                theusername = "owner"
                
                if theusername not in KeyPressing.conversations:
                    KeyPressing.conversations[theusername] = []
                    user_context = KeyPressing.conversations[theusername]
                    user_context.append({ 'role': 'system', 'content': self.context_string })
                user_context = KeyPressing.conversations[theusername]
                
                print(user_context)
        
                content = text.encode(encoding='ASCII',errors='ignore').decode()
                user_context.append({ 'role': 'user', 'content': theusername+" said: "+content})
                
                try:
                    response = gpt3_completion(user_context)
                except openai.error.InvalidRequestError as e:
                    errormsg = str(e)
                    if "tokens" in errormsg:
                        KeyPressing.conversations[theusername] = [] #Wipe User Messages if token limit reached
                        user_context = KeyPressing.conversations[theusername] #Redeclare user context
                        user_context.append({ 'role': 'system', 'content': self.context_string}) #Readd context string from default
                        user_context.append({ 'role': 'user', 'content': theusername+" said: "+content})
                        response = gpt3_completion(user_context) #Retry the question after readding context
                response2 = response
                await self.run_methods_concurrently(response, response2, user_context, CONVERSATION_LIMIT, text, theusername)
                                
            except sr.UnknownValueError:
                print("Sorry, I could not understand your speech.")
            except sr.RequestError:
                print("Sorry, I'm having trouble accessing the speech recognition service.")
            return text
        
    ### SPEECHH ###
        
    def generate_speech(self, response, user_context, CONVERSATION_LIMIT, text, author):
        if user_context.count({ 'role': 'assistant', 'content': response }) == 0:
            user_context.append({ 'role': 'assistant', 'content': response })

        if len(user_context) > CONVERSATION_LIMIT:
            try:
                user_context.pop(1) #Pull the SECOND element only. Must be at least 1, so that AI keeps context
            except IndexError:
                print("IndexError on pop of user context")

        # Process the response text to create SSML for speech synthesis. For Google Text to Speech.
        ssml_text = '<speak>'
        response_counter = 0
        mark_array = []
        for s in response.split(' '):
            ssml_text += f'<mark name="{response_counter}"/>{s}'
            mark_array.append(s)
            response_counter += 1
        ssml_text += '</speak>'

        if settings.ttsEngine.lower() == "google":
            # Initialize the TextToSpeechClient from the Text-to-Speech API.

            client = texttospeech.TextToSpeechClient()

            input_text = texttospeech.SynthesisInput(ssml=ssml_text)

            # Configure the voice for the speech synthesis for Google Text to Speech.
            if settings.ssmlGender.lower().strip() == "male":
                voice = texttospeech.VoiceSelectionParams(
                    language_code=settings.languageCode.strip("'"),
                    name=settings.voiceName.strip("'"),
                    ssml_gender=texttospeech.SsmlVoiceGender.MALE,
                )
            elif settings.ssmlGender.lower().strip() == "female":
                voice = texttospeech.VoiceSelectionParams(
                    language_code=settings.languageCode.strip("'"),
                    name=settings.voiceName.strip("'"),
                    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
                )

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                pitch=self.minmax(settings.voicePitch, -20, 20),
                volume_gain_db=self.minmax(settings.voiceGain, -96, 16),
                speaking_rate=self.minmax(settings.voiceRate, 0.25, 4),
                sample_rate_hertz=self.minmax(settings.voiceHertz, 8000, 48000)
            )

            # Use the Text-to-Speech client to synthesize speech from the input text.
            responsespeak = client.synthesize_speech(
                request={"input": input_text, "voice": voice, "audio_config": audio_config, "enable_time_pointing": ["SSML_MARK"]}
            )

        if settings.ttsEngine.lower() == "elevenlabs":
            elevensettings = VoiceSettings(
                speaking_rate=self.minmax(settings.elevenSpeakingRate, 0, 4), 
                stability=float(settings.elevenStability), 
                similarity_boost=float(settings.elevenSimilarityBoost), 
                style=float(settings.elevenStlye), 
                use_speaker_boost=settings.elevenSpeakerBoost) 
            audio = generate(
                api_key=str(creds.ELEVENLABS_API_KEY),
                text=response,
                voice=Voice(
                    voice_id=settings.elevenVoiceID,
                    settings=elevensettings
                )
            )

        # Save the generated audio content to a file and play it using VLC.
        if settings.playAudio:
            count = 0
            current = 0

            if settings.ttsEngine.lower() == "google":
                audio_file = os.path.dirname(__file__) + '/output2.mp3'
                with open(audio_file, "wb") as out:
                    out.write(responsespeak.audio_content)

                media = vlc.MediaPlayer(audio_file)
                media.play()

            if settings.ttsEngine.lower() == "elevenlabs":
                audio_file = os.path.dirname(__file__) + '/output2.mp3'
                with open(audio_file, "wb") as out:
                    out.write(audio)

                media = vlc.MediaPlayer(audio_file)
                media.play()

            # Remove the generated audio file and print some information.
            time.sleep(2)
            try:
                os.remove(audio_file)
            except PermissionError:
                print("(PermissionError when trying to remove audio file. But not a serious issue.)")

        print('------------------------------------------------------')

    def on_press(self,key):
        if key == keyboard.Key.space:
            asyncio.run(self.listen_for_speech())
        elif key == keyboard.Key.esc:
            print(f"Exiting...")
            exit()
            
    def start(self):
        listener = keyboard.Listener(on_press=self.on_press)
        try:
            listener.start()
            listener.join()
        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            listener.stop()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = creds.GOOGLE_JSON_PATH
key_pressing = KeyPressing()
key_pressing.start()