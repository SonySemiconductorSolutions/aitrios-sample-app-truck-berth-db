"""
File: truck_berth_app.py
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

import argparse
import os
import sys
import time

import requests
from common.logger import logger

LOGGER_NAME = "[Truck-Berth-App]"
BACKEND_URL = "http://localhost:5000/api"


def import_data(url, csv_file):
    """
    Method to call import API
    """
    if not os.path.exists(csv_file):
        _msg = f"{LOGGER_NAME} CSV file {csv_file} not found"
        logger.error(_msg)
    with open(csv_file, "rb") as _csv_file:
        res = requests.post(f"{url}/import/", files={"file": _csv_file}, timeout=5000)
    return res.json()


def stop_inference(url):
    """
    Method to call stop-inference API
    """
    res = requests.get(f"{url}/stop-inference/", timeout=5000)
    return res.json()


def export_data(url, export_type, output_dir):
    """
    Method to call export data API
    """
    if export_type not in ["actual", "reservation"]:
        logger.info("Invalid export type. Should be actual or reservation.")
        sys.exit()
    res = requests.get(f"{url}/export/", timeout=5000, params={"type": export_type})
    _now = int(time.time())
    write_file = os.path.join(output_dir, f"{export_type}_{_now}.csv")
    with open(write_file, "wb") as _file:
        _file.write(res.content)
    logger.info("Data exported successfully! Path: %s", write_file)


def truck_berth_main():
    """
    Method to execute cli commands
    """
    parser = argparse.ArgumentParser(
        description="Truck Berth command line function to start inference"
    )
    parser.add_argument("method", type=str, help="Inference function to start or stop")
    parser.add_argument("--csv-file", help="Path to csv file", type=str, required=False)
    parser.add_argument(
        "--type", help="Type of data to export actual/reservation", type=str, required=False
    )
    parser.add_argument(
        "-o", "--output-dir", help="Directory to write the excel file", type=str, required=False
    )
    backend_api_url = BACKEND_URL

    if os.environ.get("TB_BACKEND_URL"):
        backend_api_url = os.environ["TB_BACKEND_URL"] + "/api"

    args = parser.parse_args()

    if args.method == "start":
        # Call the API to start inference
        response_data = import_data(backend_api_url, args.csv_file)
        logger.info(response_data["message"])
    elif args.method == "stop":
        # Call the method to stop inference
        logger.info("Stopping model inference. Please wait...")
        response_data = stop_inference(backend_api_url)
        logger.info(response_data["message"])
    elif args.method == "export":
        export_data(backend_api_url, args.type, args.output_dir)
