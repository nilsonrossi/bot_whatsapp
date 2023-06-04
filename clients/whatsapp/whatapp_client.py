import logging

from settings import settings
from support.http import http

logger = logging.getLogger("whatsapp_client")


class WhatsAppClient:
    def __init__(self, phone_number_id: str):
        self.phone_number_id = phone_number_id
        self.base_url = "https://graph.facebook.com/v17.0"
        self.url = f"{self.base_url}/{phone_number_id}/messages"
        self.headers = {"Content-Type": "application/json", "Authorization": f"Bearer {settings.WHATSAPP_API_TOKEN}"}

    def send_text_message(self, to: str, message: str, preview_url: bool = False):
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"preview_url": preview_url, "body": message},
        }
        logging.info(f"Sending message to {to}")
        response = http.post(f"{self.url}", headers=self.headers, json=data)
        return response.json()

    def mark_as_read(self, message_id: str) -> dict:
        payload = {"messaging_product": "whatsapp", "status": "read", "message_id": message_id}
        response = http.post(f"{self.url}", headers=self.headers, json=payload)
        return response.json()

    def react_message(self, message_id: str, to: str, emoji: str = "👍"):
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "reaction",
            "reaction": {"message_id": message_id, "emoji": emoji},
        }
        response = http.post(f"{self.url}", headers=self.headers, json=payload)
        return response.json()
