from abc import abstractmethod
from typing import Callable, Any, List

from apscheduler.triggers.base import BaseTrigger

from tau.core import Signal, Network, MutableSignal, NetworkScheduler, Event
from tau.trigger import ImmediateTrigger


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


class OneShot(MutableSignal):
    def __init__(self, scheduler: NetworkScheduler, values: List,
                 trigger_func: Callable[[Any], BaseTrigger] = ImmediateTrigger):
        for value in values:
            scheduler.schedule_update(self, value, trigger_func())


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
