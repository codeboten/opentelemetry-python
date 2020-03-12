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
import re
import typing
import urllib.parse

from opentelemetry import correlationcontext
from opentelemetry.context import get_current
from opentelemetry.context.context import Context
from opentelemetry.trace.propagation import httptextformat


class CorrelationContextPropagator(httptextformat.HTTPTextFormat):
    _CORRELATION_CONTEXT_HEADER_NAME = "otcorrelationcontext"

    def extract(
        self,
        get_from_carrier: httptextformat.Getter[
            httptextformat.HTTPTextFormatT
        ],
        carrier: httptextformat.HTTPTextFormatT,
        context: typing.Optional[Context] = None,
    ) -> Context:
        """ Extract CorrelationContext from the carrier.

        See `opentelemetry.trace.propagation.httptextformat.HTTPTextFormat.extract`
        """

        if not context:
            context = get_current()

        header = get_from_carrier(
            carrier, self._CORRELATION_CONTEXT_HEADER_NAME
        )

        if not header:
            return context

        correlations = header.split(",")

        for correlation in correlations:
            try:
                name, value = correlation.split("=", 1)
            except Exception:  # pylint: disable=broad-except
                continue
            context = correlationcontext.set_correlation(
                name.strip(),
                urllib.parse.unquote(value).strip(),
                context=context,
            )

        return context

    def inject(
        self,
        set_in_carrier: httptextformat.Setter[httptextformat.HTTPTextFormatT],
        carrier: httptextformat.HTTPTextFormatT,
        context: typing.Optional[Context] = None,
    ) -> None:
        """Injects CorrelationContext into the carrier.

        See `opentelemetry.trace.propagation.httptextformat.HTTPTextFormat.inject`
        """
        correlations = correlationcontext.get_correlations(context=context)
        if not correlations:
            return

        correlation_context_string = _format_correlations(correlations)
        set_in_carrier(
            carrier,
            self._CORRELATION_CONTEXT_HEADER_NAME,
            correlation_context_string,
        )


def _format_correlations(correlations: typing.Dict[str, object]) -> str:
    """Format correlations into a string.

    Args:
        correlations: the correlations to format

    Returns:
        A string that adheres to the w3c correlationcontext
        header format.
    """
    return ",".join(
        key + "=" + urllib.parse.quote_plus(str(value).lower())
        for key, value in correlations.items()
    )
