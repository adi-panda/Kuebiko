from chat import *
from google.cloud import texttospeech_v1beta1 as texttospeech
import vlc
import os 
import time
import creds
import threading
import json

with open(os.path.expanduser('~') + '/.kuebikoInfo.json') as f:
    data = json.load(f)
def message_response(message, conversation, CONVERSATION_LIMIT, is_finished):
    is_finished[0] = False;
    if len(conversation) > CONVERSATION_LIMIT:
        conversation = conversation[1:]

    # print('------------------------------------------------------')
    # print(message.content)
    # print(message.author.name)
    # print(conversation)

    conversation.append(f'CHATTER: {message}')
    text_block = '\n'.join(conversation)
    prompt_file = os.path.dirname(__file__) + '/prompt_chat.txt'
    prompt = open_file(prompt_file).replace('<<BLOCK>>', text_block)
    prompt = prompt + '\nDOGGIEBRO:'
    # print(prompt)

    response = gpt3_completion(prompt)
    print('DOGGIEBRO:' , response)



    if(conversation.count('DOGGIEBRO: ' + response) == 0):
        conversation.append(f'DOGGIEBRO: {response}')

    client = texttospeech.TextToSpeechClient()

    response = message + "? " + response
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
    with open(os.path.dirname(__file__) + '/output.mp3', "wb") as out:
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

    print('------------------------------------------------------', flush= True)
    os.remove(audio_file)
    is_finished[0] = True;

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.dirname(__file__) + "/" + data.get("GOOGLE_JSON_PATH")
