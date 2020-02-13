# Copyright 2020, OpenTelemetry Authors
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

import typing
from abc import ABC, abstractmethod


class Context(typing.Dict[str, object]):
    """ An immutable dictionary. Implemented as in PEP 351:
        https://www.python.org/dev/peps/pep-0351/
    """

    def __hash__(self) -> None:
        return id(self)

    def _immutable(self, *args, **kws):
        # pylint: disable=no-self-use
        raise TypeError("object is immutable")

    __setitem__ = _immutable
    __delitem__ = _immutable
    clear = _immutable
    update = _immutable
    setdefault = _immutable
    pop = _immutable
    popitem = _immutable


class RuntimeContext(ABC):
    """The RuntimeContext interface provides a wrapper for the different
    mechanisms that are used to propagate context in Python.
    Implementations can be made available via entry_points and
    selected through environment variables.
    """

    @abstractmethod
    def set_current(self, context: Context) -> None:
        """ Sets the current `Context` object.

        Args:
            context: The Context to set.
        """

    @abstractmethod
    def get_current(self) -> Context:
        """ Returns the current `Context` object. """


__all__ = ["Context", "RuntimeContext"]
