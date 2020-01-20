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
from contextvars import ContextVar, get_context

from opentelemetry.context.base_context import BaseContext


class ContextVarsContext(BaseContext):

    _instance = None

    def __new__(cls):
        if ContextVarContext._instance is None:
            ContextVarContext._instance = object.__new__(cls)

        return ContextVarContext._instance

    def set(self, key: str, value: Optional["object"]) -> "BaseContext":
        """Set a value in this context"""
        contextvar = ContextVar(key)
        contextvar.set(value)
        setattr(self, f"_{key}", contextvar)


    def get(self, key: str) -> Optional["object"]:
        """Get a value from this context"""
        return getattr(self, f"_{key}").get()


__all__ = ["ContextVarsContext"]
