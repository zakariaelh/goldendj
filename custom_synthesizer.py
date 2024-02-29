from typing import Optional
import logging
from vocode.streaming.models.synthesizer import SynthesizerConfig, ElevenLabsSynthesizerConfig
from vocode.streaming.synthesizer.factory import SynthesizerFactory
import aiohttp
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.synthesizer.base_synthesizer import SynthesisResult
from vocode.streaming.synthesizer.eleven_labs_synthesizer import ElevenLabsSynthesizer
from vocode.streaming.utils.mp3_helper import decode_mp3

class CustomSynthesizerFactory(SynthesizerFactory):
    def create_synthesizer(
        self,
        synthesizer_config: SynthesizerConfig,
        logger: Optional[logging.Logger] = None,
        aiohttp_session: Optional[aiohttp.ClientSession] = None,
    ):
        if isinstance(synthesizer_config, ElevenLabsSynthesizerConfig):
            return Custom11LabsSynthesizer(
                synthesizer_config, logger=logger, aiohttp_session=aiohttp_session
            )
        else:
            super().create_synthesizer(
                synthesizer_config=synthesizer_config,
                logger=logger,
                aiohttp_session=aiohttp_session
            )

class Custom11LabsSynthesizer(ElevenLabsSynthesizer):
    async def create_speech(self, message: BaseMessage, chunk_size: int, bot_sentiment = None) -> SynthesisResult:
        if message.text == "xUVsfnaonfl":
            # this means it's the result of a song download 
            audio_data = open('audios/song.mp3', "rb").read()
            output_bytes_io = decode_mp3(audio_data)

            result = self.create_synthesis_result_from_wav(
                file=output_bytes_io,
                message=message,
                chunk_size=chunk_size,
            )
            return result
        else:
            res = await super().create_speech(message, chunk_size, bot_sentiment)
            return res 