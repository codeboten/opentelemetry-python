#!/usr/bin/env python
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

# https://github.com/grpc/grpc/blob/master/examples/python/helloworld/greeter_client.py
# https://github.com/grpc/grpc/blob/v1.16.x/examples/python/interceptors/default_value/greeter_client.py
"""The Python implementation of the GRPC helloworld.Greeter client."""

import logging

import grpc

import helloworld_pb2
import helloworld_pb2_grpc
from opentelemetry import trace
from opentelemetry.ext.grpc import client_interceptor
from opentelemetry.ext.grpc.grpcext import intercept_channel
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleExportSpanProcessor,
)

trace.set_preferred_tracer_provider_implementation(lambda T: TracerProvider())
trace.tracer_provider().add_span_processor(
    SimpleExportSpanProcessor(ConsoleSpanExporter())
)
tracer = trace.get_tracer(__name__)


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel("localhost:50051") as channel:

        channel = intercept_channel(channel, client_interceptor(tracer))

        stub = helloworld_pb2_grpc.GreeterStub(channel)

        # stub.SayHello is a _InterceptorUnaryUnaryMultiCallable
        response = stub.SayHello(helloworld_pb2.HelloRequest(name="YOU"))

    print("Greeter client received: " + response.message)


if __name__ == "__main__":
    logging.basicConfig()
    run()
