import requests
import logging
from src.service import Service

class TES(Service):
    def __init__(self, base_url, username=None, password=None, token=None):
        super().__init__(base_url, username, password, token)

    def create(self, task):
        return self.request("POST", "ga4gh/tes/v1/tasks", data=task)

    def status(self, task_id, view):
        endpoint = f"ga4gh/tes/v1/tasks/{task_id}"
        params = {
            'view': view
        }
        return self.request("GET", endpoint, data=None, params=params)

    def list(self):
        return self.request("GET", "ga4gh/tes/v1/tasks")
