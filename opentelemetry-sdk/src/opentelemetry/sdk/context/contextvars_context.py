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

from contextvars import ContextVar, get_context

from opentelemetry.context.base_context import BaseContext


class ContextVarsContext(BaseContext):

    def __init__(self):
        super(ContextVarsContext).__init__(name, default)

        self._context = get_context()

    @abstractmethod
    def set(self, key: str, value: Optional["object"]) -> "BaseContext":
        """Set a value in this context"""

    @abstractmethod
    def get(self, key: str) -> Optional["object"]:
        """Get a value from this context"""

    def get_value(self, name: "str") -> "object":
        try:
            return getattr(self._thread_local, name)

        except AttributeError:
            # FIXME This is a quite obscure behavior that can easily cause
            # significant confusion to an user.
            self.set_value(name, self._default)
            return self._default

    def set_value(self, name, value: "object") -> None:
        # FIXME Finish this method

        ContextVar
        setattr(self._thread_local, name, value)


__all__ = ["AsyncRuntimeContext"]
