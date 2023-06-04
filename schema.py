from dataclasses import dataclass

from fastapi import Form


@dataclass
class Message:
    body: str = Form(alias="Body", default=None)
    phone_number: str = Form(alias="From")
    profile_name: str = Form(alias="ProfileName")
    audio_url: str = Form(alias="MediaUrl0", default=None)

    @property
    def message_type(self):
        return "audio" if self.audio_url else "text"
