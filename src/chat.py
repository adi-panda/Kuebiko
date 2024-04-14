from typing import List

from openai import OpenAI

from .chattypes import ChatCompletionMessage
from .credentials import BOT_NAME, OPENAI_API_KEY
from .logger import Logger

openai = OpenAI(api_key=OPENAI_API_KEY)


def gpt3_completion(
    system_prompt: List[ChatCompletionMessage],
    messages: List[ChatCompletionMessage] = list(),
    logger: Logger | None = None,
    engine="gpt-3.5-turbo",
    verbose=False,
    temp=0.9,
    tokens=150,
    freq_pen=2.0,
    pres_pen=2.0,
    stop: List[str] = [f"{BOT_NAME}:", "CHATTER:"],
):
    msg: List[ChatCompletionMessage] = list()
    for m in system_prompt:
        msg.append(m)
    for m in messages:
        msg.append(m)
    if logger is not None:
        logger.info(msg, verbose)
    response = openai.chat.completions.create(
        messages=messages,
        model=engine,
        temperature=temp,
        max_tokens=tokens,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop,
    )
    content = response.choices[0].message.content
    if content is None:
        return ""
    text = content.strip()
    return text
