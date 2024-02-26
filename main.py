#!/usr/bin/env python3

import configparser
import os
import click
import logging
import traceback
from src.cli import CLI
import sys

@click.group()
@click.version_option(version = open('VERSION', 'r').read().strip(), prog_name="GA4GH CLI")
@click.option('--config-file', default='~/.ga4gh-cli', metavar='PATH', help='Path to user configuration file.')
@click.option('--debug', is_flag=True, help="Enable debug mode")
@click.pass_context
def cli(ctx, config_file, debug):
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, NotImplementedError):
            logging.error(exc_value)
            sys.exit(-1)

    sys.excepthook = handle_exception

    config = configparser.ConfigParser()
    config.read(os.path.expanduser(config_file))
    config = {s:dict(config._sections[s]) for s in config._sections}

    ctx.obj = CLI(config) # ctx.obj is a special attribute that is passed to all commands


## AAI commands
    
@click.group(help="Commands for interacting with the AAI service.")
def aai():
    pass

@aai.command()
@click.pass_context
def login(ctx):
    """Log in to the AAI server."""
    ctx.obj.aai_login()

cli.add_command(aai, name='aai')

## TES commands

@click.group(help="Commands for interacting with the TES service.")
def tes():
    pass

# ga4gh-cli tes create [task.tes] --params [params.env] 
@tes.command()
@click.argument('task_file')
@click.argument('params', required=False, default=None)
@click.pass_context
def create(ctx, task_file, params):
    """Create a task on the TES server."""
    ctx.obj.tes_create(task_file, params)

# ga4gh-cli tes status [task-id]
@tes.command()
@click.argument('task_id')
@click.option('--attest', required=False, is_flag=True, help='Provide TEE Remote Attestation measurment.')
@click.option('--view', required=False, default='MINIMAL', type=click.Choice(['MINIMAL', 'BASIC', 'FULL']), help='Task view: FULL, BASIC or MINIMAL.')
@click.pass_context
def status(ctx, task_id, attest, view):
    """Get the status of a task from the TES server."""
    ctx.obj.tes_status(task_id, view, attest)

# ga4gh-cli tes list
@tes.command()
@click.pass_context
def list(ctx):
    """List all tasks from the TES server."""
    ctx.obj.tes_list()

cli.add_command(tes, name='tes')

## WES commands

@click.group(help="Commands for interacting with the WES service.")
def wes():
    pass

# ga4gh-cli wes create [workflow.wes] --params [params.env] 
@wes.command()
@click.argument('workflow_file')
@click.argument('params', required=False, default=None) #, help='File with parameters: inputs/outputs, credentials.')
@click.pass_context
def create(ctx, workflow_file, params):
    """Create a workflow on the WES server."""
    ctx.obj.wes_create(workflow_file, params)

# ga4gh-cli wes status [workflow-id]
@wes.command()
@click.argument('workflow_id')
@click.option('--attest', required=False, is_flag=True, help='Provide TEE Remote Attestation measurment.')
@click.option('--view', required=False, default='MINIMAL', type=click.Choice(['MINIMAL', 'BASIC', 'FULL']), help='Workflow view: FULL, BASIC or MINIMAL.')
@click.pass_context
def status(ctx, workflow_id, attest, view):
    """Get the status of a workflow from the WES server."""
    ctx.obj.wes_status(workflow_id, view, attest)

# ga4gh-cli wes list
@wes.command()
@click.pass_context
def list(ctx):
    """List all workflows from the WES server."""
    ctx.obj.wes_list()

cli.add_command(wes, name='wes')


if __name__ == '__main__':
    try:
        cli()
    except SystemExit:
        pass 
    except NotImplementedError as e:
        logging.error(e)
        raise SystemExit(-1)
    except BaseException:
        traceback.print_exc()
        logging.error("An error occurred.")
    except Exception as e:
        logging.error(e)
        raise SystemExit(-1)
    