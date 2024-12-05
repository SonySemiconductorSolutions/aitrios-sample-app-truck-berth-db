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
File: tasks.py
"""
import logging
import os

from celery import Celery
from celery.signals import after_setup_logger
from modules.cloudapp.interactor import Interactor
from modules.simulated_db.truck_berth_db_controller import TruckBerthDbController

celery = Celery("tasks", broker=os.getenv("RABBIT_MQ_URL"), backend=os.getenv("FERRET_DB_RESULTS_URI"))

BERTH_MAP_JSON_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data", "berth_device_map.json"
)
TOLERANCE_TIME_MINS = 30

_logger = logging.getLogger(__name__)
truck_berth_db = TruckBerthDbController()
interactor = Interactor(_logger)


@after_setup_logger.connect
def setup_loggers(logger, **kwargs):
    """
    Method to setup logger
    """
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - [MODEL_INFERENCE] - %(message)s")

    # add filehandler
    _fh = logging.FileHandler("../../../../model_inference.log", encoding="utf-8")
    _fh.setLevel(logging.DEBUG)
    _fh.setFormatter(formatter)
    logger.addHandler(_fh)


@celery.task
def get_inference_data(berth_number):
    """
    Celery task to get the inference data
    """
    interactor.get_inference_data(berth_number)


@celery.task
def update_truck_status(berth_number):
    """
    Method to update the truck status
    Args:
        berth_number (str): B1 or B2
    """
    interactor.update_truck_status(berth_number)


if __name__ == "__main__":
    update_truck_status("B1")
    update_truck_status("B2")