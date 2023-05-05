import openai
import creds
import json
import os


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

with open(os.path.expanduser('~') + '/.kuebikoInfo.json') as f:
    data = json.load(f)

openai.api_key = data.get('OPEN_API_KEY')

def gpt3_completion(prompt, engine='text-davinci-003', temp=0.9, tokens=400, freq_pen=2.0, pres_pen=2.0, stop=['DOGGIEBRO:', 'CHATTER:']):
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temp,
        max_tokens=tokens,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    text = response['choices'][0]['text'].strip()
    return text






