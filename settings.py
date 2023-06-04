import os


class Settings:
    # WhatsApp
    WHATSAPP_VERIFY_TOKEN: str
    WHATSAPP_PHONE_NUMBER_ID: str
    WHATSAPP_API_TOKEN: str

    # Twilio
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str

    def __init__(self):
        self.WHATSAPP_VERIFY_TOKEN = os.environ["WHATSAPP_VERIFY_TOKEN"]
        self.WHATSAPP_API_TOKEN = os.environ["WHATSAPP_API_TOKEN"]
        self.WHATSAPP_PHONE_NUMBER_ID = os.environ["WHATSAPP_PHONE_NUMBER_ID"]
        self.TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
        self.TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]


settings = Settings()
