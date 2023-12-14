import sys #Do not remove this line

##### AI SPECIFIC Settings #####

# AI's Name 
AINAME = 'AINAME'
# Conversation History
CONVERSATION_LIMIT = 10
# Should prompts be on a user-specific level, or just use prompt_chat.txt? If the user-specific prompt does not exist, it uses the prompt_chat.txt by default.
# This feature will require you to create files in the userprompts folder.
useUserPrompt = False
# Should we do version checking? True/False
doVersionCheck = True

### TTS SETTING ###
#For more info on this section, see https://cloud.google.com/text-to-speech/docs/voices

#Language Code
languageCode = "en-US"
#Name of Voice Model 
voiceName = "en-US-Polyglot-1"
#Gender (Accepts MALE/FEMALE)
ssmlGender = "MALE"
#Should the bot speak messages out?
playAudio = True

#Pitch (from -20 to 20), 0 is default
voicePitch = 0
#Gain (from -96 to 16), default is 0
voiceGain = 0
#Speaking Rate (from 0.25 to 4), default is 1
voiceRate = 1
#Sample Rate Hertz (8000 to 48000), default is 48000
voiceHertz = 48000


##### REDEEM DETECTION SETTINGS #####

# Should the bot listen for a specific redeem?
doRedeem = True
# Redeem ID - See https://www.instafluff.tv/TwitchCustomRewardID/?channel=YOURTWITCHCHANNEL
redeemID = ''

##### BITS DETECTION SETTINGS #####

# Should the bot listen for bits donations?
doBits = True
# Lower Bits Detection Number 
bitsLookAtLowNumber = 100
# Higher Bits Detection Number
bitsLookAtHighNumber = sys.maxsize
#Cooldown Timer in seconds
cooldownBits = 120
#Log to Twitch Chat?
bitsMessageLogChat = True

##### MESSAGE DETECTION SETTINGS #####

# Should we listen in for raw messages with the prefix?
doRawMessages = False
# AI NAME to Detect
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
# List of keywords to listen for
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

##### MESSAGE SPECIFIC SETTINGS #####

# Should the bot send messages to chat?
PostMSGtoChat = True
# Should block list be on?
blockList = False
# Profanity Filter Check
doProfanityCheck = True
# Minimum message length of message to AI to get a response (not related to message detection events)
globalminimumLength = 3
# Max Message Length (200-500), but would recommend leaving it at 500
globalmaximumLength = 500
