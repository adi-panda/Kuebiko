from typing import TypeAlias

from openai.types.chat import (ChatCompletionAssistantMessageParam,
                               ChatCompletionFunctionMessageParam,
                               ChatCompletionSystemMessageParam,
                               ChatCompletionToolMessageParam,
                               ChatCompletionUserMessageParam)

ChatCompletionMessage: TypeAlias = (
    ChatCompletionSystemMessageParam
    | ChatCompletionUserMessageParam
    | ChatCompletionAssistantMessageParam
    | ChatCompletionToolMessageParam
    | ChatCompletionFunctionMessageParam
)


class CustomMessage:
    author: str
    content: str
    plattform: str
    answer: bool

    def __init__(self, author: str, content: str, plattform: str) -> None:
        self.author = author
        self.content = content
        self.plattform = plattform
        self.answer = False
        pass
