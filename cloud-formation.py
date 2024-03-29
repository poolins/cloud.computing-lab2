#!/usr/bin/env python3

import argparse
import yaml
import hvac
import os
from openstack import connection

def create_or_update_stack(conn, stack_name, template, env):
    stack = conn.orchestration.find_stack(stack_name)

    if stack:
        print(f"Updating stack: {stack_name}")
        conn.orchestration.update_stack(
            stack.id,
	    template=template,
            environment=env
        )
    else:
        print(f"Creating stack: {stack_name}")
        conn.orchestration.create_stack(
            name=stack_name,
            template=template,
            environment=env
        )

parser = argparse.ArgumentParser(description="Create or update an OpenStack Heat stack.")
parser.add_argument("stack_name", help="Name of the Heat stack")
parser.add_argument("template_path", help="Path to the Heat template file")
parser.add_argument("environment_path", help="Path to the environment file")

args = parser.parse_args()

url = os.environ["VAULT_ADDR"]
token = os.environ["VAULT_TOKEN"]
client = hvac.Client(url, token)

read_response = client.secrets.kv.read_secret_version(path='openstack-auth', mount_point='kv')
auth_url = read_response['data']['data']['auth_url']
project_id = read_response['data']['data']['project_id']
username = read_response['data']['data']['username']
password = read_response['data']['data']['password']

auth = {
    "auth_url": auth_url,
    "project_id": project_id,
    "username": username,
    "password": password,
    "user_domain_name": "Default",
    "compute_api_version": "3",
    "identity_interface": "public"
}

conn = connection.Connection(**auth)

stack_name = args.stack_name

with open(args.template_path, 'r') as template_file:
    template = template_file.read()

with open(args.environment_path, 'r') as env_file:
    env = env_file.read()

create_or_update_stack(conn, stack_name, template, env)
