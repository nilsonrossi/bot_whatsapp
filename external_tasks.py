import logging
import sys
from concurrent.futures import ThreadPoolExecutor

from twilio.rest import Client

from bot_whatapp import dao
from bot_whatapp.app import get_connection
from custom_external_task import CustomExternalTasks
from custom_external_task_worker import CustomExternalTaskWorker
from custom_task_result import CustomTaskResult
from server import worker

logger = logging.getLogger("bot_whatsapp")
logger.setLevel(logging.DEBUG)


default_config = {
    "maxTasks": 1,
    "lockDuration": 60000,
    "asyncResponseTimeout": 60000,
    "retries": 3,
    "retryTimeout": 5000,
    "sleepSeconds": 10,
    "isDebug": True,
}

account_sid = "ACb759d51fbda66b9c0265a32f6ceff4dc"
auth_token = "a8e49aae941aea30263b92ca4ace522a"
twilio_client = Client(account_sid, auth_token)


@worker
def update_customer(task: CustomExternalTasks) -> CustomTaskResult:
    logger.info("<get_customer> Atualizando o cliente ...")
    variables = task.get_variables()
    customer = variables["customer"]
    gender_opt = int(variables["body"])
    logger.info(variables)
    with get_connection() as conn:
        dao.CustomerDAO(conn).update_customer(customer["customer_id"], gender_opt)
        conn.commit()
        customer["gender_opt"] = gender_opt
    return variables


@worker
def process_audio(task: CustomExternalTasks) -> CustomTaskResult:
    logger.info("<get_customer> Processando o audio ...")
    variables = task.get_variables()
    logger.info(variables)
    return variables


@worker
def finish_flow(task: CustomExternalTasks) -> CustomTaskResult:
    logger.info("<get_customer> Finalizando o flow ...")
    variables = task.get_variables()
    logger.info(variables)
    with get_connection() as conn:
        dao.FlowDAO(conn).finish_flow(instance_id=task.get_process_instance_id())
        conn.commit()
    return variables


@worker
def send_message(task: CustomExternalTasks) -> CustomTaskResult:
    variables = task.get_variables()
    properties = task.get_extension_properties()
    logger.info(f"<send_message> Enviando mensagem para {variables['profile_name']}({variables['phone_number']}) ...")
    message = properties["message"].replace("\\n", "\n")
    # logger.info(f" ====> {message}")
    results = twilio_client.messages.create(body=message, from_="whatsapp:+14155238886", to=variables["phone_number"])
    logger.info(results.sid)

    variables.setdefault("send_results", [])
    variables["send_results"].append({"task_id": task.get_activity_id(), "sid": results.sid})

    return variables


def run_worker(worker_name):
    worker = CustomExternalTaskWorker(worker_id="1", config=default_config)
    worker_func = getattr(sys.modules[__name__], worker_name)
    worker.subscribe(worker_name, worker_func)


worker_list = ["send_message", "update_customer", "process_audio", "finish_flow"]

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=30) as executor:
        executor.map(run_worker, worker_list)
    # results = twilio_client.messages.create(
    #     body="Olá! Sou a Loro AI! 😎😊\n\nTraduzo seus áudios em inglês e português no WhatsApp! 🎉🚀\n\nCom a Loro, você pode quebrar barreiras, se comunicando com pessoas em outros países sem ser fluente em inglês. Que maravilha, né?🤓💬\n\nEnvie seu áudio em inglês ou português e receba traduzidinho! 🎉\n\nSolte a voz - ou encaminhe um áudio - e veja a mágica acontecer! 🧙‍♀️💫",
    #     from_="whatsapp:+14155238886",
    #     to="whatsapp:+554899983088",
    # )
    # print(results)
