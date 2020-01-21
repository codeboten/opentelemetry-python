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

from typing import Optional
from contextvars import ContextVar
# from sys import modules

from opentelemetry.context.base_context import BaseContext


# async_name = ContextVar("async_name")


class ContextVarsContext(BaseContext):

    # _instance = None
    # _module = modules[__name__]
    # _module = __import__(__name__)

    # def __new__(cls):
    #     if ContextVarsContext._instance is None:
    #         ContextVarsContext._instance = object.__new__(cls)
    #
    #     return ContextVarsContext._instance

    def __init__(self):
        self._contextvars = {}

    def set(self, key: str, value: Optional["object"]) -> "BaseContext":
        """Set a value in this context"""
        # contextvar = ContextVar(key)
        # contextvar.set(value)
        # setattr(self._module, f"_{key}", contextvar)
        # setattr(self, f"_{key}", contextvar)
        # async_name.set(value)
        self._contextvars[key] = ContextVar(key)
        self._contextvars[key].set(value)
        # print("sdf" + self._contextvars[key].get())
        # globals()[key] = ContextVar(key)
        # globals()[key].set(value)

    def get(self, key: str) -> Optional["object"]:
        """Get a value from this context"""
        # return getattr(self._module, f"_{key}").get(key)
        # return getattr(self, f"_{key}").get(key)
        # return async_name.get()
        return self._contextvars[key].get()
        # return globals()[key].get()


__all__ = ["ContextVarsContext"]
