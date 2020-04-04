import asyncio
from datetime import timedelta

from tau.core import NetworkScheduler
from tau.event import Do
from tau.signal import Interval, BufferWithCount, BufferWithTime


async def main():
    scheduler = NetworkScheduler()
    network = scheduler.get_network()
    values = Interval(scheduler)
    Do(network, values, lambda: print(f"input values: {values.get_value()}"))

    buffer1 = BufferWithCount(network, values, count=2)
    Do(network, buffer1, lambda: print(f"buffer1 values: {buffer1.get_value()}"))

    buffer2 = BufferWithTime(network, values, timedelta(seconds=5))
    Do(network, buffer2, lambda: print(f"buffer2 values: {buffer2.get_value()}"))

asyncio.get_event_loop().create_task(main())
asyncio.get_event_loop().run_forever()

