import base64
import logging

from bs4 import BeautifulSoup
from langchain.docstore.document import Document

logger = logging.getLogger(__name__)


class GmailMessageParser:
    """
    A class that parses Gmail messages and extracts relevant information.

    Methods:
        parse_message(message) -> Document: Parses a Gmail message and returns a Document object.
    """

    def _remove_html_tags(self, text) -> str:
        soup = BeautifulSoup(text, "html.parser")
        return soup.get_text()

    def parse_message(self, message) -> Document:
        """
        Parses a Gmail message and returns a Document object.

        Args:
            message: The Gmail message to be parsed.

        Returns:
            Document: The parsed document containing the extracted content and metadata.
        """
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
        text, html, attachments = self._parse_part(message["payload"])

        # Data enrichment
        content = ""

        if text is not None:
            content = text
        if html is not None and text is None:
            content = self._remove_html_tags(html)
        metadata = {
            "from": from_email,
            "to": to_email,
            "title": subject,
            "date": date,
            "source": "gmail",
        }

        document: Document = Document(page_content=content, metadata=metadata)
        return document

    def _decode_base64_urlsafe(self, data) -> str:
        """Decode base64 URL-safe encoded string."""
        padding = "=" * (4 - (len(data) % 4))
        data += padding
        return base64.urlsafe_b64decode(data).decode("utf-8")

    def _parse_part(self, part):
        """Recursively parse a MIME part to extract text, HTML, and attachments."""
        text, html, attachments = None, None, []

        mime_type = part["mimeType"]

        if mime_type == "text/plain":
            encoded_text = part["body"]["data"]
            text = self._decode_base64_urlsafe(encoded_text)
        elif mime_type == "text/html":
            encoded_html = part["body"]["data"]
            html = self._decode_base64_urlsafe(encoded_html)
        elif mime_type.startswith("multipart/"):
            for subpart in part["parts"]:
                subtext, subhtml, subattachments = self._parse_part(subpart)
                if subtext:
                    text = subtext
                if subhtml:
                    html = subhtml
                attachments.extend(subattachments)

        return text, html, attachments
