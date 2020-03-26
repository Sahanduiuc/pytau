from abc import ABC, abstractmethod
from typing import Any

import networkx
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.triggers.base import BaseTrigger


class Event(ABC):
    """
    An action that happens at a moment in time.
    """
    def __init__(self):
        self.propagate = True

    @abstractmethod
    def on_activate(self) -> bool:
        """
        Callback made whenever this event gets activated.
        :return: False if you do not wish successor events to be activated
        """
        pass


class Signal(Event, ABC):
    """
    An Event with a value associated with it.
    """
    def __init__(self, initial_value: Any = None):
        super().__init__()
        self.value = initial_value
        self.modified = False

    def is_valid(self) -> bool:
        """
        :return: True if the value is non-None (default behavior; may be subclassed)
        """
        return self.value is not None

    def get_value(self) -> Any:
        """
        Gets the current value of the signal; may be None.
        """
        return self.value

    def _update(self, value):
        """
        Internal method for updating the value of the signal; used it subclasses.
        """
        self.value = value
        self.modified = True


class MutableSignal(Signal):
    def __init__(self, initial_value: Any = None):
        super().__init__(initial_value)

    def on_activate(self):
        if self.modified:
            self.modified = False
            return True
        else:
            return False

    def set_value(self, value: Any):
        self._update(value)


class Network:
    def __init__(self):
        self.graph = networkx.Graph()

    def connect(self, evt1: Event, evt2: Event):
        self.graph.add_edge(evt1, evt2)

    def disconnect(self, evt1: Event, evt2: Event):
        self.graph.remove_edge(evt1, evt2)

    def activate(self, evt: Event):
        ordering = networkx.dfs_preorder_nodes(self.graph, evt)
        for node in ordering:
            if not node.on_activate():
                break


class NetworkScheduler:
    def __init__(self, scheduler: BaseScheduler, network: Network):
        self.scheduler = scheduler
        self.network = network

    def schedule_event(self, evt: Event, trigger: BaseTrigger):
        self.scheduler.add_job(lambda: self.network.activate(evt), trigger)

    def schedule_update(self, signal: MutableSignal, value: Any, trigger: BaseTrigger):
        def set_and_activate():
            signal.set_value(value)
            self.network.activate(signal)
        self.scheduler.add_job(set_and_activate, trigger)
