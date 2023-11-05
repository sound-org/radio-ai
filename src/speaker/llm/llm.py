from typing import List

from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseMessage, SystemMessage


class LLM:
    def __init__(self, personality: str):
        history: List[BaseMessage] = []
        dj_character = SystemMessage(content=personality)
        # initial_message = SystemMessage(content="Starting talking")
        history.append(dj_character)
        # history.append(initial_message)
        self._history = history

    def generate_speaker_lines(self, text: str) -> str:
        # text:str - input for the model
        chat = ChatOpenAI()
        message = SystemMessage(content=text)
        self._history.append(message)
        response: BaseMessage = chat(self._history)
        self._history.pop()
        return response.content
