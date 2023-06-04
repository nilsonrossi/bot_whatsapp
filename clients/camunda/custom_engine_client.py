import requests
from camunda.client.engine_client import EngineClient
from camunda.utils.response_utils import raise_exception_if_not_ok
from custom_variables import CustomVariables


class CustomEngineClient(EngineClient):
    def correlate_message(
        self,
        message_name,
        process_instance_id=None,
        tenant_id=None,
        business_key=None,
        process_variables=None,
        correlationKeys=None,
    ):
        """
        Correlates a message to the process engine to either trigger a message start event or
        an intermediate message catching event.
        :param message_name:
        :param process_instance_id:
        :param tenant_id:
        :param business_key:
        :param process_variables:
        :return: response json
        """
        url = f"{self.engine_base_url}/message"
        body = {
            "messageName": message_name,
            "resultEnabled": True,
            "processVariables": CustomVariables.format(process_variables) if process_variables else None,
            "processInstanceId": process_instance_id,
            "tenantId": tenant_id,
            "withoutTenantId": not tenant_id,
            "businessKey": business_key,
            "correlationKeys": CustomVariables.format(correlationKeys),
        }

        if process_instance_id:
            body.pop("tenantId")
            body.pop("withoutTenantId")

        body = {k: v for k, v in body.items() if v is not None}

        response = requests.post(url, headers=self._get_headers(), json=body)
        raise_exception_if_not_ok(response)
        return response.json()

    def set_instance_variable(self, variables, process_instance_id):
        url = f"{self.engine_base_url}/process-instance/variables-async"
        body = {"processInstanceIds": [process_instance_id], "variables": CustomVariables.format(variables)}
        response = requests.post(url, headers=self._get_headers(), json=body)
        raise_exception_if_not_ok(response)
        return response.json()

    def start_process(self, process_key, variables, tenant_id=None, business_key=None):
        """
        Start a process instance with the process_key and variables passed.
        :param process_key: Mandatory
        :param variables: Mandatory - can be empty dict
        :param tenant_id: Optional
        :param business_key: Optional
        :return: response json
        """
        url = self.get_start_process_instance_url(process_key, tenant_id)
        body = {"variables": CustomVariables.format(variables)}
        if business_key:
            body["businessKey"] = business_key

        response = requests.post(url, headers=self._get_headers(), json=body)
        raise_exception_if_not_ok(response)
        return response.json()
