import os
import click
import json
import logging
from dotenv import dotenv_values
from .tes.tes_client import TES
from .utils import find_placeholders, replace_placeholders

class CLI:
    def __init__(self, config):
        self.config = config

    def create_task(self, task_file, params):
        with open(task_file, 'r') as json_file:
            task = json.load(json_file)

        if params:
            params = dotenv_values(params)

        placeholders = find_placeholders(task)
        for placeholder in placeholders:
            value = params.get(placeholder) if params else None  # Try to get the value from the params
            if value is None:
                value = self.config.get(placeholder)  # Try to get the value from the config
                if value is None:
                    value = os.environ.get(placeholder)  # Try to get the value from the environment
                    if value is None:
                        value = click.prompt(f"Enter value for {placeholder}", type=str)
            self.config[placeholder] = value

        task = TES(self.config).create_task(replace_placeholders(task, self.config))
        if task:
            logging.info(f"Created Task ID: {task.get('id')}")
        else:
            logging.error("Failed to create task.")

    def task_status(self, task_id, view, attest):
        if attest and view == 'MINIMAL': # MINIMAL view does not contain the measurement
            view = 'FULL'

        task = TES(self.config).get_task(task_id, view)
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

    def list_all_tasks(self):
        """List all tasks from the TES server."""
        task_list = TES(self.config).list_tasks()
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
