from typing import List

from langchain.docstore.document import Document

from .schema import GmailMessageSchema


def convert_gmail_message_model_to_schema(
    gmail_message: Document,
) -> GmailMessageSchema:
    return GmailMessageSchema(
        message_id=gmail_message.metadata["message_id"],
        title=gmail_message.metadata["title"],
        receiver=gmail_message.metadata["to"],
        sender=gmail_message.metadata["from"],
        date=gmail_message.metadata["date"],
        # NOTE: one caveat: this will work if message with given id belongs to user's
        # primary google account (eg. I'm logged into 3 different accounts, and can't
        # open message with that link, since ai.startup.ai account is my 3rd google account)
        url=f"https://mail.google.com/mail/u/0/#all/{gmail_message.metadata['message_id']}",
        content=gmail_message.page_content,
    )


def convert_gmail_messages_model_to_schema(
    gmail_messages: List[Document],
) -> List[GmailMessageSchema]:
    return [
        convert_gmail_message_model_to_schema(gmail_message=gmail_message)
        for gmail_message in gmail_messages
    ]
