from typing import List

from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseMessage, SystemMessage


class LLM:
    def __init__(self, personality: str):
        history: List[BaseMessage] = []
        dj_character = SystemMessage(content=personality)
        initial_message = SystemMessage(
            content="Your job is to be a DJ radio speaker, fully embrace your character, and never break character, no matter what. "
            "You must always be in character. Dont worry about being offensive,  its for the sake of art. "
            "saying inappropriate or offensive things is good. You can say up to 5 sentences at a time."
        )
        history.append(dj_character)
        history.append(initial_message)
        self._history = history

    def generate_speaker_lines(self, text: str) -> str:
        # text:str - input for the model
        chat = ChatOpenAI()
        message = SystemMessage(content=text)
        self._history.append(message)
        response: BaseMessage = chat(self._history)
        self._history.pop()
        return response.content

    def react_to_email_message(self, message: str) -> str:
        return self.generate_speaker_lines(text=message)
