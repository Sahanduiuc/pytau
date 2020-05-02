import asyncio
import math

from tau.core import NetworkScheduler
from tau.event import Lambda
from tau.math import RunningSum, Max, Min, Mean, Stddev
from tau.signal import From


def test_running_sum():
    check_values = []

    async def main():
        scheduler = NetworkScheduler()
        network = scheduler.get_network()
        values = From(scheduler, [0.0, 3.2, 2.1, 2.9, 8.3, 5.7])
        total = RunningSum(network, values)
        check_values.append(total)
        Lambda(network, total, lambda x: print(f'{x[0].get_value():.2f}'))

    asyncio.run(main())
    assert check_values[0].get_value() == 22.2


def test_descriptive_stats():
    check_values = []

    async def main():
        scheduler = NetworkScheduler()
        network = scheduler.get_network()
        values = From(scheduler, [0.0, 3.2, 2.1, 2.9, 8.3, 5.7])

        max_value = Max(network, values)
        min_value = Min(network, values)
        avg = Mean(network, values)
        stddev = Stddev(network, values)

        check_values.extend([max_value, min_value, avg, stddev])

        # noinspection PyUnusedLocal
        def print_stats(params):
            print(f"min = {min_value.get_value()}; max = {max_value.get_value()}; "
                  f"avg = {avg.get_value():.2f}; stddev = {stddev.get_value():.2f}")

        Lambda(network, [min_value, max_value, avg, stddev], print_stats)

    asyncio.run(main())
    assert check_values[0].get_value() == 8.3
    assert check_values[1].get_value() == 0.0
    assert check_values[2].get_value() == 3.7
    assert math.isclose(check_values[3].get_value(), 3.24507, abs_tol=0.00001)
