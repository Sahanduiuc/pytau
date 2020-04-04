import asyncio

from tau.core import NetworkScheduler
from tau.event import Do
from tau.signal import From, Filter


async def main():
    scheduler = NetworkScheduler()
    network = scheduler.get_network()
    values = From(scheduler, [0.0, -3.2, 2.1, -2.9, 8.3, -5.7])
    filt = Filter(network, values, lambda x: x >= 0.0)
    Do(network, filt, lambda: print(f"{filt.get_value()}"))

asyncio.run(main())



