import asyncio
from abc import ABC, abstractmethod
from typing import Any

import networkx


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
    """
    A signal whose value can be updated programmatically.
    """
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
    """
    A graph network connecting Events.
    """
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

    # noinspection PyCallingNonCallable
    def activate(self, evt: Event):
        nodes = networkx.descendants(self.graph, evt)
        ordering = networkx.topological_sort(networkx.subgraph(self.graph, nodes))
        self.__clear_activation_flags()

        # process the originating node
        if not evt.on_activate():
            return
        else:
            self.activation_flags[evt] = True

        # process the node's descendants
        for node in ordering:
            if not node.on_activate():
                # skip forward to the next terminal node
                skipping = True
                while skipping:
                    node = next(ordering, None)
                    if not node or self.graph.out_degree(node) == 0:
                        skipping = False
            else:
                self.activation_flags[node] = True

    def __clear_activation_flags(self):
        self.activation_flags = self.activation_flags.fromkeys(self.activation_flags, False)


class NetworkScheduler:
    """
    A higher-level scheduler object sitting on top of asyncio that provides natural operations for
    scheduling events connected in a Network.
    """
    def __init__(self, network: Network = Network()):
        self.network = network

    def get_network(self):
        return self.network

    def schedule_event(self, evt: Event):
        asyncio.get_event_loop().call_soon(lambda: self.network.activate(evt))

    def schedule_update(self, signal: MutableSignal, value: Any):
        def set_and_activate():
            signal.set_value(value)
            self.network.activate(signal)
        asyncio.get_event_loop().call_soon(set_and_activate)
