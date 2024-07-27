from typing import Iterable, List

from .chattypes import ChatCompletionMessage
from .credentials import BOT_NAME
from .logger import Logger
from .openai import openai

_default_stop = [f"{BOT_NAME}:", "CHATTER:"]


def gpt3_completion(
    system_prompt: Iterable[ChatCompletionMessage],
    messages: Iterable[ChatCompletionMessage] = tuple(),
    logger: Logger | None = None,
    engine="gpt-3.5-turbo",
    verbose=False,
    temp=0.9,
    tokens=150,
    freq_pen=2.0,
    pres_pen=2.0,
    stop: List[str] = _default_stop,
):
    msg: List[ChatCompletionMessage] = list()
    for m in system_prompt:
        msg.append(m)
    for m in messages:
        msg.append(m)
    if logger is not None:
        logger.info(msg, verbose)
    response = openai.chat.completions.create(
        messages=msg,
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
