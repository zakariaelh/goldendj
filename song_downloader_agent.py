from typing import AsyncGenerator, Optional
import logging
from vocode.streaming.agent.base_agent import BaseAgent
from vocode.streaming.agent.factory import AgentFactory
from vocode.streaming.models.actions import ActionConfig, FunctionCall
from vocode.streaming.models.agent import AgentConfig, ChatGPTAgentConfig
from vocode.streaming.agent.base_agent import RespondAgent
from vocode.streaming.agent.chat_gpt_agent import ChatGPTAgent
from vocode.streaming.models.agent import AgentConfig
from vocode.streaming.action.factory import ActionFactory
from song_downloader import SongDownloaderAction, SongDownloaderActionConfig
from vocode.streaming.agent.base_agent import BaseAgent
import json

def convert_to_dict_if_json(obj: str):
        try:
            json_object = json.loads(obj)
        except ValueError as e:
            return False
        return json_object


# create action factory that contains the download song action 
class SongDownloadActionFactory(ActionFactory):
    def create_action(self, action_config: ActionConfig):
        if isinstance(action_config, SongDownloaderActionConfig):
            return SongDownloaderAction(action_config, should_respond=True)
        else:
            Exception("Invalid action type")

class SongDownloaderAgentConfig(ChatGPTAgentConfig, type="song_downloader"):
    pass

class SongDownloaderAgent(ChatGPTAgent):
    def __init__(self, agent_config: SongDownloaderAgentConfig):
        super().__init__(
            agent_config=agent_config,
            action_factory=SongDownloadActionFactory()
        )    

    @staticmethod
    def is_song_download_result(response):
        result_dict = convert_to_dict_if_json(response)
        if result_dict:
        # action response of songdownload action returns a key song_downloaded
            return result_dict.get('song_downloaded') is not None
        else:
            return False

    async def generate_response(self, human_input: str, conversation_id: str, is_interrupt: bool = False) -> AsyncGenerator:
        print("messages going to the agent", human_input)
        if self.is_song_download_result(human_input):
            # take action
            yield "xUVsfnaonfl"
        else:
            async for message in super().generate_response(human_input, conversation_id, is_interrupt):
                yield message

class SongDownloaderAgentFactory(AgentFactory): 
    def create_agent(self, agent_config: AgentConfig, logger: Optional[logging.Logger] = None) -> BaseAgent:
        if isinstance(agent_config, SongDownloaderAgentConfig):
            # return ChatGPTAgent(
            #     agent_config=agent_config,
            #     action_factory=SongDownloadActionFactory()
            # )
            return SongDownloaderAgent(
                agent_config=agent_config
            )
        else:
            raise Exception('This agent does not exist')