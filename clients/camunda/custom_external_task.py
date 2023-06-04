from custom_variables import CustomVariables
from custom_task_result import CustomTaskResult
from camunda.variables.properties import Properties
from camunda.external_task.external_task import ExternalTask


class CustomExternalTasks(ExternalTask):
    def __init__(self, context):
        self._context = context
        self._variables = CustomVariables(context.get("variables", {}))
        self._task_result = CustomTaskResult.empty_task_result(task=self)
        self._extProperties = Properties(context.get("extensionProperties", {}))

    def extend_lock(self, new_duration: int):
        self._task_result = CustomTaskResult.extend_lock(self, new_duration)
        return self._task_result