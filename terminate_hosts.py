#!/usr/bin/env python
import boto3
import botocore
import csv
import pprint
import yaml

from evergreen.api import EvgAuth, EvergreenApi

with open("creds.yml", "r") as f:
    yml = yaml.safe_load(f)

user = yml["user"]
api_key = yml["api_key"]

api = EvergreenApi.get_api(EvgAuth(user, api_key))

#host_ids = ["i-000cba730e92eb85b", "i-017090111eb60fd25"]
with open ("./unterminated_hosts_2021-12-10.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    raw_hosts = [api.host_by_id(row["host_id"]) for row in reader]

non_user_hosts = [host for host in raw_hosts if not host.user_host and host.status == "terminated" and host.started_by == "mci"]
IDs_to_terminate = [host.host_id for host in non_user_hosts]

print(IDs_to_terminate)
session = boto3.session.Session()
ec2 = session.client('ec2')

for host_id in IDs_to_terminate:
    try:
        termination_response = ec2.terminate_instances(InstanceIds=[host_id], DryRun=False)
        pprint.pprint(termination_response)
    except botocore.exceptions.ClientError as e:
        print(e)
