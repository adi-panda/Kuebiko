import openai


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key = ""
openai.api_base = 'https://api.openai.com/v1/chat'


def gpt3_completion(messages, engine='gpt-3.5-turbo', temp=0.9, tokens=400, freq_pen=2.0, pres_pen=2.0, stop=['DOGGIEBRO:', 'CHATTER:']):
    response = openai.Completion.create(
        engine=engine,
        messages=messages,
        temperature=temp,
        max_tokens=tokens,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    text = response['choices'][0]['message'].strip()
    return text