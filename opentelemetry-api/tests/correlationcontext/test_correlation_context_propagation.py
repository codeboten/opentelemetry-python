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
#
import typing
import unittest

from opentelemetry import correlationcontext
from opentelemetry.context import get_current
from opentelemetry.correlationcontext.propagation import (
    CorrelationContextPropagator,
)


def get_as_list(
    dict_object: typing.Dict[str, typing.List[str]], key: str
) -> typing.List[str]:
    value = dict_object.get(key)
    return value if value is not None else []


class TestCorrelationContextPropagation(unittest.TestCase):
    def setUp(self):
        self.propagator = CorrelationContextPropagator()

    def _extract(self, header_value):
        """Test helper"""
        header = {"otcorrelationcontext": [header_value]}
        return correlationcontext.get_correlations(
            self.propagator.extract(get_as_list, header)
        )

    def _inject(self, values):
        """Test helper"""
        ctx = get_current()
        for k, v in values.items():
            ctx = correlationcontext.set_correlation(k, v, context=ctx)
        output = {}
        self.propagator.inject(dict.__setitem__, output, context=ctx)
        print(output)
        return output.get("otcorrelationcontext")

    def test_no_context_header(self):
        header = ""
        self.assertEqual(self._extract(header), {})

    def test_valid_header(self):
        header = "key1=val1,key2=val2"
        expected = {"key1": "val1", "key2": "val2"}
        self.assertEqual(self._extract(header), expected)

    def test_valid_header_with_space(self):
        header = "key1 =   val1,  key2 =val2   "
        expected = {"key1": "val1", "key2": "val2"}
        self.assertEqual(self._extract(header), expected)

    def test_valid_header_with_properties(self):
        header = "key1=val1,key2=val2;prop=1"
        expected = {"key1": "val1", "key2": "val2;prop=1"}
        self.assertEqual(self._extract(header), expected)

    def test_valid_header_with_url_escaped_comma(self):
        header = "key1=val1,key2=val2%2Cval3"
        expected = {"key1": "val1", "key2": "val2,val3"}
        self.assertEqual(self._extract(header), expected)

    def test_valid_header_with_invalid_value(self):
        header = "key1=val1,key2=val2,a,val3"
        expected = {"key1": "val1", "key2": "val2"}
        self.assertEqual(self._extract(header), expected)

    def test_valid_header_with_empty_value(self):
        header = "key1=,key2=val2"
        expected = {"key1": "", "key2": "val2"}
        self.assertEqual(self._extract(header), expected)

    def test_invalid_header(self):
        header = "header1"
        expected = {}
        self.assertEqual(self._extract(header), expected)

    def test_inject(self):
        values = {
            "key1": "val1",
            "key2": "val2",
        }
        output = self._inject(values)
        self.assertIn("key1=val1", output)
        self.assertIn("key2=val2", output)

    def test_inject_escaped_values(self):
        values = {
            "key1": "val1,val2",
            "key2": "val3=4",
        }
        output = self._inject(values)
        self.assertIn("key1=val1%2Cval2", output)
        self.assertIn("key2=val3%3D4", output)

    def test_inject_non_string_values(self):
        values = {
            "key1": True,
            "key2": 123,
            "key3": 123.567,
        }
        output = self._inject(values)
        self.assertIn("key1=true", output)
        self.assertIn("key2=123", output)
        self.assertIn("key3=123.567", output)
