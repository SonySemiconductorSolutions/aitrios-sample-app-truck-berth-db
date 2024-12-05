"""
File: src/console_app/setup.py
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

import subprocess

# Always prefer setuptools over distutils
from setuptools import find_packages, setup


def get_version():
    """
    Get version from text file
    """
    filename = "./version.txt"
    with open(filename, "r", encoding="utf-8") as fh_:
        lines = fh_.read().splitlines()

    version = lines[0].split(",")[0]
    return version


def get_commit_id():
    """
    Get commit ID to include in wheel file
    """
    try:
        commit_id = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).strip()
        return commit_id.decode("utf-8")
    except subprocess.CalledProcessError:
        return "unknowncommit"


def get_requirements():
    """
    Get requirements list
    """
    filename = "./requirements.txt"
    with open(filename, "r", encoding="utf-8") as fh_:
        lines = fh_.read().splitlines()

    # Remove empty lines and comments from the list of lines
    requirements = [
        line.strip() for line in lines if line.strip() and not line.strip().startswith("#")
    ]
    return requirements


PACKAGE_NAME = "truck-berth-app-cli"
PACKAGE_VERSION = get_version()
COMMIT_ID = get_commit_id()
AUTHOR_NAME = "Sony Semiconductor Solutions Corporation"
AUTHOR_EMAIL = "aaa@xxx.com"


setup(
    name=PACKAGE_NAME,
    version=f"{PACKAGE_VERSION}+{COMMIT_ID}",
    description="Truck Berth CLI",
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: Confidential :: Sony Semiconductor Solutions Corporation",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=find_packages(),
    python_requires=">=3.6, <4",
    install_requires=get_requirements(),
    entry_points={
        "console_scripts": [
            "truck-berth-app=truck_berth_app.truck_berth_app:truck_berth_main",
        ]
    },
)
