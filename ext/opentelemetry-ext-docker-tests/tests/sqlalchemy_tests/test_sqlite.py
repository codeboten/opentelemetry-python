import unittest

import pytest
from sqlalchemy.exc import OperationalError

from opentelemetry import trace

from .mixins import SQLAlchemyTestMixin


class SQLiteTestCase(SQLAlchemyTestMixin, unittest.TestCase):
    """TestCase for the SQLite engine"""

    VENDOR = "sqlite"
    SQL_DB = ":memory:"
    SERVICE = "sqlite"
    ENGINE_ARGS = {"url": "sqlite:///:memory:"}

    def test_engine_execute_errors(self):
        # ensures that SQL errors are reported
        with pytest.raises(OperationalError):
            with self.connection() as conn:
                conn.execute("SELECT * FROM a_wrong_table").fetchall()

        traces = self.pop_traces()
        # trace composition
        self.assertEqual(len(traces), 1)
        span = traces[0]
        # span fields
        self.assertEqual(span.name, "{}.query".format(self.VENDOR))
        self.assertEqual(span.attributes.get("service"), self.SERVICE)
        self.assertEqual(
            span.attributes.get("resource"), "SELECT * FROM a_wrong_table"
        )
        self.assertEqual(span.attributes.get("sql.db"), self.SQL_DB)
        self.assertIsNone(
            span.attributes.get("sql.rows")
        )  # or span.get_metric("sql.rows"))
        self.assertTrue((span.end_time - span.start_time) > 0)
        # check the error
        self.assertEqual(
            span.status.canonical_code,
            trace.status.StatusCanonicalCode.UNKNOWN,
        )
        # TODO: error handling
        # self.assertEqual(span.attributes.get("error.msg"), "no such table: a_wrong_table")
        # self.assertTrue("OperationalError" in span.attributes.get("error.type"))
        # self.assertTrue("OperationalError: no such table: a_wrong_table" in span.attributes.get("error.stack"))
