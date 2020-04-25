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

"""
Instrument `sqlalchemy`_ to report SQL queries.

There are two options for instrumenting code. The first option is to use
the `opentelemetry-auto-instrumentation` executable which will automatically
instrument your SQLAlchemy engine. The second is to programmatically enable
instrumentation via the following code:

.. _sqlalchemy: https://pypi.org/project/sqlalchemy/
Usage
-----
.. code:: python

    from opentelemetry import trace
    from opentelemetry.ext.sqlalchemy import SQLAlchemyInstrumentor
    from opentelemetry.sdk.trace import TracerProvider
    import sqlalchemy

    trace.set_tracer_provider(TracerProvider())
    trace_engine(engine, trace.get_tracer_provider())

API
---
"""
import sqlalchemy
import wrapt
from wrapt import wrap_function_wrapper as _w

from opentelemetry.auto_instrumentation.instrumentor import BaseInstrumentor
from opentelemetry.ext.sqlalchemy.engine import _wrap_create_engine


def _unwrap(obj, attr):
    func = getattr(obj, attr, None)
    if (
        func
        and isinstance(func, wrapt.ObjectProxy)
        and hasattr(func, "__wrapped__")
    ):
        setattr(obj, attr, func.__wrapped__)


class SQLAlchemyInstrumentor(BaseInstrumentor):
    """An instrumentor for SQLAlchemy
    See `BaseInstrumentor`
    """

    def _instrument(self, **kwargs):
        _w("sqlalchemy", "create_engine", _wrap_create_engine)
        _w("sqlalchemy.engine", "create_engine", _wrap_create_engine)

    def _uninstrument(self, **kwargs):
        _unwrap(sqlalchemy, "create_engine")
        _unwrap(sqlalchemy.engine, "create_engine")
