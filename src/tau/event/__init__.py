from abc import abstractmethod
from typing import List, Callable, Any

from tau.core.api import Signal, Event, Network


class Function(Signal):
    """
    Base class for streaming functions with zero or more streaming input signals.
    """
    def __init__(self, network: Network, parameters: List):
        super().__init__()
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


class Filter(Function):
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
    def __init__(self, network: Network, values: Signal, mapper: Callable[[Any], Any]):
        super().__init__(network, [values])
        self.values = values
        self.mapper = mapper

    def _call(self):
        if self.values.is_valid():
            next_value = self.values.get_value()
            self._update(self.mapper(next_value))


class ForEach(Event):
    def __init__(self, network: Network, values: Signal, function: Callable[[Any], None]):
        super().__init__()
        self.values = values
        self.function = function
        network.connect(values, self)

    def on_activate(self):
        if self.values.is_valid():
            self.function(self.values.get_value())
