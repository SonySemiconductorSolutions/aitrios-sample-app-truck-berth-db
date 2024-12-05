"""
File: src/truck-berth-app/src/modules/db_controller/truck_berth_db_controller.py
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
import warnings
from enum import Enum
from typing import Any, Mapping

from pymongo import MongoClient

warnings.filterwarnings("ignore")


class TruckBerthDB(Enum):
    """
    Ferretdb collection name
    """

    ACTUAL_DATA = "actual_data"
    RESERVATION_DATA = "reservation_data"


class TruckBerthDbController:
    """
    TruckBerth DB controller
    """

    def __init__(self):
        ferret_client = MongoClient(os.getenv("FERRET_DB_URI"))
        self._db = ferret_client["truckberthapp"]

    def insert_one(self, table_name: TruckBerthDB, data):
        """Method to insert one object"""
        self._db[table_name.value].insert_one(data)

    def insert_many(self, table_name: TruckBerthDB, data):
        """Method to insert many objects"""
        self._db[table_name.value].insert_many(data)

    def delete_all(self, table_name: TruckBerthDB, _filter):
        """Method to delete many objects"""
        self._db[table_name.value].delete_many(_filter)

    def get_data(self, table_name: TruckBerthDB, _filter):
        """Method to find objects"""
        return self._db[table_name.value].find(_filter)

    def get_one_data(self, table_name: TruckBerthDB, _filter):
        """Method to find one object"""
        return self._db[table_name.value].find_one(_filter)

    def update_one(self, table_name: TruckBerthDB, data: Mapping[str, Any], _filter):
        """Method to update one object"""
        return self._db[table_name.value].update_one(_filter, data)
