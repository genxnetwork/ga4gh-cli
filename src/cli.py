import os
import click
import json
import logging
from dotenv import dotenv_values
from .tes.tes_client import TES
from .aai.aai_client import AAI
from .utils import find_placeholders, replace_placeholders

class CLI:
    def __init__(self, config):
        self.config = config
        self.token = self.get_aai_instance().get_token()

    def _process_input_file(self, input_file, params):
        with open(input_file, 'r') as json_file:
            task = json.load(json_file)

        if params:
            params = dotenv_values(params)

        placeholders = find_placeholders(task)
        values = {}
        for placeholder in placeholders:
            value = params.get(placeholder) if params else None  # Try to get the value from the params
            if value is None:
                value = os.environ.get(placeholder)  # Try to get the value from the environment
                if value is None:
                    value = click.prompt(f"Enter value for {placeholder}", type=str)
            values[placeholder] = value

        return replace_placeholders(task, values)
    

    # AAI commands

    def get_aai_instance(self):
        try:
            base_url = self.config['AAI']['url']
            username = self.config['AAI']['username']
            password = self.config['AAI']['password']
        except KeyError:
            raise click.ClickException('Username and password keys must be present in the config file.')

        return AAI(base_url=base_url, username=username, password=password)

    def aai_login(self):
        self.token = self.get_aai_instance().login()
        if self.token:
            logging.info("Successfully logged in.")
        else:
            logging.error("Failed to log in.")


    # TES commands
            
    def get_tes_instance(self):
        return TES(
            base_url = self.config['TES']['base_url'], 
            username = self.config['TES']['username'], 
            password = self.config['TES']['password'], 
            token = self.token)

    def tes_create(self, task_file, params):
        print(task_file, params)
        task = self.get_tes_instance().create(self._process_input_file(task_file, params))
        if task:
            logging.info(f"Created Task ID: {task.get('id')}")
        else:
            logging.error("Failed to create task.")

    def tes_status(self, task_id, view, attest):
        if attest and view == 'MINIMAL': # MINIMAL view does not contain the measurement
            view = 'FULL'

        task = self.get_tes_instance().status(task_id, view)
        if not task:
            logging.error("Failed to retrieve task.")
            return

        if attest:
            # temporary workaround to get the required only measurement fields
            _task = {
                "id": task.get("id"),
                "state": task.get("state")
            }
            required_fields = [
                "x-ms-azurevm-osdistro", "x-ms-ver", "x-ms-azurevm-dbvalidated",
                "x-ms-azurevm-signingdisabled", "iss", "x-ms-azurevm-elam-enabled",
                "x-ms-policy-hash", "exp", "iat", "jti"
            ]
            _task = {
                "id": task.get("id"),
                "measurement": {field: task['teemeasurement'].get(field) for field in required_fields},
                "state": task.get("state")
            }
            
            # required_fields = {
            #     "alg": ["header", "alg"],
            #     "kid": ["header", "kid"],
            #     "iss": ["header", "iss"],
            #     "os_distro": ["payload", "x-ms-azurevm-osdistro"],
            #     "os_type": ["payload", "x-ms-azurevm-ostype"],
            #     "vm_id": ["payload", "x-ms-azurevm-vmid"]
            # }
            # for key, path in required_fields.items():
            #     value = task['teemeasurement']
            #     print(value)
            #     for p in path:
            #         print(p)
            #         value = value.get(p)
            #     _task['teemeasurement'][key] = value

            logging.info(_task)
        else:
            logging.info(task)

    def tes_list(self):
        """List all tasks from the TES server."""
        task_list = self.get_tes_instance().list()
        if task_list:
            tasks = task_list.get("tasks", [])
            for task in tasks:
                task_id = task.get('id')
                task_state = task.get('state')
                if task_id and task_state:
                    logging.info(f"Task ID: {task_id}, State: {task_state}")
                else:
                    logging.warning("Task ID or state missing.")
        else:
            logging.error("Failed to retrieve task list.")


    # WES commands

    def wes_create(self, workflow_file, params):
        raise NotImplementedError("WES create command is not implemented yet.")

    def wes_status(self, workflow_id, view, attest):
        logging.error("WES status command is not implemented yet.")
        raise NotImplementedError("WES status command is not implemented yet.")

    def wes_list(self):
        raise NotImplementedError("WES list command is not implemented yet.")
    
    # DRS commands

    def drs_get(self, object_id):
        raise NotImplementedError("DRS get command is not implemented yet.")

    def drs_put(self, object_file, params):
        raise NotImplementedError("DRS put command is not implemented yet.")

    def drs_delete(self, object_id):
        raise NotImplementedError("DRS delete command is not implemented yet.")

    def drs_list(self):
        raise NotImplementedError("DRS list command is not implemented yet.")
    

    # TRS commands

    def trs_get(self, tool_id):
        raise NotImplementedError("TRS get command is not implemented yet.")

    def trs_put(self, tool_file, params):
        raise NotImplementedError("TRS put command is not implemented yet.")

    def trs_delete(self, tool_id):
        raise NotImplementedError("TRS delete command is not implemented yet.")

    def trs_list(self):
        raise NotImplementedError("TRS list command is not implemented yet.")