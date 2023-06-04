from camunda.external_task.external_task_executor import ExternalTaskExecutor
from custom_task_result import CustomTaskResult


class CustomExternalTaskExecutor(ExternalTaskExecutor):
    def _handle_task_result(self, task_result):
        task = task_result.get_task()
        topic = task.get_topic_name()
        task_id = task.get_task_id()
        if task_result.is_success():
            self._handle_task_success(task_id, task_result, topic)
        elif task_result.is_bpmn_error():
            self._handle_task_bpmn_error(task_id, task_result, topic)
        elif task_result.is_failure():
            self._handle_task_failure(task_id, task_result, topic)
        elif task_result.is_extend_lock():
            self._handle_task_extend_lock(task_id, task_result, topic)
        else:
            err_msg = f"task result for task_id={task_id} must be either complete/failure/BPMNError/extendLock"
            self._log_with_context(err_msg, task_id=task_id, log_level='warning')
            raise Exception(err_msg)

    def _handle_task_extend_lock(self, task_id, task_result: CustomTaskResult, topic):
        self._log_with_context(f"Extending lock task Topic: {topic}", task_id)
        if self.external_task_client.extend_lock(task_id, task_result.new_duration):
            self._log_with_context(f"Extending lock task failed - Topic: {topic} task_result: {task_result}", task_id)
        else:
            self._log_with_context(f"Not able to extend task lock - Topic: {topic}", task_id=task_id)
            raise Exception(f"Not able to extend task lock for task_id={task_id} "
                            f"for topic={topic}, worker_id={self.worker_id}")