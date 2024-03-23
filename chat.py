import openai
import creds
from logger import Logger


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = creds.OPENAI_API_KEY
openai.api_base = 'https://api.openai.com/v1/chat'


def gpt3_completion(system_prompt, messages,logger:Logger = None, engine='gpt-3.5-turbo',verbose = False , temp=0.9, tokens=400, freq_pen=2.0, pres_pen=2.0, stop=['DOGGIEBRO:', 'CHATTER:']):
    msg = list()
    msg.append(system_prompt)
    for m in messages:
        msg.append(m)
    if not logger == None:
        logger.info(msg, verbose)
    
    response = openai.Completion.create(
        model=engine,
        messages=messages,
        temperature=temp,
        max_tokens=tokens,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    text = response['choices'][0]['message']['content'].strip()
    return text