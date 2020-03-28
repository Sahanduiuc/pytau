from abc import ABC, abstractmethod
from typing import Any

from apscheduler.schedulers.base import BaseScheduler
from apscheduler.triggers.base import BaseTrigger
import networkx

from tau.trigger import ImmediateTrigger


class Event(ABC):
    """
    An action that happens at a moment in time.
    """
    @abstractmethod
    def on_activate(self) -> bool:
        """
        Callback made whenever this event gets activated.
        :returns: True if subsequent nodes in the graph should be activated
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
        self.graph = networkx.DiGraph()
        self.activation_flags = dict()

    def connect(self, evt1: Event, evt2: Event):
        self.activation_flags[evt1] = False
        self.activation_flags[evt2] = False
        self.graph.add_edge(evt1, evt2)

    def disconnect(self, evt1: Event, evt2: Event):
        del self.activation_flags[evt1]
        del self.activation_flags[evt2]
        self.graph.remove_edge(evt1, evt2)

    def has_activated(self, evt: Event):
        return self.activation_flags[evt]

    def activate(self, evt: Event):
        nodes = networkx.descendants(self.graph, evt)
        ordering = networkx.topological_sort(networkx.subgraph(self.graph, nodes))
        self.__clear_activation_flags()
        for node in ordering:
            if not node.on_activate():
                break
            else:
                self.activation_flags[node] = True

    def __clear_activation_flags(self):
        self.activation_flags = self.activation_flags.fromkeys(self.activation_flags, False)


class NetworkScheduler:
    def __init__(self, scheduler: BaseScheduler, network: Network = Network()):
        self.scheduler = scheduler
        self.network = network

    def get_network(self):
        return self.network

    def schedule_event(self, evt: Event, trigger: BaseTrigger = ImmediateTrigger()):
        self.scheduler.add_job(lambda: self.network.activate(evt), trigger)

    def schedule_update(self, signal: MutableSignal, value: Any, trigger: BaseTrigger = ImmediateTrigger()):
        def set_and_activate():
            signal.set_value(value)
            self.network.activate(signal)
        self.scheduler.add_job(set_and_activate, trigger)
