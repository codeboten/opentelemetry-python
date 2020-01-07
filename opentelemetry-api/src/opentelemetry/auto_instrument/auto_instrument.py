#!/usr/bin/env python3

# Copyright 2019, OpenTelemetry Authors
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

from distutils.spawn import find_executable
from os import environ, execl
from os.path import dirname
from sys import argv


def run() -> None:
    environ["PYTHONPATH"] = dirname(__file__)
    python3 = find_executable(argv[1])
    execl(python3, python3, *argv[2:])  # type: ignore


if __name__ == "__main__":
    run()
