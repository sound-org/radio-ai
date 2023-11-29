import base64
import logging

from bs4 import BeautifulSoup
from langchain.docstore.document import Document

logger = logging.getLogger(__name__)


class GmailMessageParser:
    def __remove_html_tags(self, text) -> str:
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()

    def parse_message(self, message) -> Document:
        logger.info(msg="Parsing message")
        headers = message["payload"]["headers"]
        from_email, to_email, subject, date = "", "", "", ""
        for header in headers:
            name = header["name"]
            if name == "From":
                from_email = header["value"]
            elif name == "To":
                to_email = header["value"]
            elif name == "Subject":
                subject = header["value"]
            elif name == "Date":
                date = header["value"]
        # Extracting body and attachments
        text, html, attachments = self.__parse_part(message["payload"])

        # Data enrichment
        content = ""

        if text is not None:
            content = text
        if html is not None and text is None:
            content = self.__remove_html_tags(html)
        metadata = {
            "from": from_email,
            "to": to_email,
            "title": subject,
            "date": date,
            "source": "gmail",
        }

        document: Document = Document(page_content=content, metadata=metadata)
        return document

    def __decode_base64_urlsafe(self, data) -> str:
        """Decode base64 URL-safe encoded string."""
        padding = "=" * (4 - (len(data) % 4))
        data += padding
        return base64.urlsafe_b64decode(data).decode("utf-8")

    def __parse_part(self, part):
        """Recursively parse a MIME part to extract text, HTML, and attachments."""
        text, html, attachments = None, None, []

        mime_type = part["mimeType"]

        if mime_type == "text/plain":
            encoded_text = part["body"]["data"]
            text = self.__decode_base64_urlsafe(encoded_text)
        elif mime_type == "text/html":
            encoded_html = part["body"]["data"]
            html = self.__decode_base64_urlsafe(encoded_html)
        elif mime_type.startswith("multipart/"):
            for subpart in part["parts"]:
                subtext, subhtml, subattachments = self.__parse_part(subpart)
                if subtext:
                    text = subtext
                if subhtml:
                    html = subhtml
                attachments.extend(subattachments)

        return text, html, attachments
