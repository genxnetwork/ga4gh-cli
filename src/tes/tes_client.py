import requests
import logging

class TES:
    def __init__(self, config):
        self.config = config

    def request(self, method, endpoint, data=None, params=None):
        url = f"{self.config.get('base_url')}/{endpoint}"
        headers = {"Content-Type": "application/json"}

        if self.config['username'] and self.config['password']:
            logging.debug(f"{method} request to {endpoint} with data: {data}, params: {params}, and username: {self.config['username']}")
            auth = (self.config['username'], self.config['password'])
            response = requests.request(method, url, json=data, headers=headers, params=params, auth=auth)
        else:
            logging.debug(f"Making {method} request to {endpoint} with data: {data} and params: {params}")
            response = requests.request(method, url, json=data, headers=headers, params=params)

        if response.status_code != 200:
            error_message = f"Error: HTTP {response.status_code} - {response.reason}"
            logging.error(error_message)
            raise Exception(error_message)
        
        logging.debug(f"Response: {response.json()}")
        return response.json()

    def create_task(self, task):
        return self.request("POST", "ga4gh/tes/v1/tasks", data=task)

    def get_task(self, task_id, view):
        endpoint = f"ga4gh/tes/v1/tasks/{task_id}"
        params = {
            'view': view
        }
        return self.request("GET", endpoint, data=None, params=params)

    def list_tasks(self):
        return self.request("GET", "ga4gh/tes/v1/tasks")
