from typing import List

from twitchio.ext import commands

from . import credentials
from .chat import gpt3_completion
from .chattypes import Conversation
from .texttospeech import generate_audio_and_subtitle
from .utils import check_and_filter_user_message, open_file


CONVERSATION_LIMIT = 20


class Bot(commands.Bot):
    conversation: List[Conversation] = list()

    # Initialise our Bot with our access token, prefix and a list of channels
    # to join on boot...
    # prefix can be a callable, which returns a list of strings or a string...
    # initial_channels can also be a callable which returns a list of strings.
    def __init__(self):
        Bot.conversation.append(
            {"role": "system", "content": open_file("prompt_chat.txt")}
        )
        super().__init__(
            token=credentials.TWITCH_TOKEN,
            prefix="!",
            initial_channels=[credentials.TWITCH_CHANNEL],
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
        print(f"{credentials.BOT_NAME}:", bot_response)

        conversation = {"role": "assistant", "content": bot_response}
        if Bot.conversation.count(conversation) == 0:
            Bot.conversation.append(conversation)

        if len(Bot.conversation) > CONVERSATION_LIMIT:
            Bot.conversation = Bot.conversation[1:]

        generate_audio_and_subtitle(user_question, bot_response)

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
