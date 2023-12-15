#!/usr/bin/python3

import requests
import json
import argparse

class TES:
    def __init__(self, base_url, debug):
        self.base_url = base_url
        self.debug = debug

    def _make_request(self, method, endpoint, params=None, data=None, debug=False):
        url = f"{self.base_url}/{endpoint}"
        headers = {"Content-Type": "application/json"}

        try:
            if params:
                url += "?" + "&".join([f"{key}={value}" for key, value in params.items()])

            if self.debug:
                print(method, url)

            response = requests.request(method, url, data=json.dumps(data), headers=headers)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print("An error occurred:", str(e))
            return None

    def create_task(self, task):
        return self._make_request("POST", "ga4gh/tes/v1/tasks", data=task)

    def get_task(self, task_id, view=None):
        params = {"view": view} if view else None
        return self._make_request("GET", f"ga4gh/tes/v1/tasks/{task_id}", params=params)

    def list_tasks(self):
        return self._make_request("GET", "ga4gh/tes/v1/tasks")


def create_task(base_url, task_json_file, debug=False):
    try:
        with open(task_json_file, "r") as json_file:
            task = json.load(json_file)
    except Exception as e:
        print("Error reading Task JSON file:", str(e))
        return

    tes_client = TES(base_url, debug)

    created_task = tes_client.create_task(task)

    if created_task:
        print("Created Task ID:", created_task.get("id"))
    else:
        print("Failed to create task.")


def task_status(base_url, task_id, debug=False):
    tes_client = TES(base_url, debug)

    task = tes_client.get_task(task_id)

    if task:
        print(task.get("state"))
    else:
        print("Failed to retrieve task.")


def list_all_tasks(base_url, debug=False):
    tes_client = TES(base_url, debug)
    task_list = tes_client.list_tasks()

    if task_list:
        try:
            tasks = task_list.get("tasks")
            if isinstance(tasks, list):
                for task in tasks:
                    print(f"Task ID: {task.get('id')}, State: {task.get('state')}")
            else:
                print("Invalid response: Tasks should be a list.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {str(e)}")
    else:
        print("Failed to retrieve task list.")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a TES task from a JSON file, check task status, or list tasks.")
    parser.add_argument("--createTask", dest="task_json_file", help="Path to the JSON file containing the TES task definition.")
    parser.add_argument("--status", dest="task_id", help="Task ID to check the status.")
    parser.add_argument("--listTasks", action="store_true", help="List all tasks.")
    parser.add_argument("--debug", action="store_true", help="List all tasks.")
    parser.add_argument("--base-url", default="http://tesktest.genx.link",
                        help="Base URL of the TES server. Default is http://tesktest.genx.link/ga4gh/tes/v1")

    args = parser.parse_args()

    if args.task_json_file:
        create_task(args.base_url, args.task_json_file, debug=args.debug)
    elif args.task_id:
        task_status(args.base_url, args.task_id, debug=args.debug)
    elif args.listTasks:
        list_all_tasks(args.base_url, debug=args.debug)
    else:
        print("No action specified. Use --createTask, --status, or --listTasks.")

