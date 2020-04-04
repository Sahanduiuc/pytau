import asyncio

from tau.core import NetworkScheduler
from tau.event import Do
from tau.signal import Interval, Scan


async def main():
    scheduler = NetworkScheduler()
    network = scheduler.get_network()
    values = Interval(scheduler)
    accumulator = Scan(network, values)
    Do(network, accumulator, lambda: print(f"{accumulator.get_value()}"))

asyncio.get_event_loop().create_task(main())
asyncio.get_event_loop().run_forever()
