import os
import unittest

import sqlalchemy

from opentelemetry import trace
from opentelemetry.instrumentation.sqlalchemy import patch, unpatch

from .utils import TracerTestBase

POSTGRES_CONFIG = {
    "host": "127.0.0.1",
    "port": int(os.getenv("TEST_POSTGRES_PORT", "5432")),
    "user": os.getenv("TEST_POSTGRES_USER", "testuser"),
    "password": os.getenv("TEST_POSTGRES_PASSWORD", "testpassword"),
    "dbname": os.getenv("TEST_POSTGRES_DB", "opentelemetry-tests"),
}


class SQLAlchemyPatchTestCase(TracerTestBase, unittest.TestCase):
    """TestCase that checks if the engine is properly traced
    when the `patch()` method is used.
    """

    def setUp(self):
        # create a traced engine with the given arguments
        # and configure the current PIN instance
        patch()
        dsn = (
            "postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(dbname)s"
            % POSTGRES_CONFIG
        )
        self.engine = sqlalchemy.create_engine(dsn)

        # prepare a connection
        self.conn = self.engine.connect()
        self._span_exporter.clear()

    def tearDown(self):
        super(SQLAlchemyPatchTestCase, self).tearDown()

        # clear the database and dispose the engine
        self.conn.close()
        self.engine.dispose()
        unpatch()

    def test_engine_traced(self):
        # ensures that the engine is traced
        rows = self.conn.execute("SELECT 1").fetchall()
        assert len(rows) == 1

        traces = self.pop_traces()
        # trace composition
        assert len(traces) == 1
        span = traces[0]
        # check subset of span fields
        assert span.name == "postgres.query"
        assert span.attributes.get("service") == "postgres"
        assert (
            span.status.canonical_code == trace.status.StatusCanonicalCode.OK
        )
        assert (span.end_time - span.start_time) > 0
