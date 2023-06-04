import logging
import time
from typing import Callable

from camunda.client.external_task_client import ENGINE_LOCAL_BASE_URL
from camunda.external_task.external_task_worker import ExternalTaskWorker
from camunda.utils.utils import get_exception_detail
from custom_external_task import CustomExternalTasks
from custom_external_task_client import CustomExternalTaskClient
from custom_external_task_executor import CustomExternalTaskExecutor
from custom_task_result import CustomTaskResult

logger = logging.getLogger("camunda")
logger.setLevel(logging.DEBUG)


class NoExternalTaskFound(Exception):
    pass


class BpmnError(Exception):
    def __init__(self, error_code: str, error_message: str):
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(self.error_message)


def worker(task_function: Callable):
    def worker_wrapper(task: CustomExternalTasks) -> CustomTaskResult:
        try:
            result = task_function(task)
            return task.complete(result)
        except BpmnError as e:
            return task.bpmn_error(error_code=e.error_code, error_message=e.error_message)
        except Exception as e:
            logger.warning(str(e))
            return task.failure(error_message="task failed",  error_details=str(e), max_retries=0, retry_timeout=5000)
    return worker_wrapper


class CustomExternalTaskWorker(ExternalTaskWorker):
    def __init__(self, worker_id, base_url=ENGINE_LOCAL_BASE_URL, config=None):
        config = config if config is not None else {}  # To avoid to have a mutable default for a parameter
        self.worker_id = worker_id
        self.client = CustomExternalTaskClient(self.worker_id, base_url, config)
        self.executor = CustomExternalTaskExecutor(self.worker_id, self.client)
        self.config = config
        self._log_with_context(f"Created new External Task Worker with config: {self.config}")

    def _parse_response(self, resp_json, topic_names, process_variables):
        tasks = []
        if resp_json:
            for context in resp_json:
                task = CustomExternalTasks(context)
                tasks.append(task)

        tasks_count = len(tasks)
        self._log_with_context(f"{tasks_count} External task(s) found for "
                               f"Topics: {topic_names}, Process variables: {process_variables}")
        return tasks