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

import threading

from opentelemetry.context.base_context import BaseContext


class ThreadLocalRuntimeContext(BaseContext):

    _default = None

    def __init__(self, name: str, default: "object"):
        super(ThreadLocalRuntimeContext).__init__(name, default)

        self._thread_local = threading.local()

    def clear(self) -> None:
        # FIXME iterate through all the thread_local attributes and set them
        # to the default value
        setattr(self._thread_local, self.name, self.default())

    def get_value(self, name: "str") -> "object":
        try:
            return getattr(self._thread_local, name)

        except AttributeError:
            self.set_value(name, self._default)
            return self._default

    def set_value(self, name, value: "object") -> None:
        setattr(self._thread_local, name, value)


__all__ = ["ThreadLocalRuntimeContext"]
