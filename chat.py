import openai
import creds
import settings

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = creds.OPENAI_API_KEY
openai.api_base = 'https://api.openai.com/v1/chat'

def gpt3_completion(messages, engine=settings.chatEngine, topp=max(min(float(settings.chatTopp), 1), 0) ,temp=max(min(float(settings.chatTemperature), 2), 1), tokens=abs(int(settings.chatTokenCount)), freq_pen=max(min(float(settings.chatFreqPenalty), 2), 1), pres_pen=max(min(float(settings.chatPresPenalty), 2), 1), stop=settings.chatStop):
    response = openai.Completion.create(
        model=engine,
        messages=messages,
        temperature=temp,
        max_tokens=tokens,
        top_p=topp,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    text = response['choices'][0]['message']['content'].strip()
    return text
