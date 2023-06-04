import logging
import sys
import traceback
from typing import Callable

from clients.camunda.custom_external_task import CustomExternalTasks
from clients.camunda.custom_task_result import CustomTaskResult

logger = logging.getLogger("camunda_workers")
logger.setLevel(logging.DEBUG)


class WorkerError(Exception):
    def __init__(self, error_code: str, error_message: str):
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(self.error_message)


def worker(task_function: Callable):
    def worker_wrapper(task: CustomExternalTasks) -> CustomTaskResult:
        try:
            result = task_function(task)
            return task.complete(result)
        except WorkerError as e:
            return task.bpmn_error(error_code=e.error_code, error_message=e.error_message)
        except Exception as e:
            logger.error(e, exc_info=True)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error_details = "\n".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
            return task.failure(
                error_message="Erro ao executar a task", error_details=error_details, max_retries=0, retry_timeout=5000
            )

    return worker_wrapper
