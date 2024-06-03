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
File: interactor.py
"""
import json
import os
import time
from datetime import datetime, timedelta
from io import StringIO

import pandas as pd
import pymongo
from common.config import CLIENT_ID, CLIENT_SECRET, MAIL_NOTIFICATION
from common.util import convert_to_schedule_format, get_group, is_time_between, notify_by_sendgrid
from flask import Response
from modules.AITRIOS_console.authentication import get_access_token
from modules.AITRIOS_console.cloud_db_controller import CloudDBController
from modules.AITRIOS_console.edge_device_controller import EdgeDeviceController
from modules.simulated_db.truck_berth_db_controller import TruckBerthDB, TruckBerthDbController

# Global variables
BERTH_MAP_JSON_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../../data", "berth_device_map.json"
)

PRIMARY_MATCH_COLOR = "#82b366"
PRIMARY_NON_MATCH_COLOR = "#ea6b66"
SECONDARY_MATCH_COLOR = "#d5e8d4"
SECONDARY_NON_MATCH_COLOR = "#f8cecc"
TOLERANCE_TIME_MINS = 30


class Interactor:
    """
    Use case Interactor
    """

    def __init__(self, logger) -> None:
        self.logger = logger
        self.db_obj = TruckBerthDbController()
        access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
        self.ed_device_obj = EdgeDeviceController(access_token)

    # pylint:disable=too-many-locals
    def import_reservation_data(self, request):
        """
        Method to import reservation data
        Args:
            request : Flask request object
        """
        self.logger.info("API request received: %s %s", request.method, request.path)
        file = request.files["file"]
        if file:
            try:
                # Read the CSV file
                _df = pd.read_csv(file)
                allowed_columns = [
                    "email_id",
                    "start_time",
                    "end_time",
                    "berth_number",
                    "car_number",
                    "status",
                ]
                bad_cols = set(_df.columns) - set(allowed_columns)
                if len(bad_cols) > 0:
                    _msg = f"Unknown column {bad_cols};\
                          only {allowed_columns} columns should be present"
                    return {
                        "status": 400,
                        "message": _msg,
                    }
                # Clear all the existing reservation data
                self.logger.info("[DB][DELETE] Deleting the existing reservation data")
                self.db_obj.delete_all(TruckBerthDB.RESERVATION_DATA, {})

                _df["start_time"] = pd.to_datetime(_df["start_time"], dayfirst=True)
                _df["end_time"] = pd.to_datetime(_df["end_time"], dayfirst=True)

                # Insert the data into MongoDB
                data = _df.to_dict(orient="records")
                self.logger.info("[DB][INSERT] Adding the reservation data")
                self.db_obj.insert_many(TruckBerthDB.RESERVATION_DATA, data)
                with open(BERTH_MAP_JSON_FILE, "r", encoding="utf-8") as _map_json_file:
                    berth_device_map = json.loads(_map_json_file.read())

                # Set the start status in the berth configuration file
                for _berth_number, value in berth_device_map.items():
                    value["inference_status"] = "start"
                with open(BERTH_MAP_JSON_FILE, "w", encoding="utf-8") as _file:
                    _file.write(json.dumps(berth_device_map, indent=4))

                # Re-map reservation data to actual data table
                actual_data_list = self.db_obj.get_data(TruckBerthDB.ACTUAL_DATA, {})
                for actual_data_row in actual_data_list:
                    reservation_id = self._find_reservation_data(
                        TruckBerthDB.RESERVATION_DATA, actual_data_row
                    )
                    self.db_obj.update_one(
                        TruckBerthDB.ACTUAL_DATA,
                        {"$set": {"reservation_id": reservation_id}},
                        {"_id": actual_data_row["_id"]},
                    )
                response = {"status": 200, "message": "Data imported successfully!"}
                return response
            except Exception as _e:
                return {"status": 500, "message": f"Internal error {_e}"}
        return {"status": 500, "message": "CSV file is missing"}

    def export_data(self, request):
        """
        Method to export data
        Args:
            request : Flask request object
        """
        self.logger.info("API request received: %s %s", request.method, request.path)
        export_type = request.args.get("type")

        # Check if the export type is either reservation/actual
        if export_type not in ["reservation", "actual"]:
            return {
                "status": 400,
                "message": "Invalid export type",
            }
        collection = TruckBerthDB.ACTUAL_DATA
        if export_type == "reservation":
            collection = TruckBerthDB.RESERVATION_DATA
        # pylint:disable=abstract-class-instantiated
        self.logger.info("[DB][READ] Read the collection: %s", collection.value)
        # Query the collection
        cursor = self.db_obj.get_data(collection, {})
        _df = pd.DataFrame(list(cursor))
        csv_data = StringIO()

        _df.to_csv(csv_data, index=False)
        # Convert into csv and send the response
        response = Response(csv_data.getvalue(), mimetype="text/csv")
        response.headers["Content-Disposition"] = f"attachment; filename={collection.value}.csv"

        return response

    def get_berth_status(self, request):
        """
        Method to get berth status
        Args:
            request : Flask request object
        """
        self.logger.info("API request received: %s %s", request.method, request.path)
        # Initialize the collections
        reserve_coll = TruckBerthDB.RESERVATION_DATA
        actual_coll = TruckBerthDB.ACTUAL_DATA
        response = {"status": 200, "data": {"berths": ["B1", "B2"], "status": [], "message": ""}}
        self.logger.info("[DB][READ] Read collection: '%s'", actual_coll.name)
        actual_data_list = list(self.db_obj.get_data(actual_coll, {}))
        schedule_data = []
        mapped_reservation_ids = []
        mapped_actual_ids = []

        # Iterate over the actual data
        for actual_data in actual_data_list:
            self.logger.info("[DB][READ] Read collection: '%s'", reserve_coll.name)
            reserve_data = list(
                self.db_obj.get_data(
                    reserve_coll,
                    {
                        "start_time": {"$lte": actual_data["start_time"]},
                        "end_time": {"$gte": actual_data["end_time"]},
                        "berth_number": {"$eq": actual_data["berth_number"]},
                    },
                )
            )
            is_mapped = False
            # Check if any reservation available for this actual data
            if len(reserve_data) > 0:
                r_data = reserve_data[0]
                if r_data["car_number"] == actual_data["car_number"]:
                    is_mapped = True
                    # Push the item to the response list
                    schedule_data.append(
                        convert_to_schedule_format(
                            actual_data,
                            color_code=PRIMARY_MATCH_COLOR,
                            bg_color=SECONDARY_MATCH_COLOR,
                            group=get_group(r_data["berth_number"], is_actual_data=True),
                        )
                    )
                else:
                    schedule_data.append(
                        convert_to_schedule_format(
                            actual_data,
                            color_code=PRIMARY_NON_MATCH_COLOR,
                            bg_color=SECONDARY_NON_MATCH_COLOR,
                            group=get_group(r_data["berth_number"], is_actual_data=True),
                        )
                    )
                # Check if the reservation time range had any other cars
                self.logger.info("[DB][READ] Read collection: '%s'", actual_coll.name)
                any_other_cars_found = list(
                    self.db_obj.get_data(
                        actual_coll,
                        {
                            "car_number": {"$ne": actual_data["car_number"]},
                            "$or": [
                                {
                                    "start_time": {
                                        "$gte": r_data["start_time"],
                                        "$lte": r_data["end_time"],
                                    }
                                },
                                {
                                    "end_time": {
                                        "$gte": r_data["start_time"],
                                        "$lte": r_data["end_time"],
                                    },
                                },
                            ],
                        },
                    )
                )
                color_code = (
                    SECONDARY_MATCH_COLOR
                    if len(any_other_cars_found) == 0
                    else SECONDARY_NON_MATCH_COLOR
                )
                bg_color_code = (
                    PRIMARY_MATCH_COLOR
                    if len(any_other_cars_found) == 0
                    else PRIMARY_NON_MATCH_COLOR
                )
                if not is_mapped:
                    color_code = SECONDARY_NON_MATCH_COLOR
                    bg_color_code = PRIMARY_NON_MATCH_COLOR
                schedule_data.append(
                    convert_to_schedule_format(
                        r_data,
                        color_code=color_code,
                        bg_color=bg_color_code,
                        group=get_group(r_data["berth_number"], is_actual_data=False),
                    )
                )
                mapped_reservation_ids.append(r_data["_id"])
                mapped_actual_ids.append(actual_data["_id"])
            else:
                color_code = PRIMARY_NON_MATCH_COLOR
                schedule_data.append(
                    convert_to_schedule_format(
                        actual_data,
                        color_code=color_code,
                        bg_color=SECONDARY_NON_MATCH_COLOR,
                        group=get_group(actual_data["berth_number"], is_actual_data=True),
                    )
                )
                mapped_actual_ids.append(actual_data["_id"])

        # Collect Un mapped reservation data
        self.logger.info("[DB][READ] Read collection: '%s'", reserve_coll.name)
        other_reserve_data_list = list(
            self.db_obj.get_data(reserve_coll, {"_id": {"$nin": mapped_reservation_ids}})
        )
        for res_data in other_reserve_data_list:
            color_code = SECONDARY_NON_MATCH_COLOR
            schedule_data.append(
                convert_to_schedule_format(
                    res_data,
                    color_code=color_code,
                    bg_color=PRIMARY_NON_MATCH_COLOR,
                    group=get_group(res_data["berth_number"], is_actual_data=False),
                )
            )
        # Collect Un mapped actual data
        self.logger.info("[DB][READ] Read collection: '%s'", actual_coll.name)
        other_actual_data_list = list(
            self.db_obj.get_data(actual_coll, {"_id": {"$nin": mapped_actual_ids}})
        )
        for act_data in other_actual_data_list:
            color_code = PRIMARY_NON_MATCH_COLOR
            schedule_data.append(
                convert_to_schedule_format(
                    act_data,
                    color_code=color_code,
                    bg_color=SECONDARY_NON_MATCH_COLOR,
                    group=get_group(act_data["berth_number"], is_actual_data=True),
                )
            )

        # Add unique ID to the schedule data
        for key, _schedule in enumerate(schedule_data, start=1):
            _schedule["id"] = key
        response["data"]["status"] = schedule_data
        return response

    def stop_inference(self, request):
        """
        Method to stop inference
        Args:
            request : Flask request object
        """
        self.logger.info("API request received: %s %s", request.method, request.path)

        # Read the berth map json file
        with open(BERTH_MAP_JSON_FILE, "r", encoding="utf-8") as _map_json_file:
            berth_device_map = json.loads(_map_json_file.read())

        # Iterate over the devices
        for _berth_number, value in berth_device_map.items():
            # Call the stop inference CAL API
            self.ed_device_obj.stop_upload_inference(value["device_id"])
            value["inference_status"] = "stop"
            self.logger.info("Inference stopped for Berth: %s", _berth_number)

        # Set the status in the berth map file
        with open(BERTH_MAP_JSON_FILE, "w", encoding="utf-8") as _file:
            _file.write(json.dumps(berth_device_map, indent=4))

        return {
            "status": 200,
            "message": f"Inference stopped for the berths {list(berth_device_map.keys())}",
            "berths": list(berth_device_map.keys()),
        }

    def get_notifications(self, request):
        """
        Method to get notifications
        Args:
            request : Flask request object
        """
        self.logger.info("API request received: %s %s", request.method, request.path)
        # Initialize the collections
        actual_coll = TruckBerthDB.ACTUAL_DATA
        response = {"status": 200, "data": []}
        # Get the Notification time filter
        filter_time = request.args.get("notification_time")
        query = {}
        format_data = "%d/%m/%y %H:%M"
        if filter_time:
            query = {"end_time": {"$gte": datetime.strptime(filter_time, format_data)}}
        self.logger.info("[DB][READ] Read collection: '%s'", actual_coll.name)
        # Query the actual data list
        actual_data_list = list(
            self.db_obj.get_data(actual_coll, query).sort("start_time", pymongo.DESCENDING)
        )
        for actual_data_row in actual_data_list:
            # Format the data as per the UI needs
            temp = {
                "class": "notify-item notify-item-success",
                "notification_time": None,
                "car_number": actual_data_row["car_number"],
                "berth_number": actual_data_row["berth_number"],
                "notification_message": f"Truck {actual_data_row['car_number']} has arrived",
            }
            temp["notification_time"] = datetime.strftime(
                actual_data_row["start_time"], format_data
            )
            # Check if the reservation id is available.
            if not actual_data_row["reservation_id"]:
                temp[
                    "notification_message"
                ] = f"Truck {actual_data_row['car_number']} has entered without any reservation"
                temp["class"] = "notify-item notify-item-danger"
            response["data"].append(temp.copy())
        return response

    def get_inference_data(self, berth_number: str):
        """
        Method to get inference data from AITRIOS and store it in the DB

        Args:
            berth_number(str): B$ (B1 or B2)
        """
        # Read the berth map json file
        with open(BERTH_MAP_JSON_FILE, "r", encoding="utf-8") as _map_json_file:
            berth_device_map = json.loads(_map_json_file.read())
        # Make sure the inference status is set to "start"
        if berth_device_map[berth_number]["inference_status"] == "start":
            device_id = berth_device_map[berth_number]["device_id"]
            init_inference_resp = self.ed_device_obj.start_upload_inference(device_id)
            try:
                if init_inference_resp.json()["result"] == "SUCCESS":
                    # Get plate text if the response is available.
                    plate_text = self._get_plate_text(self.ed_device_obj.access_token, device_id)
                    if not plate_text:
                        self.logger.info("No Trucks detected")
                        return
                    start_time, end_time = self._get_start_end_time_for_today()
                    # Check if the same car number and berth number is already available for today
                    query = {
                        "berth_number": berth_number,
                        "car_number": plate_text,
                        "end_time": {"$gte": start_time, "$lte": end_time},
                    }
                    record = self.db_obj.get_one_data(TruckBerthDB.ACTUAL_DATA, query)
                    # Check if the record exists in the database
                    if record:
                        update_data = {"$set": {"end_time": datetime.now()}}
                        self.logger.info("[DB][READ] Record found %s", record)
                        self.logger.info("[DB][UPDATE] %s", update_data)
                        # Update the existing record
                        record = self.db_obj.update_one(
                            TruckBerthDB.ACTUAL_DATA, update_data, query
                        )
                    else:
                        # Add new record
                        time_now = datetime.now()
                        data = {
                            "berth_number": berth_number,
                            "email_id": None,
                            "start_time": time_now,
                            "end_time": time_now,
                            "status": "occupied",
                            "car_number": plate_text,
                            "arrival_notification": False,
                            "depart_notification": False,
                            "reservation_id": None,
                            "is_email_notified": False,
                        }
                        data["reservation_id"] = self._find_reservation_data(
                            TruckBerthDB.RESERVATION_DATA, data
                        )
                        self.logger.info("[DB][INSERT] Record not found Adding.. %s", data)
                        self.db_obj.insert_one(TruckBerthDB.ACTUAL_DATA, data)
                else:
                    self.logger.info(init_inference_resp.json())
                    self.logger.info("No inference data available.. Retrying..")
            except Exception as _err:
                self.logger.error(_err)
                self.logger.error(init_inference_resp)
        else:
            self.logger.info("Inference has been stopped by the user.")

    def _get_max_bb_score_index(self, slot_list):
        _bb = []
        for _sl in slot_list:
            _bb.append(_sl["car"]["license_plate"]["bounding_box_score"])
        return _bb.index(max(_bb))

    def _get_plate_text(self, access_token: str, device_id: str):
        match_streak = 0
        max_retry = 5
        last_plate_text = ""
        plate_text_list = []
        match_found = False
        count = 0

        cloud_db_ctrl = CloudDBController()
        # Run until the match found or till the max retry threshold
        while not match_found:
            response = cloud_db_ctrl.get_latest_inference(access_token, device_id)
            if response.status_code == 200:
                inferred_raw_data = response.json()["Inferences"][0]["O"]
                # Deserialize the base64 output
                deserialized_data = self.ed_device_obj.get_deserialized_data(inferred_raw_data)
                self.logger.info("Inference data obtained")
                self.logger.info(deserialized_data)
                if len(deserialized_data["slot_list"]) > 0:
                    _max_bb_score_index = 0
                    if len(deserialized_data["slot_list"]) > 1:
                        # Get max bounding box score if the slot list has multiple detections
                        _max_bb_score_index = self._get_max_bb_score_index(
                            deserialized_data["slot_list"]
                        )
                    current_plate_text = deserialized_data["slot_list"][_max_bb_score_index]["car"][
                        "license_plate"
                    ]["license_plate_text"]["plate_number"]
                    if last_plate_text == current_plate_text and current_plate_text != "":
                        match_streak += 1
                    else:
                        match_streak = 0

                    last_plate_text = current_plate_text

                    if match_streak == 2:
                        return current_plate_text
                    plate_text_list.append(current_plate_text)
                else:
                    self.logger.info("No detections found!")
                count += 1

            if count >= max_retry:
                break
            time.sleep(2)

        if len(plate_text_list) > 0:
            # Get the most frequent element out of the plate text list
            # The frequency has to be at least 3.
            plate_text = self._most_frequent(plate_text_list)
            if plate_text:
                return plate_text
        return None

    def _most_frequent(self, _list: list):
        """
        Get the most frequent element from the list
        Args:
            List of items
        """
        if not _list:
            return None

        counter = 0
        num = None

        for i in _list:
            curr_frequency = _list.count(i)
            if curr_frequency >= 3 and curr_frequency > counter:
                counter = curr_frequency
                num = i

        return num if counter >= 3 else None

    def _find_reservation_data(self, r_collection, actual_data):
        """
        Method to find the reservation data for the given actual data

        Args:
            r_collection (mongodb collection): Mongodb collection object
            actual_data (dict): Dictionary of actual data
        """
        start_time, end_time = self._get_start_end_time_for_today()
        query = {
            "berth_number": actual_data["berth_number"],
            "car_number": actual_data["car_number"],
            "end_time": {"$gte": start_time, "$lte": end_time},
        }
        reservation_data_list = self.db_obj.get_data(r_collection, query)
        reservation_data = None
        # Iterate over the reservation data the find the time match for the actual data.
        for _r_data in reservation_data_list:
            _offset_start = _r_data["start_time"] - timedelta(minutes=TOLERANCE_TIME_MINS)
            _offset_end = _r_data["end_time"]
            if is_time_between(_offset_start, _offset_end, actual_data["start_time"]):
                reservation_data = str(_r_data["_id"])
                break
        return reservation_data

    def _get_start_end_time_for_today(self):
        today = datetime.now()
        res_format = "%d/%m/%y %H:%M"
        _st = today.strftime("%d/%m/%y") + " 00:00"
        _ed = today.strftime("%d/%m/%y") + " 23:59"
        return (datetime.strptime(_st, res_format), datetime.strptime(_ed, res_format))

    def update_truck_status(self, berth_number: str):
        """
        Method to update the truck status in the DB
        Args:
            berth_number (str): B$ (B1 or B2)
        """
        start_time, end_time = self._get_start_end_time_for_today()
        query = {
            "berth_number": berth_number,
            "status": "occupied",
            "end_time": {"$gte": start_time, "$lte": end_time},
        }
        actual_data_list = list(self.db_obj.get_data(TruckBerthDB.ACTUAL_DATA, query))
        for actual_data_row in actual_data_list:
            if MAIL_NOTIFICATION:
                # send email notification if the reservation is not made
                if (
                    not actual_data_row["reservation_id"]
                    and not actual_data_row["is_email_notified"]
                ):
                    _msg = f"Truck number: [{actual_data_row['car_number']}]"
                    _msg = _msg + " has arrived without any reservation"
                    notify_by_sendgrid(_msg)
                    update_data = {"$set": {"is_email_notified": True}}
                    _query = {**query, "car_number": actual_data_row["car_number"]}
                    self.db_obj.update_one(TruckBerthDB.ACTUAL_DATA, update_data, _query)

            diff = datetime.now() - actual_data_row["end_time"]
            tolerance_in_secs = TOLERANCE_TIME_MINS * 60
            # Check if the end time has reached the tolerance time
            if diff.seconds >= tolerance_in_secs:
                query = {"_id": actual_data_row["_id"]}
                # Consider that the truck has left
                update_data = {"$set": {"status": "left"}}
                self.logger.info(
                    "[DB][UPDATE] Updated status as left for %s",
                    actual_data_row["car_number"],
                )
                self.db_obj.update_one(TruckBerthDB.ACTUAL_DATA, update_data, query)
