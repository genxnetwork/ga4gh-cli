# Command-Line Interface for GA4GH Environments

This project provides a Command-Line Interface (CLI) for interacting with a GA4GH-compliant federated research environments.

## Features
The current version only supports working with Task Execution Service (TES) server. The CLI allows users to create tasks, check the status of tasks, and list all tasks in the TES server.
- **Create Tasks**: Submit new tasks to the TES server. For example, `ga4gh-cli create-task my-task.tes --params my-task.env`.
- **Task Status**: Retrieve the status of a specific task. For example, `ga4gh-cli task-status my-task-id`.
- **List Tasks**: List all tasks from the TES server. For example, `ga4gh-cli list-tasks`.

## Installation
To use this CLI, ensure that Python 3 is installed on your system. 

### Installation from GitHub Repository

Open your terminal and run the following command to install:

```commandline
git clone https://github.com/genxnetwork/ga4gh-cli.git
cd ga4gh-cli
pip install .
```

### Installation from PyPI Repository

Alternatively, you can install `ga4gh-cli` using pip packet manager:
```commandline
pip install --upgrade ga4gh-cli
```

## TES Task Definition File

The following is an example of a JSON file that defines a TES task. In this example, the task consists of multiple executors and resources. Please note that this is just an example, and your task definition may vary based on your specific requirements. Task files may include configurable placeholders for input/output parameters and access credentials, such as `${INPUT}`, `${OUTPUT}`, and `${AWS_ACCESS_KEY_ID}`. Before sending the task to the TES server, these placeholders can be automaticly replaced in three ways:

1. **Environment Variables**: If an environment variable with the same name as the placeholder is set in your system, the CLI will use its value.

2. **Parameter File**: You can provide a `.env` file with your parameters using the `--params` option when running the CLI. This file should contain key-value pairs in the format `KEY=VALUE`, one per line. An example file `grape.env.template` is provided in the `sample` directory.

3. **Console Input**: If a value for a placeholder is not found in the environment variables or the parameter file, the CLI will prompt you to enter it in the console when you run the task.

```json
{
    "name": "YOUR TASK NAME",
    "resources": {
        "cores": 24,
        "disk_gb": 200,
    },
    "volumes": [
        "/vol/a/"
    ],
    "executors": [
        {
            "image": "amazon/aws-cli",
            "command": [
                "aws", "s3", "cp", "${INPUT}", "/vol/a/input.vcf.gz"
            ],
            "env": {
                "AWS_ACCESS_KEY_ID": "${AWS_ACCESS_KEY_ID}", 
                "AWS_SECRET_ACCESS_KEY": "${AWS_SECRET_ACCESS_KEY}",
                "AWS_REGION": "${AWS_REGION}"
            }
        },
        {
            "image": "YOUR DOCKER CONTAINER NAME",
            "command": [
                "python", "launcher.py",
                "--input", "/vol/a/input.vcf.gz"
                "--output", "/vol/a/output.tsv"
            ]
        },
        {
            "image": "amazon/aws-cli",
            "command": [
                "aws", "s3", "cp", "/vol/a/output.tsv", "${OUTPUT}" 
            ],
            "env": {
                "AWS_ACCESS_KEY_ID": "${AWS_ACCESS_KEY_ID}",
                "AWS_SECRET_ACCESS_KEY": "${AWS_SECRET_ACCESS_KEY}",
                "AWS_REGION": "${AWS_REGION}"
            }
        }
    ]
}
```
You can find example task files in the `sample` directory. These files provide templates that you can use as a starting point for creating your own tasks. Simply copy an example file, replace the placeholder values with your own, and save it in your project directory.

## Usage

## User Configuration File

The CLI expects to find a user configuration file at `~/.ga4gh-cli`. This file should contain the base URL for the TES server, HTTP basic authentication username and password, and any environment variables that may be used by the task template engine.

Here's an example of what this file might look like:

```ini
[TES]
base_url = https://0.0.0.0:8080
username = ga4gh
password = elixir
```

### Create a Task

To create a task:

```bash
ga4gh-cli create-task [TASK_FILE] [--params PARAMS]
```
`TASK_FILE`: Path to the JSON file containing the task definition.  
`--params PARAMS`: (Optional) Path to the `.env` format file containing the base URL for the TES server and other necessary configurations. This file should contain key-value pairs in the format `KEY=VALUE`, one per line.

### Task Status

To check the status of a task:

```bash
ga4gh-cli task-status [TASK_ID] [--view VIEW] [--attest]
```
`TASK_ID`: The ID of the task.  
`--view VIEW` : (Optional) The level of detail to return. This can be one of MINIMAL, BASIC, or FULL. If not specified, the default is BASIC.

`--attest`: (Optional) If specified, the response will include a TEE Attestation measurment of the task workload.

For example, to get the full details of a task:
```bash
ga4gh-cli task-status task-5c7d7853 --view FULL
```
And to get the details of a task with an attestation:
```bash
ga4gh-cli task-status task-5c7d7853 --attest
```
### List Tasks

To list all tasks:

```bash
ga4gh-cli list-tasks
```

### Logging

The CLI supports different levels of logging. You can set the log level using the `--log-level` option followed by one of the following values: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. 

For example, to enable debug logging, you would run:

```bash
ga4gh-cli --log-level DEBUG ...
```

## Contributing

Contributions to this project are welcome. Please ensure that your code adheres to the project's coding standards.

## License

GPLv2

## Contact
info@genxt.network
