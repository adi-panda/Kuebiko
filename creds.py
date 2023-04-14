from decouple import config as environ  # type: ignore

# You're Twitch Token
TWITCH_TOKEN = str(environ("TWITCH_TOKEN", ""))
# Your TWITCH Channel Name
TWITCH_CHANNEL = str(environ("TWITCH_CHANNEL", ""))
# Your OpenAI API Key
OPENAI_API_KEY = str(environ("OPENAI_API_KEY", ""))
# Your Google Cloud JSON Path
GOOGLE_JSON_PATH = str(environ("GOOGLE_JSON_PATH", ""))
