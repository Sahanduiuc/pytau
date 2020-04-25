import asyncio
from abc import abstractmethod
from datetime import timedelta
from typing import Callable, Any, List

from tau.core import Signal, Network, MutableSignal, NetworkScheduler, Event


class Function(Signal):
    """
    Base class for streaming functions with zero or more streaming input signals.
    """
    def __init__(self, network: Network, parameters: Any):
        super().__init__()
        if type(parameters) is not list:
            parameters = [parameters]
        self.parameters = parameters
        for param in parameters:
            network.connect(param, self)

    def on_activate(self) -> bool:
        self.modified = False
        self._call()
        return self.modified

    @abstractmethod
    def _call(self):
        pass


class BufferWithCount(Function):
    """
    Operators that transforms a stream of values into batched values, as lists. This particular
    implementation corresponds to rxpy's buffer_with_count operator.

    .. seealso:: http://reactivex.io/documentation/operators/buffer.html
    """
    def __init__(self, network: Network, values: Signal, count: int):
        super().__init__(network, [values])
        self.values = values
        self.count = count
        self.buffer = list()

    def _call(self):
        if self.values.is_valid():
            self.buffer.append(self.values.get_value())
            if len(self.buffer) == self.count:
                self._update(self.buffer.copy())
                self.buffer.clear()


class BufferWithTime(Function):
    """
    Operators that transforms a stream of values into batched values, as lists. This particular
    implementation corresponds to rxpy's buffer_with_time operator.

    .. seealso:: http://reactivex.io/documentation/operators/buffer.html
    """
    def __init__(self, network: Network, values: Signal, interval: timedelta):
        super().__init__(network, [values])
        self.values = values
        self.interval = interval
        self.buffer = list()
        self.timed_out = False

        async def expire_timeout():
            while True:
                await asyncio.sleep(int(self.interval.total_seconds()))
                self.timed_out = True

        asyncio.create_task(expire_timeout())

    def _call(self):
        if self.values.is_valid():
            self.buffer.append(self.values.get_value())
            if self.timed_out:
                self._update(self.buffer.copy())
                self.buffer.clear()
                self.timed_out = False


class Filter(Function):
    """
    Simple operator function that applies a filtering predicate to a stream of values
    and only returns matching values.
    """
    def __init__(self, network: Network, values: Signal, predicate: Callable[[Any], bool]):
        super().__init__(network, [values])
        self.values = values
        self.predicate = predicate

    def _call(self):
        if self.values.is_valid():
            next_value = self.values.get_value()
            if self.predicate(next_value):
                self._update(next_value)


class Map(Function):
    """
    Transforming function that applies a Callable to incoming values and updates the output value.

    .. seealso:: http://reactivex.io/documentation/operators/map.html
    """
    def __init__(self, network: Network, values: Signal, mapper: Callable[[Any], Any]):
        super().__init__(network, [values])
        self.values = values
        self.mapper = mapper

    def _call(self):
        if self.values.is_valid():
            next_value = self.values.get_value()
            self._update(self.mapper(next_value))


class FlatMap(MutableSignal):
    """
    Transforming function that applies a Callable to incoming values and updates the output value.

    .. seealso:: http://reactivex.io/documentation/operators/flatmap.html
    """
    def __init__(self, scheduler: NetworkScheduler, values: Signal):
        super().__init__()
        self.scheduler = scheduler
        self.values = values

        class Handler(Event):
            def __init__(self, outer):
                self.outer = outer

            def on_activate(self) -> bool:
                if values.is_valid():
                    next_values = values.get_value()
                    for next_value in next_values:
                        scheduler.schedule_update(self.outer, next_value)
                    return True
                else:
                    return False

        scheduler.get_network().connect(values, Handler(self))


class Just(MutableSignal):
    """
    Emits a single value immediately.
    .. seealso:: http://reactivex.io/documentation/operators/just.html
    """
    def __init__(self, scheduler: NetworkScheduler, value: Any):
        super().__init__()
        scheduler.schedule_update(self, value)


class From(MutableSignal):
    """
    Emits a list of values immediately, in order.

    .. seealso:: http://reactivex.io/documentation/operators/from.html
    """
    def __init__(self, scheduler: NetworkScheduler, values: List):
        super().__init__()
        for value in values:
            scheduler.schedule_update(self, value)


class Interval(MutableSignal):
    """
    Emits a monotonically increasing sequence of integers spaced out by a given interval of time.

    .. seealso:: http://reactivex.io/documentation/operators/interval.html
    """

    def on_activate(self) -> bool:
        return True

    def __init__(self, scheduler: NetworkScheduler, interval: timedelta = timedelta(seconds=1)):
        super().__init__()
        self.next_value = 0

        async def schedule_update():
            while True:
                self.next_value += 1
                scheduler.schedule_update(self, self.next_value)
                await asyncio.sleep(int(interval.total_seconds()))

        asyncio.create_task(schedule_update())


class Scan(Function):
    """
    Operator that accumulates values in a streaming fashion.

    .. seealso:: http://reactivex.io/documentation/operators/scan.html
    """
    def __init__(self, network: Network, values: Signal):
        super().__init__(network, [values])
        self.prev_value = 0.0

    def _call(self):
        if self.parameters[0].is_valid():
            next_value = self.parameters[0].get_value()
            new_value = self.prev_value + next_value
            self._update(new_value)
            self.prev_value = new_value


class AllActivated(Event):
    """
    An event that activates when all of N input events have activated.
    """
    def __init__(self, network: Network, events: List):
        super().__init__()
        self.network = network
        self.events = events
        self.activated = dict()
        for event in events:
            self.activated[event] = False
            network.connect(event, self)

    def on_activate(self) -> bool:
        for event in self.events:
            if self.network.has_activated(event):
                self.activated[event] = True
        return all(self.activated.values())


class AnyActivated(Event):
    """
    An event that activates when any of N input events activate.
    """
    def __init__(self, network: Network, events: List):
        super().__init__()
        self.network = network
        self.events = events
        self.activated = dict()
        for event in events:
            self.activated[event] = False
            network.connect(event, self)

    """
    An event that activates when all of N input events have activated.
    """
    def on_activate(self) -> bool:
        for event in self.events:
            if self.network.has_activated(event):
                self.activated[event] = True
        return any(self.activated.values())
