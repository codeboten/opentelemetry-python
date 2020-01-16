from threading import Thread, local
from time import sleep

local_name = local()


def waiting(threading_name, first_sleep, second_sleep):

    sleep(first_sleep)

    local_name.threading_name = threading_name

    print("thread_name:\t{}".format(threading_name))
    print("local_name:\t{}".format(local_name.threading_name))
    print()

    sleep(second_sleep)

    print("thread_name:\t{}".format(threading_name))
    print("local_name:\t{}".format(local_name.threading_name))
    print()


def main():

    threads = []

    for threading_name, first_sleep, second_sleep in [
        ["A", 0, 1], ["B", 0.1, 3], ["C", 2, 1]
    ]:
        thread = Thread(
            target=waiting, args=(threading_name, first_sleep, second_sleep)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


main()
