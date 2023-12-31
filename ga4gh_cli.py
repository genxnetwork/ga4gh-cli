#!/usr/bin/env python3

import requests
import json
import click
import re
from typing import Dict

VERSION = "0.1.6"

from click import version_option

class TES:
    def __init__(self, base_url, username=None, password=None, debug=False):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.password = password
        self.debug = debug

    def make_request(self, method, endpoint, data=None, params=None):
        if self.debug:
            print(f"Making {method} request to {endpoint} with data: {data} and params: {params}")

        url = f"{self.base_url}/{endpoint}"
        headers = {"Content-Type": "application/json"}

        if self.username and self.password:
            auth = (self.username, self.password)
            response = requests.request(method, url, json=data, headers=headers, params=params, auth=auth)
        else:
            response = requests.request(method, url, json=data, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error: HTTP {response.status_code} - {response.reason}")
            return None
        return response.json()

    def create_task(self, task):
        return self.make_request("POST", "ga4gh/tes/v1/tasks", data=task)

    def get_task(self, task_id):
        endpoint = f"ga4gh/tes/v1/tasks/{task_id}"
        params = {'view': 'FULL'} if self.debug else None
        return self.make_request("GET", endpoint, data=None, params=params)

    def list_tasks(self):
        return self.make_request("GET", "ga4gh/tes/v1/tasks")

def load_config(config_file_path) -> Dict:
    try:
        with open(config_file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading config file: {e}")
    return {}

def find_placeholders(task) -> set:
    placeholder_pattern = r'\$\{\w+\}'
    placeholders = set()

    def search(obj):
        if isinstance(obj, dict):
            for value in obj.values():
                search(value)
        elif isinstance(obj, list):
            for item in obj:
                search(item)
        elif isinstance(obj, str):
            found = re.findall(placeholder_pattern, obj)
            placeholders.update(found)

    search(task)
    return placeholders

def replace_placeholders(obj, values) -> Dict:
    if isinstance(obj, str):
        for placeholder, value in values.items():
            obj = obj.replace(placeholder, value)
        return obj
    elif isinstance(obj, dict):
        return {k: replace_placeholders(v, values) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_placeholders(elem, values) for elem in obj]
    return obj

@click.group()
@click.option('--debug', is_flag=True, help='Enable debug mode.')
@version_option(version=VERSION, prog_name="GA4GH CLI")
@click.pass_context
def cli(ctx, debug):
    ctx.ensure_object(dict)
    ctx.obj['debug'] = debug

@cli.command()
@click.argument('task_file')
@click.option('--config', required=True, help='Path to the JSON config file.')
@click.pass_context
def create_task(ctx, task_file, config):
    config = load_config(config)
    tes = TES(config["base_url"], config["http-username"], config["http-password"], ctx.obj['debug'])

    with open(task_file, 'r') as json_file:
        task = json.load(json_file)

    placeholders = find_placeholders(task)

    for placeholder in placeholders:
        if placeholder not in config:
            config[placeholder] = click.prompt(f"Enter value for {placeholder}", type=str)

    task = replace_placeholders(task, config)
    created_task = tes.create_task(task)

    if created_task:
        print(f"Created Task ID: {created_task.get('id')}")
    else:
        print("Failed to create task.")

@cli.command()
@click.argument('task_id')
@click.option('--config', required=True, help='Path to the JSON config file.')
@click.pass_context
def task_status(ctx, task_id, config):
    config = load_config(config)
    debug = ctx.obj['debug']
    tes = TES(config["base_url"], config["http-username"], config["http-password"], debug)
    task = tes.get_task(task_id)
    if task:
        if not debug:
            print(task.get("state"))
        else:
            print(task)
    else:
        print("Failed to retrieve task.")

@cli.command(name='list-tasks')
@click.option('--config', required=True, help='Path to the JSON config file.')
@click.pass_context
def list_all_tasks(ctx, config):
    config = load_config(config)
    tes = TES(config["base_url"], config["http-username"], config["http-password"], ctx.obj['debug'])
    task_list = tes.list_tasks()
    if task_list:
        tasks = task_list.get("tasks", [])
        for task in tasks:
            print(f"Task ID: {task.get('id')}, State: {task.get('state')}")
    else:
        print("Failed to retrieve task list.")

if __name__ == '__main__':
    cli()
