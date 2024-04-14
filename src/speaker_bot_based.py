import threading

from twitchio.ext import commands  # type: ignore

from .credentials import TWITCH_CHANNEL, TWITCH_TOKEN
from .logger import Logger
from .queue_consumer import QueueConsumer


class Bot(commands.Bot):

    def __init__(
        self, consumer: QueueConsumer, logger: Logger, no_command: bool = False
    ):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...  # noqa: E501
        # prefix can be a callable, which returns a list of strings or a string...  # noqa: E501
        # initial_channels can also be a callable which returns a list of strings...  # noqa: E501
        self.logger = logger
        self.logger.passingblue("Spawning Bot")
        self.queueConsumer = consumer
        self.no_command = no_command
        super().__init__(
            token=TWITCH_TOKEN,
            prefix="?",
            initial_channels=[TWITCH_CHANNEL],
        )

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        self.logger.passing(f"Logged in as | {self.nick}")
        self.queueConsumer.nick = self.nick
        await self.updateStreamInfo()

    # returns true if response should be given

    async def updateStreamInfo(self):
        ch = await self.fetch_channel(self.nick)
        game = ch.game_name
        title_parts = ch.title.split("|")
        title = title_parts[0]
        self.queueConsumer.setStreamInfo(game, title)

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        self.logger.info("Message recieved:")

        # if message.echo:
        #    return
        if message.author.name == self.nick:

            if "!reload_prompt" in message.content:
                self.logger.warning("Reloading prompt")

                await self.queueConsumer.reload_prompt()
                return

            if "!toggle_verbose" in message.content:
                self.logger.warning("Toggling Verbosity")

                await self.queueConsumer.toggle_verbosity()
                return

            if "!clear_conv" in message.content:
                self.logger.warning("Clearing Conversation")

                await self.queueConsumer.clear_conv()
                return

            if "!update_info" in message.content:
                self.logger.warning("Updating Info")
                await self.updateStreamInfo()
                await self.queueConsumer.reload_prompt()
                return

            if "!reload_all" in message.content:
                self.logger.warning("Reloading everything")
                await self.updateStreamInfo()
                await self.queueConsumer.reload_prompt()
                await self.queueConsumer.clear_conv()
                return

        msg = f"{message.author.name}:  {message.content}"
        self.logger.info(msg)
        await self.queueConsumer.put_message(message)

        await self.handle_commands(message)


if __name__ == "__main__":

    logger = Logger(
        console_log=True,
        file_logging=True,
        file_URI="logs/logger.txt",
        override=True,
    )

    consumer = QueueConsumer(logger=logger, verbose=True, answer_rate=20)
    bot = Bot(consumer, logger)
    process = threading.Thread(target=consumer.run)
    process.start()

    bot.run()
    process.join()
