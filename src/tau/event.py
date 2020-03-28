from typing import Callable, Any

from tau.core import Signal, Event, Network


class Lambda(Event):
    """
    A helper implementation of Event that binds any Python function to zero or more Event parameters
    """
    def __init__(self, network: Network, parameters: Any, function: Callable[[Any], Any]):
        super().__init__()
        if type(parameters) is not list:
            parameters = [parameters]

        self.parameters = parameters
        for param in parameters:
            network.connect(param, self)
        self.function = function

    def on_activate(self) -> bool:
        return self.function(self.parameters)


class ForEach(Event):
    def __init__(self, network: Network, values: Signal, function: Callable[[Any], Any]):
        super().__init__()
        self.values = values
        self.function = function
        network.connect(values, self)

    def on_activate(self) -> bool:
        if self.values.is_valid():
            self.function(self.values.get_value())
        return False