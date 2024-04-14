import asyncio
import random
import time
from asyncio import Queue
from typing import List

from .chat import gpt3_completion
from .chattypes import ChatCompletionMessage, CustomMessage
from .json_handler import read_json_file
from .logger import Logger
from .utils import open_file
from .websocket import connect_websocket

CONVERSATION_LIMIT = 40


class QueueConsumer:

    def __init__(
        self,
        logger: Logger,
        speaker_bot_port: int = 7580,
        speaker_alias: str = "Default",
        no_command: bool = False,
        verbose: bool = False,
        answer_rate: int = 30,
    ) -> None:

        self.logger = logger
        self.logger.passing("Spawning Consumer")
        self.verbose = verbose
        self.nick = ""
        self.system_prompt: ChatCompletionMessage = {
            "role": "system",
            "content": open_file("prompt_chat.txt"),
        }
        self.conversation: List[ChatCompletionMessage] = list()
        self.queue: Queue[CustomMessage] = Queue()
        self.no_command = no_command
        self.port = speaker_bot_port
        self.speaker_alias = speaker_alias
        self.answer_rate = answer_rate
        pass

    def run(self):
        self.logger.passing("starting consumer")
        asyncio.run(self.main())

    async def main(self):
        self.logger.passing("consumer started")

        json_file = read_json_file("filter.json")
        bad_words = json_file["blacklist"] if json_file else {}
        ignored_users = json_file["ignored_users"] if json_file else {}

        try:
            while True:

                if not self.queue.empty():
                    message = await self.queue.get()
                    msg_author = message.author
                    msg_content = message.content
                    msg_platform = message.plattform
                    if any(bad_word in msg_content for bad_word in bad_words):
                        self.logger.warning(
                            f"Found blacklisted word in message {msg_content} from {msg_author} on {msg_platform}"  # noqa: E501
                        )
                        continue
                    if any(user == msg_author for user in ignored_users):
                        self.logger.warning(
                            f"Message ignored, user on ignore list: {msg_author}"  # noqa: E501
                        )
                        continue

                    if not await self.check_completion(
                        message
                    ):  # checks for already answered messages
                        await self.request_completion(
                            message
                        )  # requests chatGPT completion
                        await asyncio.sleep(len(message.content) / 10)
                        continue
                await self.youtube_chat()  # check for new Youtube chat messages  # noqa: E501
                await self.voice_control()  # check for new Voice commands

        except Exception as e:
            self.logger.fail(f"Exception in main loop: {e}")

    async def voice_control(self):

        await self.file2queue("streamer_exchange.txt", "Stream")

    async def youtube_chat(self):

        await self.file2queue("chat_exchange.txt", "YouTube")

    async def file2queue(self, file_uri: str, plattform: str):
        file_contents = open_file(file_uri)
        if len(file_contents) < 1:
            return
        lines = file_contents.split("\n")
        for line in lines:
            if len(line) < 1:
                continue
            contents = line.split(";msg:")
            msg = CustomMessage(contents[0], contents[1], plattform)
            msg.answer = await self.response_decision(msg)
            await self.queue.put(msg)

        self.delete_file_contents(file_uri)

        self.logger.userReply(msg.author, msg.plattform, msg.content)

    def delete_file_contents(self, file_path: str):
        try:
            # Open the file in write mode, which truncates the file
            with open(file_path, "w"):
                pass  # Using pass to do nothing inside the with block
            msg_passing = "Contents of '{}' have been deleted.".format(
                file_path,
            )
            self.logger.passing(msg_passing)
        except IOError:
            msg_error = "Unable to delete contents of '{}'.".format(file_path)
            self.logger.error(msg_error)

    async def put_message(
        self, message
    ):  # Only for twitch Message Objects! Not custom message
        author = message.author.name
        msg = message.content

        new_msg = CustomMessage(author, msg, "Twitch")
        new_msg.answer = await self.response_decision(new_msg)
        await self.queue.put(new_msg)

    async def reload_prompt(self):
        self.logger.passingblue("Reloading Prompt")
        self.system_prompt = {
            "role": "system",
            "content": open_file("prompt_chat.txt"),
        }

    async def toggle_verbosity(self):
        self.verbose = not self.verbose
        self.logger.passingblue(f"Verbosity is now: {self.verbose}")

    async def clear_conv(self):
        self.logger.passingblue("Clearing Conversations")
        self.conversation = list()

    async def check_completion(self, message: CustomMessage):

        for c in self.conversation:
            if c["content"] == message.content:
                return True

        return False

    async def request_completion(self, message: CustomMessage):

        # Check if the message is too long or short
        if len(message.content) > 150:
            self.logger.warning("Message ignored: Too long")
            return
        if len(message.content) < 6:
            self.logger.warning("Message ignored: Too short")
            return

        self.logger.warning("--------------\nMessage being processed")
        self.logger.userReply(
            message.author,
            message.plattform,
            message.content,
        )
        self.logger.info(self.conversation, printout=self.verbose)
        n: str = message.author
        cleaned_name = n.replace("_", " ")

        content = message.content.encode(
            encoding="ASCII",
            errors="ignore",
        ).decode()
        self.conversation.append(
            {
                "role": "user",
                "content": f"{cleaned_name} on {message.plattform}: {content}",
            }
        )

        self.logger.info(content, printout=self.verbose)

        if not message.answer:
            self.logger.info(
                "Message appended, not answering",
                printout=self.verbose,
            )
            return
        response: str = gpt3_completion(
            self.system_prompt,
            self.conversation,
            self.logger,
            verbose=self.verbose,
        )
        response = response.replace(
            "_", " "
        )  # replace _ with SPACE to make TTS less jarring

        # All of the following checks are dependend on your prompt
        if response.startswith(f"{self.speaker_alias}:"):
            response = response.replace(
                f"{self.speaker_alias}", ""
            )  # sometimes Sally: shows up
        if response.startswith(f"{self.speaker_alias} on Twitch:"):
            response = response.replace(
                f"{self.speaker_alias} on Twitch:", ""
            )  # don't even...
        if response.startswith(f"{self.speaker_alias} on YouTube:"):
            response = response.replace(
                f"{self.speaker_alias} on YouTube:",
                "",
            )
        if response.startswith(f"{self.speaker_alias} on Stream:"):
            response = response.replace(f"{self.speaker_alias} on Stream:", "")

        self.logger.botReply(self.speaker_alias, response)

        await self.speak(response)

        role_assistant: ChatCompletionMessage = {
            "role": "assistant",
            "content": str(response),
        }
        if self.conversation.count(role_assistant) == 0:
            self.conversation.append(role_assistant)

        if len(self.conversation) > CONVERSATION_LIMIT:
            self.conversation = self.conversation[1:]

        time.sleep(len(response) / 10)

        self.logger.warning(
            "Cooldown ended, waiting for next message...\n--------------"
        )

    async def response_decision(self, msg: CustomMessage) -> bool:
        if self.no_command:
            self.logger.info("No Command flag set")
            return True

        if self.speaker_alias in msg.content.lower():
            self.logger.info(f"{self.speaker_alias} in msg")
            return True

        if "!response" in msg.content.lower():
            self.logger.info("Command in msg")
            return True

        if (
            random.randint(1, 100) < self.answer_rate
        ):  # respond to 30% of messages anyway
            self.logger.info("Random trigger")
            return True

        if self.nick in msg.author:
            self.logger.info(f"{self.nick} in msg")
            return True

        self.logger.warning("Discarding message")
        return False

    def setStreamInfo(self, game, title):
        self.logger.passing(
            f'Setting stream info to "{title}" playing "{game}"',
        )
        self.system_prompt["content"] = (
            self.system_prompt["content"]
            .replace("STREAM_TITLE", title)
            .replace("GAME_NAME", game)
        )

    async def speak(self, message):

        id = random.randrange(10000, 99999)

        data = {
            "request": "Speak",
            "id": f"{id}",
            "voice": f"{self.speaker_alias}",
            "message": f"{message}",
        }

        self.logger.info(f"Sending Packet with ID {id}")

        await self.send_json_via_websocket(data)

    async def send_json_via_websocket(self, json_data):
        websockets_url = f"ws://localhost:{self.port}"
        await connect_websocket(websockets_url, json_data, self.logger)
