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
"""
File: src/truck-berth-app/src/modules/common/util.py
"""
import datetime
import json

import requests
from common.config import (
    EMAIL_SUBJECT,
    FROM_EMAIL,
    NOTIFIER_EMAIL_LIST,
)


def convert_to_schedule_format(_in: dict, color_code: str, bg_color: str, group: int) -> dict:
    """
    Method to format the db data to schedule

    Sample return:
    {
        "content": "9111",
        "end": "2023-10-25 12:00:00",
        "group": 1,
        "id": 7,
        "start": "2023-10-25 08:00:00",
        "style": "color: #f8cecc; background-color: pink;"
    }
    """

    temp = {}
    temp["start"] = _in["start_time"]
    temp["end"] = _in["end_time"]
    if isinstance(_in["start_time"], datetime.datetime):
        temp["start"] = _in["start_time"].strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(_in["end_time"], datetime.datetime):
        temp["end"] = _in["end_time"].strftime("%Y-%m-%d %H:%M:%S")
    temp["content"] = str(_in["car_number"])
    temp[
        "style"
    ] = f"color: {color_code};\
          background-color: {bg_color}; border: 2px solid {bg_color}; border-radius: 3px;"
    temp["group"] = group
    return temp


def get_group(berth_number, is_actual_data):
    """
    Method to get the group number

    B1: 1,2
    B2: 3,4
    B3: 5,6
    """
    berth_no = int(berth_number[-1])
    if berth_no == 1:
        berth_rows = (1, 2)
    else:
        berth_rows = (berth_no + 1, berth_no + 2)

    if is_actual_data:
        return berth_rows[1]
    return berth_rows[0]


def is_time_between(begin_time, end_time, check_time):
    """
    Check if the given check_time is between the start and end time
    Args:
        begin_time: Start time
        end_time: End time
        check_time: Time to check
    """
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    return check_time >= begin_time or check_time <= end_time


def get_beat_schedule_config(berth_device_map_file):
    """
    Method to get the beat schedule config
    """
    with open(berth_device_map_file, "r", encoding="utf-8") as _map_json_file:
        berth_device_map = json.loads(_map_json_file.read())
    beat_schedule = {}
    for _berth_number, _ in berth_device_map.items():
        beat_schedule[f"lpd-lpr-inference-{_berth_number}"] = {
            "task": "tasks.get_inference_data",
            "args": (_berth_number,),
            "schedule": 60.0,  # Run every minute,
        }
        beat_schedule[f"lpd-lpr-status_update-{_berth_number}"] = {
            "task": "tasks.update_truck_status",
            "args": (_berth_number,),
            "schedule": 30.0,
        }
    return beat_schedule


def _post_request(url, headers, data):
    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=300)
    return response


def notify_by_email(message):
    """Send notification by E-mail.
    Args:
        message (str): Message to send
    """
    # send the E-mail.

