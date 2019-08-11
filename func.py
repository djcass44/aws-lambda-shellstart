#    Copyright 2019 Django Cass
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import boto3
import paramiko
import os


def get_key(event):
    """
    Get the SSH key from S3 and save it to /tmp
    :param event: passed from AWS Lambda
    :return: the path to the saved key
    """
    s3 = boto3.client('s3')
    # download the key
    key_name = event['s3']['key']
    s3.download_file(event['s3']['bucket'], key_name, f"/tmp/{key_name}")
    return f"/tmp/{key_name}"


def cleanup(key_path):
    try:
        os.remove(key_path)
    except OSError as e:
        print(f"Failed to remove key: {e}")


def connect(event, key_path):
    """
    Connect to the target and execute the commands
    :param event: passed from AWS Lambda
    :param key_path: the path to the saved key
    :return: completion confirmation
    """
    # setup the ssh client
    k = paramiko.RSAKey.from_private_key_file(key_path)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # open the ssh connection
    host = event['ssh']['target']
    user = event['ssh']['user']
    print(f"Connecting to {host} as {user}")
    c.connect(hostname=host, username=user, pkey=k)
    print(f"Connected to {user}@{host}")

    base_dir = f"cd {event['ssh']['directory']}"
    commands = []
    containers = event['containers']
    # if no containers are provided, update them all
    if len(containers) == 0:
        commands.append(f"{base_dir}; docker-compose down")
        commands.append(f"{base_dir}; docker-compose pull")
        commands.append(f"{base_dir}; docker-compose up -d")
    else:
        # otherwise, check which containers we want to update
        for container in containers:
            commands.append(f"{base_dir}; docker-compose stop {container} && docker-compose pull {container} && docker"
                            f"-compose up -d {container}")
    for command in commands:
        print(f"Executing: '{command}'")
        stdin, stdout, stderr = c.exec_command(command)
        print(stdout.read())
        print(stderr.read())
    return {
        "message": "Execution complete! See CloudWatch Logs for more information"
    }


# noinspection PyUnusedLocal
def trigger_handler(event, context):
    """
    Function to be triggered by AWS Lambda
    :param event: data passed in from the Lambda
    :param context: unused
    :return: message
    """
    key_path = get_key(event)
    connect(event, key_path)
