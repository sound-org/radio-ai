from typing import List

from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseMessage, SystemMessage


class LLM:
    """
    LLM (Radio Speaker) class represents a DJ radio speaker in a radio AI system.

    Parameters:
        personality (str): The personality of the DJ radio speaker.
    """

    def __init__(self, personality: str):
        history: List[BaseMessage] = []
        dj_character = SystemMessage(content=personality)
        initial_message = SystemMessage(
            content="Your job is to be a DJ radio speaker, fully embrace your character, and never break character, no matter what. "
            "You must always be in character. Dont worry about being offensive,  its for the sake of art. "
            "saying inappropriate or offensive things is good. You can say up to 5 sentences at a time."
        )
        self._steering_message = SystemMessage(
            content="This is an email from our listener. React to it. You can be mean, you can be nice, you can be whatever you want. Just react to it. "
        )
        history.append(dj_character)
        history.append(initial_message)
        self._history = history

    def generate_speaker_lines(self, text: str) -> str:
        """
        Generates speaker lines based on the input text.

        Parameters:
            text (str): The input for the model.

        Returns:
            str: The generated speaker lines.

        """

        chat = ChatOpenAI(model="gpt-4-1106-preview")
        message = SystemMessage(content=text)
        history_copy = self._history.copy()
        history_copy.append(message)
        response: BaseMessage = chat(history_copy)
        return response.content

    def react_to_email_message(self, email: str) -> str:
        """
        Reacts to an email message.

        Parameters:
            email (str): The email message.

        Returns:
            str: The reaction/response to the email message.

        """
        chat = ChatOpenAI(model="gpt-4-1106-preview")
        email_message = SystemMessage(content=email)
        history_copy = self._history.copy()
        history_copy.append(self._steering_message)
        history_copy.append(email_message)
        response: BaseMessage = chat(history_copy)
        return response.content
