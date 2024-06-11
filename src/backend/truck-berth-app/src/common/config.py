"""
File: config.py
"""

# ------------------------------------------------------------------------
# Copyright 2024 Sony Semiconductor Solutions Corp. All rights reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------
import os

import yaml

CAL_SETTINGS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../data", "truck_berth_backend_settings.yaml"
)

with open(CAL_SETTINGS_FILE, "r", encoding="utf-8") as _file:
    base_config = yaml.safe_load(_file)

config = base_config["truck_berth_backend_settings"]

BASE_URL = config["console_endpoint"]
ACCESS_TOKEN_URL = config["portal_authorization_endpoint"]
CLIENT_ID = config["client_id"]
CLIENT_SECRET = config["client_secret"]
SENDGRID_API_KEY = config["sendgrid_api_key"]
FROM_EMAIL = config["from_email"]
EMAIL_SUBJECT = config["email_subject"]
NOTIFIER_EMAIL_LIST = config["notifier_email_list"]
MAIL_NOTIFICATION = config["mail_notification"]
SENDGRID_API_ENDPOINT = config["sendgrid_api_endpoint"]
