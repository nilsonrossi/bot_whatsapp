import os

from clients.camunda.custom_engine_client import CustomEngineClient
from clients.whatsapp.whatapp_client import WhatsAppClient
from connection import get_connection
from dao.customer_dao import CustomerDAO
from dao.flow_dao import FlowDAO
from models.customer_model import CustomerModel
from models.flow_model import FlowModel
from models.webhook_message_model import WebhookMessageModel

default_config = {
    "maxTasks": 1,
    "lockDuration": 60000,
    "asyncResponseTimeout": 60000,
    "retries": 3,
    "retryTimeout": 5000,
    "sleepSeconds": 10,
    "isDebug": True,
}

CAMUNDA_URL = os.environ["CAMUNDA_URL"]


class NirsuService:
    def __init__(self, message_model: WebhookMessageModel, client: WhatsAppClient):
        self.message_model = message_model
        self.client = client
        self.camunda_client = CustomEngineClient(engine_base_url=CAMUNDA_URL)

    def _create_workflow_payload(self):
        return {"message": {"body": self.message_model.message_content, "type": self.message_model.message_type}}

    def process_message(self):
        self.is_message()

    def is_message(self):
        if not self.message_model.is_message:
            return
        # self.client.mark_as_read(self.message_model.message_id)
        # self.client.react_message(self.message_model.message_id)
        flow_payload = self._create_workflow_payload()
        with get_connection() as conn:
            customer: CustomerModel = CustomerDAO(conn).get_or_create_customer(
                phone_number=self.message_model.phone_number, profile_name=self.message_model.profile_name
            )

            flow_dao = FlowDAO(conn)
            flow: FlowModel = flow_dao.get_or_create_flow(self.message_model.phone_number, customer)

            flow_payload["customer"] = customer.dict()
            if flow.is_new:
                resp_json = self.camunda_client.start_process(process_key="bot", variables=flow_payload)
                flow_dao.set_instance_id(flow.flow_id, resp_json["id"])
            else:
                resp_json = self.camunda_client.correlate_message(
                    "new_message", process_instance_id=flow.instance_id, process_variables=flow_payload
                )
            print(resp_json)
            conn.commit()
