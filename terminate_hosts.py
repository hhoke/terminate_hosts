#!/usr/bin/env python
import boto3
import yaml

from evergreen.api import EvgAuth, EvergreenApi

with open("creds.yml", "r") as f:
    yml = yaml.safe_load(f)

user = yml["user"]
api_key = yml["api_key"]

api = EvergreenApi.get_api(EvgAuth(user, api_key))

host_ids = ["i-000cba730e92eb85b", "i-017090111eb60fd25"]
raw_hosts = [api.host_by_id(host_id) for host_id in host_ids]
non_user_hosts = [host for host in raw_hosts if not host.user_host]
IDs_to_terminate = [host.host_id for host in non_user_hosts]

print(IDs_to_terminate)
exit()

session = boto3.session.Session()
ec2 = session.client('ec2')
ec2.terminate_instances(InstanceIds=IDs_to_terminate, DryRun=True)
