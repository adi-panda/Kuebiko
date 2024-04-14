from typing import List

from twitchio.ext import commands  # type: ignore

from .chat import gpt3_completion
from .chattypes import ChatCompletionMessage
from .credentials import BOT_NAME, TWITCH_CHANNEL, TWITCH_TOKEN
from .filter_message import check_and_filter_user_message
from .texttospeech_evenlabs import get_speech_by_text
from .utils import open_file
from .websocket import open_websocket

CONVERSATION_LIMIT = 20


class Bot(commands.Bot):
    conversation: List[ChatCompletionMessage] = list()

    def __init__(self, speaker_bot=False, speaker_alias="Default"):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...  # noqa: E501
        # prefix can be a callable, which returns a list of strings or a string...  # noqa: E501
        # initial_channels can also be a callable which returns a list of strings...  # noqa: E501
        Bot.conversation.append(
            {"role": "system", "content": open_file("prompt_chat.txt")}
        )
        self.speaker_bot = speaker_bot
        self.speaker_alias = speaker_alias
        super().__init__(
            token=TWITCH_TOKEN,
            prefix="!",
            initial_channels=[TWITCH_CHANNEL],
        )

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f"Logged in as | {self.nick}")

    async def event_message(self, message):
        if check_and_filter_user_message(message):
            return

        msg = message.content
        user = message.author.name
        user_question = msg.encode(encoding="ASCII", errors="ignore").decode()
        print("------------------------------------------------------")
        print(Bot.conversation)
        print(f"{user} say: {user_question}")

        Bot.conversation.append({"role": "user", "content": user_question})

        bot_response = gpt3_completion(Bot.conversation)
        print(f"{BOT_NAME}:", bot_response)

        conversation = {"role": "assistant", "content": bot_response}
        if Bot.conversation.count(conversation) == 0:
            Bot.conversation.append(conversation)

        if len(Bot.conversation) > CONVERSATION_LIMIT:
            Bot.conversation = Bot.conversation[1:]

        if (
            self.speaker_bot
        ):  # if speakerbot flag is set, skip everything else, just send
            # message to sb
            self.send_to_speaker_bot(bot_response)
            await self.handle_commands(message)
            return

        get_speech_by_text(user_question, bot_response)

        # Print the contents of our message to console...

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    @commands.command(name="hola", aliases=["op", "haupei", "alo", "buen día"])
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our
        # prefix and command name e.g ?hello
        # We can also give our commands aliases (different names)
        # to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f"Hello {ctx.author.name}!")

    async def send_to_speaker_bot(self, message: str, verbose=False) -> None:
        """
        Sends message to speaker.bot websocket using standart setup
        @param message: the message you want to have spoken
        @param verbose: set to true if debugging info is wanted
        """

        await open_websocket(self.speaker_alias, message, verbose)
