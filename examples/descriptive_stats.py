import asyncio

from tau.core import NetworkScheduler
from tau.event import Lambda
from tau.signal import From
from tau.math import Max, Mean, Min, Stddev


async def main():
    scheduler = NetworkScheduler()
    network = scheduler.get_network()
    values = From(scheduler, [0.0, 3.2, 2.1, 2.9, 8.3, 5.7])

    max_value = Max(network, values)
    min_value = Min(network, values)
    avg = Mean(network, values)
    stddev = Stddev(network, values)

    # noinspection PyUnusedLocal
    def print_stats(params):
        print(f"min = {min_value.get_value()}; max = {max_value.get_value()}; "
              f"avg = {avg.get_value():.2f}; stddev = {stddev.get_value():.2f}")

    Lambda(network, [min_value, max_value, avg, stddev], print_stats)

asyncio.run(main())
