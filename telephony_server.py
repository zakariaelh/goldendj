# Standard library imports
import logging
import os

from vocode.streaming.models.telephony import TwilioConfig
from vocode.streaming.telephony.config_manager.in_memory_config_manager import InMemoryConfigManager

from vocode.streaming.models.message import BaseMessage
from vocode.streaming.telephony.server.base import (
    TwilioInboundCallConfig,
    TelephonyServer,
)
from dotenv import load_dotenv

# Local application/library specific imports
from vocode.streaming.models.synthesizer import *
from vocode.streaming.telephony.constants import DEFAULT_AUDIO_ENCODING, DEFAULT_SAMPLING_RATE

# agent specific imports 
from song_downloader import SongDownloaderActionConfig
from song_downloader_agent import SongDownloaderAgentConfig, SongDownloaderAgentFactory
from custom_synthesizer import CustomSynthesizerFactory


# if running from python, this will load the local .env
# docker-compose will load the .env file by itself
load_dotenv()

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

config_manager = InMemoryConfigManager()

BASE_URL = os.getenv("BASE_URL")
VOICE_ID =  None # "nDLkfhgP1msRF4o1WsQE"
INITIAL_MESSAGE = "Hello, how are you doing my friend?"
PROMPT = """
Initiate friendly conversation with an elderly user, focusing on their well-being, interests, and any music they might enjoy. Remember to keep the tone warm, respectful, and engaging. Ask about their day, any specific music they want to hear, and share a positive, uplifting message.
If they ask you to play a song, you will do a search using one of the tools passed to you. 
Suggest songs to user if they give something very broad.
When using the song downloader always give a song name and the artist !!!
if you're asked how you're doing reply that you're doing well and say something gentle.
"""

telephony = TelephonyServer(
    base_url=BASE_URL,
    config_manager=config_manager,
    inbound_call_configs=[
        TwilioInboundCallConfig(
            url="/inbound_call",
            agent_config=SongDownloaderAgentConfig(
                initial_message=BaseMessage(text=INITIAL_MESSAGE),
                prompt_preamble=PROMPT,
                model_name="gpt-4-0125-preview",
                actions=[
                    SongDownloaderActionConfig()
                ]
            ),
            twilio_config=TwilioConfig(
                account_sid=os.environ["TWILIO_ACCOUNT_SID"],
                auth_token=os.environ["TWILIO_AUTH_TOKEN"],
            ),
            synthesizer_config=ElevenLabsSynthesizerConfig(
                audio_encoding=DEFAULT_AUDIO_ENCODING,
                sampling_rate=DEFAULT_SAMPLING_RATE,
                voice_id=VOICE_ID
            ),
            logger=logger
        )
    ],
    agent_factory=SongDownloaderAgentFactory(),
    synthesizer_factory=CustomSynthesizerFactory(),
    logger=logger,
)