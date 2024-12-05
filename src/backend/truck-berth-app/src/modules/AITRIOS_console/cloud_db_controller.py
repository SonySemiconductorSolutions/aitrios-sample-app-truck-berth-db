"""
File: src/truck-berth-app/src/modules/AITRIOS_console/cloud_db_controller.py
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
import warnings

import requests
from common.config import BASE_URL

warnings.filterwarnings("ignore")


class CloudDBController:
    """
    Class to implement cloud DB controller
    """

    def get_latest_inference(self, access_token, device_id):
        """
        Method to get latest uploaded inference
        """
        url = f"{BASE_URL}/devices/{device_id}/inferenceresults"
        if access_token:
            header = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(
                url,
                params={"NumberOfInferenceresults": 1},
                headers=header,
                timeout=300,
                verify=True,
            )
            if response.status_code == 200:
                response = requests.get(
                    url + f'/{response.json()[0]["id"]}',
                    headers=header,
                    timeout=300,
                    verify=True,
                )
            return response
        return "Token not found"
