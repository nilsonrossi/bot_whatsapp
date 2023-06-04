from camunda.external_task.external_task import TaskResult


class CustomTaskResult(TaskResult):
    def __init__(
        self,
        task,
        success=False,
        new_duration=60000,
        global_variables=None,
        local_variables=None,
        bpmn_error_code=None,
        error_message=None,
        error_details=None,
        retries=0,
        retry_timeout=300000
    ):
        if global_variables is None:
            global_variables = {}
        if local_variables is None:
            local_variables = {}
        if error_details is None:
            error_details = {}
        self.task = task
        self.success_state = success
        self.new_duration = new_duration
        self.global_variables = global_variables
        self.local_variables = local_variables
        self.bpmn_error_code = bpmn_error_code
        self.error_message = error_message
        self.error_details = error_details
        self.retries = retries
        self.retry_timeout = retry_timeout


    @classmethod
    def extend_lock(cls, task, new_duration):
        return CustomTaskResult(
            task,
            success=False,
            new_duration=new_duration
        )