"""
File: logger.py
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


import logging
import os

log_level = os.environ.get("TB_DEBUG_LEVEL")
logging.getLogger("paramiko").setLevel(logging.WARNING)
LOG_FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"

logging.basicConfig(
    filename="truckberthapp.log", level=logging.DEBUG, filemode="w", format=LOG_FORMAT
)

# create logger
logger = logging.getLogger("tbapp")

# logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
if log_level == "INFO":
    ch.setLevel(logging.INFO)
elif log_level == "DEBUG":
    ch.setLevel(logging.DEBUG)
elif log_level == "ERROR":
    ch.setLevel(logging.ERROR)

# ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter(LOG_FORMAT)

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
