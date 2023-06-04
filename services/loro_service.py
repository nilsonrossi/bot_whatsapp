import os

from clients.camunda.custom_engine_client import CustomEngineClient
from connection import get_connection
from dao.customer_dao import CustomerDAO
from dao.flow_dao import FlowDAO
from models.customer_model import CustomerModel
from models.flow_model import FlowModel
from schema import Message

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


class LoroService:
    def __init__(self, message_model: Message):
        self.message_model = message_model
        self.camunda_client = CustomEngineClient(engine_base_url=CAMUNDA_URL)

    def _create_workflow_payload(self):
        return {"message": {"body": self.message_model.body, "type": self.message_model.message_type}}

    def process_message(self):
        flow_payload = self._create_workflow_payload()
        with get_connection() as conn:
            customer: CustomerModel = CustomerDAO(conn).get_or_create_customer(
                self.message_model.phone_number, self.message_model.profile_name
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
