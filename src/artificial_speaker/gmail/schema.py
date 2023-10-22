from pydantic import BaseModel


class GmailMessageSchema(BaseModel):
    message_id: str
    title: str
    receiver: str
    sender: str
    date: str
    url: str
    content: str

