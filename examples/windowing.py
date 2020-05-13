import asyncio

from tau.core import NetworkScheduler
from tau.event import Do
from tau.signal import Interval, WindowWithCount


async def main():
    scheduler = NetworkScheduler()
    network = scheduler.get_network()
    values = Interval(scheduler)
    Do(network, values, lambda: print(f"input values: {values.get_value()}"))

    window = WindowWithCount(network, values, count=5)
    Do(network, window, lambda: print(f"window values: {window.get_value()}"))

asyncio.get_event_loop().create_task(main())
asyncio.get_event_loop().run_forever()

