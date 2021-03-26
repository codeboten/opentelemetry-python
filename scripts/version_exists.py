#!/usr/bin/env python3
#
# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import sys
import urllib3
import pathlib


def current_version(package_name):
    version_file = sorted(pathlib.Path(package_name).glob("**/version.py"))[0]

    info = {}
    with open(version_file.absolute()) as f:
        exec(f.read(), info)

    return info["__version__"]


def versions(package_name):
    url = "https://pypi.org/pypi/%s/json" % (package_name,)
    http = urllib3.PoolManager()
    r = http.request("GET", url)
    data = json.loads(r.data.decode("utf-8"))
    return data["releases"].keys()


if __name__ == "__main__":

    package = sys.argv[1]
    version = current_version(package)
    print(version)
    if version in versions(package):
        print("true")
    else:
        print("false")
