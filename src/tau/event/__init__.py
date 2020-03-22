from abc import abstractmethod
from typing import List, Callable, Any

from tau.core.api import Signal, Timeline, Event


class Function(Signal):
    """
    Base class for streaming functions with zero or more streaming input signals.
    """
    def __init__(self, timeline: Timeline, parameters: List):
        super().__init__()
        self.parameters = parameters
        for param in parameters:
            # noinspection PyTypeChecker
            timeline.bind(param, self)

    def on_raise(self):
        self.modified = False
        self._call()
        return self.modified

    @abstractmethod
    def _call(self):
        pass


class Filter(Function):
    def __init__(self, timeline: Timeline, values: Signal, predicate: Callable[[Any], bool]):
        super().__init__(timeline, [values])
        self.values = values
        self.predicate = predicate

    def _call(self):
        if self.values.is_valid():
            next_value = self.values.get_value()
            if self.predicate(next_value):
                self._update(next_value)


class Map(Function):
    def __init__(self, timeline: Timeline, values: Signal, mapper: Callable[[Any], Any]):
        super().__init__(timeline, [values])
        self.values = values
        self.mapper = mapper

    def _call(self):
        if self.values.is_valid():
            next_value = self.values.get_value()
            self._update(self.mapper(next_value))


class ForEach(Event):
    def __init__(self, timeline: Timeline, values: Signal, function: Callable[[Any], None]):
        super().__init__()
        self.values = values
        self.function = function
        timeline.bind(values, self)

    def on_raise(self) -> bool:
        if self.values.is_valid():
            self.function(self.values.get_value())
        return True
