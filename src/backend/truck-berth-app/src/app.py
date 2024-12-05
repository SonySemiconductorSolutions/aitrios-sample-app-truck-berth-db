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
File: src/truck-berth-app/src/app.py
"""
import logging
import os

from celery import Celery
from common.logger import get_log_handler
from common.util import get_beat_schedule_config
from flask import Flask, request
from flask_cors import CORS
from modules.cloudapp.interactor import Interactor

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Configure the Celery broker and result backend
app.config["CELERY_BROKER_URL"] = os.getenv("RABBIT_MQ_URL")
app.config["result_backend"] = os.getenv("FERRET_DB_RESULTS_URI")

# creates a Celery object
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)
celery.conf.update(include=["tasks"])

# Configure the FerretDB connection
app.config["FERRET_URI"] = os.getenv("FERRET_DB_URI")

BERTH_MAP_JSON_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "berth_device_map.json"
)

celery.conf.beat_schedule = get_beat_schedule_config(BERTH_MAP_JSON_FILE)
# Configure logging for the Flask app
log_handler = get_log_handler()
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.DEBUG)
interactor = Interactor(app.logger)


@app.route("/api/import/", methods=["GET", "POST"])
def import_reservation_data():
    """
    Route to import csv file to ferretdb

    This route allows you to import the reservation csv data
    and store it into ferretdb.

    :param file: CSV file containing reservation data information
    :type file: file

    :return: A JSON response for confirmation
    :rtype: dict

    :raises 400: If the reservation data format is invalid

    Example usage:
    ```

    POST /api/import
    Request data: file <csv file>
    Response: {"message":"Data imported successfully!","status":200}
    ```
    """
    return interactor.import_reservation_data(request)


@app.route("/api/export/", methods=["GET"])
def export_data():
    """
    Route to export csv file from ferretdb

    This route allows you to import the reservation csv data
    and store it into ferretdb.

    :return: CSV File
    :rtype: file

    :raises 400: If the reservation data format is invalid

    Example usage:
    ```

    POST /api/export/
    Response: File
    ```
    """
    return interactor.export_data(request)


@app.route("/getberthstatus", methods=["GET"])
def get_berth_status():
    """
    Route to get status data

    This route allows you to get the reservation and actual data
    and binds into the graph

    :raises 400: If the reservation data format is invalid

    Example usage:
    ```

    POST /getberthstatus
    Response: {}
    ```
    """
    return interactor.get_berth_status(request)


@app.route("/getnotifications", methods=["GET"])
def get_notifications():
    """
    Route to get notification

    This route allows you to get the notification of truck entry and exit

    Example usage:
    ```

    POST /getnotifications
    Response: {}
    ```
    """
    return interactor.get_notifications(request)


@app.route("/api/stop-inference/", methods=["GET"])
def stop_inference():
    """
    Route to stop model inference

    This route allows you to stop the model inference

    Example usage:
    ```

    POST /stop-inference
    Response: {}
    ```
    """
    return interactor.stop_inference(request)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
