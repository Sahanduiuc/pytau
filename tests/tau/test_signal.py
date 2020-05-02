import asyncio

from tau.core import NetworkScheduler
from tau.event import Do
from tau.signal import From, Map, Scan, Filter


def test_hello_world():
    async def main():
        scheduler = NetworkScheduler()
        signal = From(scheduler, ["world"])
        Do(scheduler.get_network(), signal, lambda: print(f"Hello, {signal.get_value()}!"))

    asyncio.run(main())


def test_map_reduce():
    check_values = []

    async def main():
        scheduler = NetworkScheduler()
        network = scheduler.get_network()
        values = From(scheduler, [0.0, 3.2, 2.1, 2.9, 8.3, 5.7])
        mapper = Map(network, values, lambda x: round(x))
        accumulator = Scan(network, mapper)
        check_values.append(accumulator)
        Do(network, accumulator, lambda: print(f"{accumulator.get_value()}"))

    asyncio.run(main())
    assert check_values[0].get_value() == 22.0


def test_filter():
    check_values = []

    async def main():
        scheduler = NetworkScheduler()
        network = scheduler.get_network()
        values = From(scheduler, [0.0, -3.2, 2.1, -2.9, 8.3, -5.7])
        filt = Filter(network, values, lambda x: x >= 0.0)
        check_values.append(filt)
        Do(network, filt, lambda: print(f"{filt.get_value()}"))

    asyncio.run(main())
    assert check_values[0].get_value() == 8.3
