import asyncio

from tau.core import NetworkScheduler
from tau.event import Lambda
from tau.signal import From


async def main():
    scheduler = NetworkScheduler()
    signal = From(scheduler, ["world"])
    Lambda(scheduler.get_network(), signal, lambda x: print(f"Hello, {x[0].get_value()}!"))

asyncio.run(main())
