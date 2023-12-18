# Command-Line Interface for GA4GH-compliant environments

This project provides a Command-Line Interface (CLI) for interacting with a GA4GH-compliant federated research environments.

## Features
The current version only supports working with Task Execution Service (TES) server. The CLI allows users to create tasks, check the status of tasks, and list all tasks in the TES server.
- **Create Tasks**: Submit new tasks to the TES server.
- **Task Status**: Retrieve the status of a specific task.
- **List Tasks**: List all tasks from the TES server.

## Installation
To use this CLI, ensure that Python 3 is installed on your system. No additional installation steps are required for the CLI itself.

### Installation from GitHub Repository

Open your terminal and run the following command to install:

```commandline
git clone https://github.com/genxnetwork/ga4gh-cli.git
cd ga4gh-cli
bash install.sh
```

### Installation from PyPI Repository

Alternatively, you can install `ga4gh-cli` using pip packet manager:
```commandline
pip install ga4gh-cli==0.1.5
```

## TES Task Definition File

This JSON file defines a TES task with configurable placeholders for input/output parameters or access credentials. The task is named "GRAPE" and consists of multiple executors and resources.

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
                // These environment variables are configured in a separate file
                "AWS_ACCESS_KEY_ID": "${AWS_ACCESS_KEY_ID}", 
                "AWS_SECRET_ACCESS_KEY": "${AWS_SECRET_ACCESS_KEY}",
                "AWS_REGION": "${AWS_REGION}"
            }
        },
        {
            "image": "YOUR DOCKER CONTAINER NAME",
            // Example command to be executed after deployment
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
You can find example task files in `sample` directory.

## Usage

### Create a Task

To create a task:

```bash
ga4gh-cli create-task [TASK_FILE] --config [CONFIG_FILE]
```
`TASK_FILE`: Path to the JSON file containing the task definition.  
`CONFIG_FILE`: Path to the JSON config file containing the base URL for the TES server and other necessary configurations.

### Task Status

To check the status of a task:

```bash
ga4gh-cli task-status [TASK_ID] --config [CONFIG_FILE]
```
`TASK_ID`: The ID of the task.  
`CONFIG_FILE`: Path to the JSON config file.

### Debug Mode

The CLI also supports a debug mode for additional logging:

```bash
ga4gh-cli --debug ...
```

### Config File

You need to provide a JSON configuration file that contains the base URL and any required placeholders for your GA4GH environment.

Example configuration file (`task-name.tesconfig`):
```json
{  
    "base_url": "https://tes-server.example.com",  
    "AWS_ACCESS_KEY_ID": "your-access-key-id",  
    "AWS_SECRET_ACCESS_KEY": "your-secret-access-key",  
    "AWS_REGION": "eu-west-3",  
    "INPUT": "s3://your-storage-url/input.vcf.gz",  
    "OUTPUT": "s3://your-storage-url/output.tsv"  
}
```
In this example, replace the values ("your-access-key-id," "your-secret-access-key," etc.) with your actual configuration values.

## Contributing

Contributions to this project are welcome. Please ensure that your code adheres to the project's coding standards.

## License

GPLv2

## Contact
info@genxt.network