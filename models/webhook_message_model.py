from typing import Optional, Union

from pydantic import BaseModel, Field


class ProfileModel(BaseModel):
    name: str = Field(description="The customer's name.")


class ContactsModel(BaseModel):
    wa_id: str = Field(description="The customer's WhatsApp ID. A business can respond to a customer using this ID.")
    profile: ProfileModel


class MetadataModel(BaseModel):
    display_phone_number: str = Field(description="The phone number that is displayed for a business.")
    phone_number_id: str = Field(
        description="ID for the phone number. A business can respond to a message using this ID."
    )


class ErrorDetailModel(BaseModel):
    detail: str = Field(description="Describes the error.")


class ErrorMessageModel(BaseModel):
    code: int = Field(description="Error code. Example: 130429")
    title: str = Field(description="Error code title. Example: Rate limit hit")
    message: str = Field(description="Error code message. For example: (#130429) Rate limit hit")
    error_data: ErrorDetailModel


class ErrorModel(BaseModel):
    code: int = Field(description="Example: 130429.")
    title: str = Field(description="Error code title.")
    message: str
    error_data: ErrorDetailModel


class StatusesModel(BaseModel):
    id_: str = Field(
        alias="id",
        description="The ID for the message that the business that is subscribed to the webhooks sent to a customer",
    )
    recipient_id: str = Field(
        description="""
            The WhatsApp ID for the customer that the business, that is subscribed to the webhooks,
            sent to the customer
        """
    )
    status: str
    timestamp: int = Field(description="Date for the status message")
    errors: Optional[list[ErrorMessageModel]]


class AudioMessageModel(BaseModel):
    id_: str = Field(alias="id", description="ID for the audio file.")
    mime_type: str = Field(description="Mime type of the audio file.")


class ButtonMessageModel(BaseModel):
    payload: str = Field(
        description="""
            The payload for a button set up by the business that a customer clicked as part of an interactive message.
        """
    )
    text: str = Field(description="Button text.")


class ReferedProductModel(BaseModel):
    catalog_id: str = Field(
        description="Unique identifier of the Meta catalog linked to the WhatsApp Business Account."
    )
    product_retailer_id: str = Field(description="Unique identifier of the product in a catalog.")


class ContextMessageModel(BaseModel):
    id_: str = Field(default=None, alias="id", description="The message ID for the sent message for an inbound reply.")
    forwarded: bool = Field(
        default=False, description="Set to true if the message received by the business has been forwarded."
    )
    frequently_forwarded: bool = Field(
        default=False,
        description="Set to true if the message received by the business has been forwarded more than 5 times.",
    )
    from_: str = Field(
        default=None, alias="from", description="The WhatsApp ID for the customer who replied to an inbound message."
    )
    referred_product: Optional[ReferedProductModel]


class DocumentMessageModel(BaseModel):
    id_: str = Field(alias="id", description="ID for the document.")
    caption: str = Field(default=None, description="Caption for the document, if provided")
    filename: str = Field(description="Name for the file on the sender's device.")
    sha256: str = Field(description="SHA 256 hash.")
    mime_type: str = Field(description="Mime type of the document file.")


class IdentityMessageModel(BaseModel):
    acknowledged: str = Field(description="State of acknowledgment for the messages system customer_identity_changed.")
    created_timestamp: str = Field(
        description="""
            The time when the WhatsApp Business Management API detected the customer may have changed
            their profile information.
        """
    )
    hash_: str = Field(description="The ID for the messages system customer_identity_changed")


class ImageMessageModel(BaseModel):
    id_: str = Field(alias="id", description="ID for the image.")
    caption: str = Field(default=None, description="Caption for the image, if provided.")
    sha256: str = Field(description="Image hash.")
    mime_type: str = Field(description="Mime type for the image.")


class ButtonReplyTypeModel(BaseModel):
    id_: str = Field(alias="id", description="Unique ID of a button.")
    title: str = Field(description="Title of a button.")


class ListReplyTypeModel(BaseModel):
    id_: str = Field(alias="id", description="Unique ID of the selected list item.")
    title: str = Field(description="Title of the selected list item.")
    description: str = Field(description="Description of the selected row.")


class InteractiveTypeModel(BaseModel):
    button_reply: Optional[ButtonReplyTypeModel]
    list_reply: Optional[ListReplyTypeModel]


class InteractiveMessageModel(BaseModel):
    type_: InteractiveTypeModel


class OrderProductItemsModel(BaseModel):
    product_retailer_id: str = Field(description="Unique identifier of the product in a catalog.")
    quantity: str = Field(description="Number of items.")
    item_price: str = Field(description="Price of each item.")
    currency: str = Field(description="Price currency.")


class OrderMessageModel(BaseModel):
    catalog_id: str = Field(description="ID for the catalog the ordered item belongs to.")
    text: str = Field(description="Text message from the user sent along with the order.")
    product_items: list[OrderProductItemsModel]


class SystemMessageModel(BaseModel):
    body: str = Field(description="Describes the change to the customer's identity or phone number.")
    identity: str = Field(description="Hash for the identity fetched from server.")
    wa_id: str = Field(description="New WhatsApp ID for the customer when their phone number is updated.")
    customer: str = Field(description="The WhatsApp ID for the customer prior to the update.")
    type_change: str = Field(description="Type of system update.")


class VideoMessageModel(BaseModel):
    id_: str = Field(alias="id", description="The ID for the video.")
    caption: str = Field(default=None, description="The caption for the video, if provided.")
    filename: str = Field(description="The name for the file on the sender's device.")
    sha256: str = Field(description="The hash for the video.")
    mime_type: str = Field(description="The mime type for the video file.")


class StickerMessageModel(BaseModel):
    id_: str = Field(alias="id", description="ID for the sticker.")
    animated: bool = Field(description="Set to true if the sticker is animated; false otherwise.")
    sha256: str = Field(description="The hash for the sticker.")
    mime_type: str = Field(description=" image/webp.")


class TextMessageModel(BaseModel):
    body: str = Field(description="The text of the message.")


class MessageModel(BaseModel):
    id_: str = Field(alias="id", description="The ID for the message that was received by the business.")
    from_id: str = Field(alias="from", description="The customer's WhatsApp ID.")
    timestamp: str = Field(
        description="Unix timestamp indicating when the WhatsApp server received the message from the customer."
    )
    message_type: str = Field(
        alias="type",
        description="The type of message that has been received by the business that has subscribed to Webhooks.",
    )
    audio: Optional[AudioMessageModel]
    button: Optional[ButtonMessageModel]
    context: Optional[ContextMessageModel]
    document: Optional[DocumentMessageModel]
    errors: Optional[ErrorMessageModel]
    identity: Optional[IdentityMessageModel]
    image: Optional[ImageMessageModel]
    interactive: Optional[InteractiveMessageModel]
    order: Optional[OrderMessageModel]
    sticker: Optional[StickerMessageModel]
    system: Optional[SystemMessageModel]
    text: Optional[TextMessageModel]
    video: Optional[VideoMessageModel]


class ObjectModel(BaseModel):
    messaging_product: str = Field(description="Product used to send the message. Value is always whatsapp.")
    metadata: MetadataModel
    contacts: Optional[list[ContactsModel]]
    errors: Optional[list[ErrorModel]]
    messages: Optional[list[MessageModel]]
    statuses: Optional[list[StatusesModel]]


class ChangeModel(BaseModel):
    value: ObjectModel
    field: str = Field(description="Notification type")


class EntryModel(BaseModel):
    id_: str = Field(
        alias="id", description="The WhatsApp Business Account ID for the business that is subscribed to the webhook."
    )
    changes: list[ChangeModel]


class WebhookMessageModel(BaseModel):
    _object = Field(
        alias="object",
        description="The specific webhook a business is subscribed to. The webhook is whatsapp_business_account.",
    )
    entry: list[EntryModel]

    @property
    def is_message(self):
        return self.entry[0].changes[0].value.messages

    @property
    def message_content(self) -> Union[str, dict]:
        if self.message_type == "text":
            return self.entry[0].changes[0].value.messages[0].text.body
        elif self.message_type == "audio":
            return self.entry[0].changes[0].value.messages[0].audio.dict()

    @property
    def message_id(self):
        return self.entry[0].changes[0].value.messages[0].id_

    @property
    def is_status(self):
        return self.entry[0].changes[0].value.statuses

    @property
    def profile_name(self):
        return self.entry[0].changes[0].value.contacts[0].profile.name

    @property
    def phone_number(self):
        return self.entry[0].changes[0].value.contacts[0].wa_id

    @property
    def message_type(self):
        return self.entry[0].changes[0].value.messages[0].message_type
