from http import HTTPStatus

import requests

from camunda.client.external_task_client import ExternalTaskClient
from camunda.utils.response_utils import raise_exception_if_not_ok
from camunda.utils.utils import str_to_list
from custom_variables import CustomVariables
from http_utils import http


class CustomExternalTaskClient(ExternalTaskClient):
    def _get_topics(self, topic_names, process_variables):
        return [
            {
                "topicName": topic,
                "lockDuration": self.config["lockDuration"],
                "processVariables": process_variables or {},
                "includeExtensionProperties": self.config.get("includeExtensionProperties") or False,
                "businessKey": self.config.get("businessKey"),
            }
            for topic in str_to_list(topic_names)
        ]

    def complete(self, task_id, global_variables, local_variables=None):
        # sourcery skip: class-extract-method
        local_variables = {} if local_variables is None else local_variables
        url = self.get_task_complete_url(task_id)

        body = {
            "workerId": self.worker_id,
            "variables": CustomVariables.format(global_variables),
            "localVariables": CustomVariables.format(local_variables)
        }

        response = http.post(url, headers=self._get_headers(), json=body, timeout=self.http_timeout_seconds)
        raise_exception_if_not_ok(response)
        return response.status_code == HTTPStatus.NO_CONTENT

    def extend_lock(self, task_id, new_duration: int):
        url = self.get_extend_lock_url(task_id)

        body = {
            "workerId": self.worker_id,
            "newDuration": new_duration
        }

        response = requests.post(url, headers=self._get_headers(), json=body, timeout=self.http_timeout_seconds)
        raise_exception_if_not_ok(response)
        return response.status_code == HTTPStatus.NO_CONTENT

    def get_extend_lock_url(self, task_id):
        return f"{self.external_task_base_url}/{task_id}/extendLock"

    def lock(self, task_id, new_duration: int):
        url = self.get_lock_url(task_id)

        body = {
            "workerId": self.worker_id,
            "lockDuration": new_duration
        }

        response = requests.post(url, headers=self._get_headers(), json=body, timeout=self.http_timeout_seconds)
        raise_exception_if_not_ok(response)
        return response.status_code == HTTPStatus.NO_CONTENT

    def get_lock_url(self, task_id):
        return f"{self.external_task_base_url}/{task_id}/lock"

    def get_extend_lock_url(self, task_id):
        return f"{self.external_task_base_url}/{task_id}/extendLock"

    def get_task(self, task_id):
        url = self.get_task_url(task_id)

        response = requests.get(url, headers=self._get_headers(), timeout=self.http_timeout_seconds)
        raise_exception_if_not_ok(response)
        return response.status_code == HTTPStatus.NO_CONTENT

    def get_task_url(self, task_id):
        return f"{self.external_task_base_url}/{task_id}"
