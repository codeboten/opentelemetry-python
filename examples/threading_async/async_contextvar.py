from asyncio import sleep, gather, get_event_loop
from contextvars import ContextVar

local_name = ContextVar("async_name")


async def waiting(async_name, first_sleep, second_sleep):

    await sleep(first_sleep)

    local_name.set(async_name)

    print("async_name:\t{}".format(async_name))
    print("local_name:\t{}".format(local_name.get()))
    print()

    await sleep(second_sleep)

    print("async_name:\t{}".format(async_name))
    print("local_name:\t{}".format(local_name.get()))
    print()


async def main():
    await gather(waiting("A", 0, 1), waiting("B", 0.1, 3), waiting("C", 2, 1))

loop = get_event_loop()
loop.run_until_complete(main())
loop.close()
