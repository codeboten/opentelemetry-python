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

from unittest import TestCase
from asyncio import gather, get_event_loop, sleep as asyncio_sleep
from time import sleep
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
import aiocontextvars  # noqa

from opentelemetry.sdk.context.contextvars_context_global import (
    ContextVarsContextGlobal
)


class TestContextVarsContextGlobal(TestCase):

    def test_async_global(self):

        contextvars_context = ContextVarsContextGlobal()

        async def waiting(async_name, first_sleep, second_sleep):

            await asyncio_sleep(first_sleep)

            contextvars_context.set("async_name", async_name)

            self.assertEqual(
                async_name, contextvars_context.get("async_name")
            )

            await asyncio_sleep(second_sleep)

            self.assertEqual(
                async_name, contextvars_context.get("async_name")
            )

        async def run_waiting():
            await gather(
                waiting("A", 0, 1), waiting("B", 0.1, 3), waiting("C", 2, 1)
            )

        loop = get_event_loop()
        loop.run_until_complete(run_waiting())
        loop.close()

    def test_threading_global(self):

        contextvars_context = ContextVarsContextGlobal()

        def waiting(threading_name, first_sleep, second_sleep):

            sleep(first_sleep)

            contextvars_context.set("threading_name", threading_name)

            self.assertEqual(threading_name, contextvars_context.get())

            sleep(second_sleep)

            self.assertEqual(threading_name, contextvars_context.get())

        def run_waiting():

            threads = []

            for threading_name, first_sleep, second_sleep in [
                ["A", 0, 1], ["B", 0.1, 3], ["C", 2, 1]
            ]:
                thread = Thread(
                    target=waiting,
                    args=(threading_name, first_sleep, second_sleep)
                )
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

        run_waiting()

    def test_futures_global(self):

        contextvars_context = ContextVarsContextGlobal()

        def waiting(thread_pool_name, first_sleep, second_sleep):

            sleep(first_sleep)

            contextvars_context.set("thread_pool_name", thread_pool_name)

            self.assertEqual(thread_pool_name, contextvars_context.get())

            sleep(second_sleep)

            self.assertEqual(thread_pool_name, contextvars_context.get())

        def run_waiting():

            with ThreadPoolExecutor(max_workers=5) as executor:

                for thread_pool_name, first_sleep, second_sleep in [
                    ["A", 0, 1], ["B", 0.1, 3], ["C", 2, 1]
                ]:
                    executor.submit(
                        waiting, thread_pool_name, first_sleep, second_sleep
                    )

        run_waiting()
