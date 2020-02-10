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
import typing
from copy import copy

from opentelemetry.context import RuntimeContext


class ThreadLocalRuntimeContext(RuntimeContext):
    """An implementation of the RuntimeContext interface
    which uses thread-local storage under the hood. This
    implementation is available for usage with Python 3.4.
    """

    def __init__(self) -> None:
        self._thread_local = threading.local()

    def set_value(self, key: str, value: "object") -> None:
        """See `opentelemetry.context.RuntimeContext.set_value`."""
        setattr(self._thread_local, key, value)

    def get_value(self, key: str) -> "object":
        """See `opentelemetry.context.RuntimeContext.get_value`."""
        try:
            got = getattr(self._thread_local, key)  # type: object
            return got
        except AttributeError:
            return None

    def remove_value(self, key: str) -> None:
        """See `opentelemetry.context.RuntimeContext.remove_value`."""
        try:
            delattr(self._thread_local, key)
        except AttributeError:
            pass

    def copy(self) -> RuntimeContext:
        """See `opentelemetry.context.RuntimeContext.copy`."""

        context_copy = ThreadLocalRuntimeContext()

        for key, value in self._thread_local.__dict__.items():
            context_copy.set_value(key, copy(value))

        return context_copy

    def snapshot(self) -> typing.Dict[str, "object"]:
        """See `opentelemetry.context.RuntimeContext.snapshot`."""
        return dict(
            (key, value) for key, value in self._thread_local.__dict__.items()
        )

    def apply(self, snapshot: typing.Dict[str, "object"]) -> None:
        """See `opentelemetry.context.RuntimeContext.apply`."""
        diff = set(self._thread_local.__dict__) - set(snapshot)
        for key in diff:
            self._thread_local.__dict__.pop(key, None)
        for name in snapshot:
            self.set_value(name, snapshot[name])


__all__ = ["ThreadLocalRuntimeContext"]
