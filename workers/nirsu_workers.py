import logging
import sys
from concurrent.futures import ThreadPoolExecutor

from clients.camunda.custom_external_task import CustomExternalTasks
from clients.camunda.custom_external_task_worker import CustomExternalTaskWorker
from clients.camunda.custom_task_result import CustomTaskResult
from clients.camunda.decorator import worker
from clients.whatsapp.whatapp_client import WhatsAppClient
from connection import get_connection
from dao.customer_dao import CustomerDAO
from dao.flow_dao import FlowDAO
from models.customer_model import CustomerModel
from settings import settings

logger = logging.getLogger("loro_workers")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


default_config = {
    "maxTasks": 1,
    "lockDuration": 60000,
    "asyncResponseTimeout": 60000,
    "retries": 3,
    "retryTimeout": 5000,
    "sleepSeconds": 10,
    "isDebug": True,
}

whatsapp_client = WhatsAppClient(settings.WHATSAPP_PHONE_NUMBER_ID)


@worker
def process_audio(task: CustomExternalTasks) -> CustomTaskResult:
    logger.info("<process_audio> Processando o audio ...")
    variables = task.get_variables()
    logger.info(variables)
    return variables


@worker
def update_customer(task: CustomExternalTasks) -> CustomTaskResult:
    logger.info("<update_customer> Atualizando o cliente ...")
    variables = task.get_variables()
    logger.info(variables)
    customer = CustomerModel(**variables["customer"])
    gender_opt = variables["message"]["body"]
    with get_connection() as conn:
        CustomerDAO(conn).update_customer(customer.customer_id, gender_opt)
        conn.commit()
    variables["customer"]["gender_opt"] = gender_opt
    return variables


@worker
def finish_flow(task: CustomExternalTasks) -> CustomTaskResult:
    logger.info("<finish_flow> Finalizando o flow ...")
    variables = task.get_variables()
    logger.info(variables)
    with get_connection() as conn:
        FlowDAO(conn).finish_flow(instance_id=task.get_process_instance_id())
        conn.commit()
    return variables


@worker
def send_message(task: CustomExternalTasks) -> CustomTaskResult:
    variables = task.get_variables()
    properties = task.get_extension_properties()
    customer: CustomerModel = CustomerModel(**variables["customer"])
    logger.info(f"<send_message> Enviando mensagem para {customer.profile_name}({customer.phone_number}) ...")
    message = properties["message"].replace("\\n", "\n")
    results = whatsapp_client.send_text_message(customer.phone_number, message)
    logger.info(results)
    variables.setdefault("send_results", [])
    variables["send_results"].append({"task_id": task.get_activity_id(), "sid": ""})

    return variables


def run_worker(worker_name):
    worker = CustomExternalTaskWorker(worker_id="1", config=default_config)
    worker_func = getattr(sys.modules[__name__], worker_name)
    worker.subscribe(worker_name, worker_func)


worker_list = ["send_message", "update_customer", "process_audio", "finish_flow"]

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=30) as executor:
        executor.map(run_worker, worker_list)
