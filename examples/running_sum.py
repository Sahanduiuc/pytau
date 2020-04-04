import asyncio

from tau.core import NetworkScheduler
from tau.event import Lambda
from tau.math import RunningSum
from tau.signal import From


async def main():
    scheduler = NetworkScheduler()
    network = scheduler.get_network()
    values = From(scheduler, [0.0, 3.2, 2.1, 2.9, 8.3, 5.7])
    total = RunningSum(network, values)
    Lambda(network, total, lambda x: print(f'{x[0].get_value():.2f}'))

asyncio.run(main())
