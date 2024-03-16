import sys #Do not remove this line

###### FORMAT ######
# ##### Denotes a program's section
# ### Denotes a sub-section
# ## Denotes a sub-sub-section
# # Denotes a setting

##### GENERAL AI SETTINGS #####

# AI's Name (This is what will be parsed in the chat for the chat when the AI speaks.)
AINAME = 'AINAME'
# Conversation History (How many messages to keep in the conversation history)
CONVERSATION_LIMIT = 10
# Should prompts be on a user-specific level, or just use prompt_chat.txt? If the user-specific prompt does not exist, it uses the prompt_chat.txt by default.
# This feature will require you to create files in the customprompts/userprompts directory.
useUserPrompt = False
# Should we do version checking? True/False
doVersionCheck = True
# Engine to use (Accepted variables are: OpenAI, Gemini) for AI Engine Handing
AIMode = 'OpenAI'

### OPENAI SETTINGS ###

# GPT Model to use
chatEngine = 'gpt-3.5-turbo-1106'
# AI Temperature from 0-2. (0 is very predictable, 2 is very random). Recommended values are 0.8 to 1.4.
chatTemperature = 1.2
# Token Count for messages (Amount of tokens to return in the message, Recommended to keep lower to prevent spamming chat.)
chatTokenCount = 210
#Top P
chatTopp=1
# Frequency Penalty, value from 0 to 2
chatFreqPenalty = 0.0
#Presence Penalty, value from 0 to 2 
chatPresPenalty = 0.0
# Chat Stoopers
chatStop = [AINAME, 'CHATTER:']

### GEMINI SETTINGS ###
model = 'gemini-pro' # See https://ai.google.dev/models/gemini for more info regarding models.
# Temperature
GeminiTemp = 1
# Top P
GeminiTopP = 1
#Top K
GeminiTopK = 1
# Max Output Tokens
GeminiMaxTokens = 2048
#### SAFETY SETTINGS ####
#### Organized by Catrgory and Rating on a scale of of 0 to 3- Read https://ai.google.dev/docs/safety_setting_gemini for more info ####
# Harassment Category
GeminiHarmHarassmentBlock = 3
# Hate Speech Category
geminiHateSpeechBlock = 3
# NSFW Category
geminiNSFWBlock = 3
#Dangerous Category
geminiDangerousBlock = 3


### TTS SETTING ###
#For more info on this section, see https://cloud.google.com/text-to-speech/docs/voices

# Engine to use (Accepted variables are: Google, Elevenlabs) for TTS Voice Handing
ttsEngine = 'Google'
#Should the bot speak messages as audio?
playAudio = True

# Google TTS Settings ##

#Language Code
languageCode = "en-US"
#Name of Voice Model 
voiceName = "en-US-Polyglot-1"
#Gender (Accepts MALE/FEMALE)
ssmlGender = "MALE"

#Pitch (from -20 to 20), 0 is default
voicePitch = 0
#Gain (from -96 to 16), default is 0
voiceGain = 0
#Speaking Rate (from 0.25 to 4), default is 1
voiceRate = 1
#Sample Rate Hertz (8000 to 48000), default is 48000
voiceHertz = 48000

## Elevenlabs TTS Settings ##

#Voice ID - Use getVoices.py from tools to get a list of voice IDs.
elevenVoiceID = ""
#Similiarity Boost
elevenSimilarityBoost = 0
#Stability
elevenStability = 0
#Styling
elevenStlye = 0
#Use Speaker Boost? (True/False)
elevenSpeakerBoost = False
# Optimize Streaming Later? (0-4)
elevenOptimizeStreaming = 0
# Output Format (See https://elevenlabs.io/docs/api-reference/text-to-speech for more info. Recommended to not change this settings below.)
elevenOutputFormat = "mp3_44100_128"
# Speaking Rate
elevenSpeakingRate = 1

### BEGIN REDEEM SETTINGS ###

# Should block list be on?
blockList = False
# Profanity Filter Check
doProfanityCheck = True
# Minimum message length of message to AI to get a response (not related to message detection events)
globalminimumLength = 3
# How big should the message chunks be for the bot's response? (200-500)
globalmaximumLength = 500

## REDEEM DETECTION SETTINGS ##

# Should the bot listen for a specific redeem?
doRedeem = True
# Redeem ID - See https://www.instafluff.tv/TwitchCustomRewardID/?channel=YOURTWITCHCHANNEL
redeemID = ''

## BITS DETECTION SETTINGS ##

# Should the bot listen for bits donations?
doBits = True
# Lower Bits Detection Number 
bitsLookAtLowNumber = 100
# Higher Bits Detection Number )
bitsLookAtHighNumber = sys.maxsize
#Cooldown Timer expressed in seconds. Expects an integer.
cooldownBits = 120
#Log to Twitch Chat?
bitsMessageLogChat = True

## MESSAGE DETECTION SETTINGS ##

# Should we listen in for raw messages with the prefix?
doRawMessages = False
# AI Name Detection (Combined with prefix, will listen for messages that contain the AI's name.)
detectMSGName = 'AINAME'
# Prefix
prefix = '!'
#Cooldown Timer in seconds
cooldownMsg = 120
#Log to Twitch Chat?
rawMessageLogChat = True

# Should we listen for keywords found in the chat?
doKeywords = False
# Cooldown Timer in seconds for messages that see the keyword?
cooldownKeywords = 10
# List of keywords to listen for (Each keyword should be wrapped in quotes and separated by a comma.)
keywordsinUserMsg = []
# Chance to respond to messages (0-100) 
keywordsinUserChance = 100
#Log to Console?
keywordsLogConsole = True

# Should we listen for pitch and speed event in the user's message?
listenForAudioEvent = True
# Users Allowed to control pitch and speed in their messages, in lower case:
listOfUsersAudioEvent = []
# Global Mode. Will allow everyont to interact with the audio event, regardless of who is on the list of allowed users.
globalAudioEventMode = False

### AI MESSAGE SPECIFIC SETTINGS ###

# Should the bot send messages to chat?
PostMSGtoChat = True

### SHOUTOUT/RAID SETTINGS ###
# You can customize the behavior of the prompt message at raidPrompt.txt

#Activate on shoutout commands?
doShoutout = True
# What should the shoutout commands be? (Separated by a comma.)
raidCommands = ["!shoutout", "!so"]
# Should Shoutout Message Audio be played? (True/False)
playAudioRaid = False
# Should shotout prompts be on a user-specific level, or just use raidprompts.txt? If the user-specific prompt does not exist, it uses the raidprompt.txt by default.
# This feature will require you to create files in the customprompts/userprompts directory.
useUserRaidPrompt = False

#Should Kazushin collect information about the raiding channel? (True/False)
#This is useful if you want Kazushin to generate personlized shoutouts to those who raided your channel with reference to live data from the raiding channel.
collectInfoFromRaid = True



##### SPEECH TO TEXT SETTINGS #####

# Which audio device should we use for speech to text? (Use getAudioDevices.py from tools to get a list of devices. 0 assumes the default device.)
useDeviceID = 0