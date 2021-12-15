#!/usr/bin/env python
import yaml

from evergreen.api import EvgAuth, EvergreenApi

with open("creds_bot.yml", "r") as f:
    yml = yaml.safe_load(f)

user = yml["user"]
print(user)
api_key = yml["api_key"]

api = EvergreenApi.get_api(EvgAuth(user, api_key))

taskname= "mongodb_mongo_master_enterprise_rhel_80_64_bit_dynamic_required_build_variant_gen_patch_c07540fefab04df035434955230f95a1d6297ed6_61ba26d83e8e864892e79cd8_21_12_15_17_33_31"
print(api.task_by_id(taskname))
