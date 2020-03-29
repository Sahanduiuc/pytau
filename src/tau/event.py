from typing import Callable, Any

from tau.core import Event, Network


class Lambda(Event):
    """
    A helper implementation of Event that binds any Python function to zero or more Event parameters.
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


class Do(Event):
    """
    A simple operator that executes a function whenever an Event fires; a more limited form of
    Lambda, which lets you connect to multiple upstream parameters and pass them to the function.

    .. seealso:: http://reactivex.io/documentation/operators/do.html
    """
    def __init__(self, network: Network, event: Event, function: Callable[[], Any]):
        super().__init__()
        self.event = event
        self.function = function
        network.connect(event, self)

    def on_activate(self) -> bool:
        self.function()
        return True
