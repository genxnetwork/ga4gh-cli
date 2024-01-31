#!/usr/bin/env python3

import configparser
import os
import click
import logging
from src.cli import CLI

@click.group()
@click.version_option(version = open('VERSION', 'r').read().strip(), prog_name="GA4GH CLI")
@click.option('--config-file', default='~/.ga4gh-cli', metavar='PATH', help='Path to user configuration file.')
@click.option('--log-level', default='INFO', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']), help='Set the logging level')
@click.pass_context
def cli(ctx, config_file, log_level):
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    logging.basicConfig(level=numeric_level, format='%(asctime)s - %(levelname)s - %(message)s')

    config = configparser.ConfigParser()
    config.read(os.path.expanduser(config_file))
    config = {
        "base_url": config.get('TES', 'base_url', fallback=None),
        "username": config.get('TES', 'username', fallback=None),
        "password": config.get('TES', 'password', fallback=None)
    }
    ctx.obj = CLI(config) # ctx.obj is a special attribute that is passed to all commands

# ga4gh-cli create-task [task.tes] --params [params.env] 
@cli.command()
@click.argument('task_file')
@click.option('--params', required=False, help='File with parameters: inputs/outputs, credentials.')
@click.pass_context
def create_task(ctx, task_file, params):
    """Create a task on the TES server."""
    ctx.obj.create_task(task_file, params)

# ga4gh-cli task-status [task-id]
@cli.command()
@click.argument('task_id')
@click.option('--attest', required=False, is_flag=True, help='Provide TEE Remote Attestation measurment.')
@click.option('--view', required=False, default='MINIMAL', type=click.Choice(['MINIMAL', 'BASIC', 'FULL']), help='Task view: FULL, BASIC or MINIMAL.')
@click.pass_context
def task_status(ctx, task_id, attest, view):
    """Get the status of a task from the TES server."""
    ctx.obj.task_status(task_id, view, attest)

# ga4gh-cli task-status [task-id]
@cli.command(name='list-tasks')
@click.pass_context
def list_all_tasks(ctx):
    """List all tasks from the TES server."""
    ctx.obj.list_all_tasks()


if __name__ == '__main__':
    cli()