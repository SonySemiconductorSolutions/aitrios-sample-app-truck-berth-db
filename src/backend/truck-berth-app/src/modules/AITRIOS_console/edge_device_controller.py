"""
File: src/truck-berth-app/src/modules/AITRIOS_console/edge_device_controller.py
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
import base64

import requests
from common.config import BASE_URL
from modules.cloudapp.SmartCamera import BoundingBox2d, PerceptionResult


class EdgeDeviceController:
    """
    Edge Device controller
    """

    def __init__(self, access_token):
        self.access_token = access_token

    def start_upload_inference(self, device_id):
        """
        Method to start upload inference
        """
        url = f"{BASE_URL}/devices/{device_id}/inferenceresults/collectstart"
        if self.access_token:
            header = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.post(url, headers=header, timeout=300, verify=True)
            return response
        return "Token not found"

    def stop_upload_inference(self, device_id):
        """
        Method to stop upload inference
        """
        url = f"{BASE_URL}/devices/{device_id}/inferenceresults/collectstop"
        if self.access_token:
            header = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.post(url, headers=header, timeout=300, verify=True)
            return response
        return "Token not found"

    def _deserialize(self, output_meta_data):
        """
        Method to deserialize the inferred data

        Args:
            output_meta_data
        """
        # Call the main method to deserialize
        ppl_out = PerceptionResult.PerceptionResult.GetRootAsPerceptionResult(output_meta_data, 0)

        image_info = ppl_out.Image()

        image_dict = {
            "camera_id": image_info.CameraId(),
            "channel": image_info.Channel(),
            "width": image_info.Width(),
            "height": image_info.Height(),
            "pixel_format": image_info.PixelFormat(),
            "timestamp": image_info.Timestamp(),
        }

        slot_len = ppl_out.SlotListLength()

        slot_dict = []
        for i in range(slot_len):
            slot_data = ppl_out.SlotList(i)

            car_data = slot_data.Car()

            lp_data = car_data.LicensePlate()
            lp_box = BoundingBox2d.BoundingBox2d()
            lp_box.Init(lp_data.BoundingBox().Bytes, lp_data.BoundingBox().Pos)

            lp_text = lp_data.PlateText()

            # Prepare output dict
            slot_dict += [
                {
                    "camera_id": slot_data.CameraId(),
                    "car": {
                        "bounding_box_score": car_data.BoundingBoxScore(),
                        "license_plate": {
                            "bounding_box": {
                                "top": lp_box.Top(),
                                "left": lp_box.Left(),
                                "bottom": lp_box.Bottom(),
                                "right": lp_box.Right(),
                            },
                            "bounding_box_score": lp_data.BoundingBoxScore(),
                            "license_plate_text": {
                                "plate_number": lp_text.PlateNumber().decode("utf-8"),
                            },
                        },
                    },
                    "timestamp": slot_data.Timestamp(),
                }
            ]

        deserialize_dict = {"image": image_dict, "slot_list": slot_dict, "type": ppl_out.Type()}

        return deserialize_dict

    def get_deserialized_data(self, lpd_meta_data):
        """
        Args:
            lpd_meta_data
        """
        # Decode base64
        lpd_meta_data = base64.b64decode(lpd_meta_data)
        # Deserialize the decoded base64 data
        deserialize_lpd_meta_data = self._deserialize(lpd_meta_data)

        return deserialize_lpd_meta_data
