import requests
import logging

class Service():
    def __init__(self, base_url, username=None, password=None, token=None):
        if base_url is None:
            raise ValueError("base_url cannot be None.")
        self.base_url = base_url 
        self.username = username
        self.password = password
        self.token = token

    def request(self, method, endpoint, data=None, params=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {"Content-Type": "application/json"}

        auth = None
        if self.username and self.password:
            auth = (self.username, self.password)

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        logging.debug(f"{method} request to {endpoint} with data: {data}, params: {params}, headers: {headers}, and auth: {auth}")
        response = requests.request(method, url, json=data, headers=headers, params=params, auth=auth)

        if response.status_code != 200:
            error_message = f"Error: HTTP {response.status_code} - {response.reason}"
            logging.error(error_message)
            raise Exception(error_message)
        
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = response.text
        else:
            response_data = response.text

        logging.debug(f"Response: {response_data}")
        return response.json()
