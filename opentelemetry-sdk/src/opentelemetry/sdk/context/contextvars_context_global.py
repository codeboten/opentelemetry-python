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

from opentelemetry.context.base_context import BaseContext


async_name = ContextVar("async_name")


class ContextVarsContextGlobal(BaseContext):

    def set(self, key: str, value: Optional["object"]) -> "BaseContext":
        """Set a value in this context"""
        async_name.set(value)

    def get(self, key: str) -> Optional["object"]:
        """Get a value from this context"""
        return async_name.get()


__all__ = ["ContextVarsContextGlobal"]
