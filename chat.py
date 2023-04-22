import openai
import creds


def open_file(filepath):
    with open(filepath, "r", encoding="utf-8") as infile:
        return infile.read()


openai.api_key = creds.OPENAI_API_KEY
openai.api_base = "https://api.openai.com/v1/chat"


def gpt3_completion(
    messages,
    engine="gpt-3.5-turbo",
    temp=0.9,
    tokens=350,
    freq_pen=2.0,
    pres_pen=2.0,
    stop=[f"{creds.BOT_NAME}:"],
):
    response = openai.Completion.create(
        model=engine,
        messages=messages,
        temperature=temp,
        max_tokens=tokens,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop,
    )
    text = response["choices"][0]["message"]["content"].strip()
    return text
