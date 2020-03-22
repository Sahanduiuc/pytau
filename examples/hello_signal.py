from datetime import timedelta

from tau.core.api import Event, Signal, MutableSignal
from tau.core.singlethreaded import SingleThreadedTimeline


class SayHello(Event):
    def __init__(self, name: Signal):
        self.name = name

    def on_raise(self) -> bool:
        print(f"Hello, {self.name.get_value()}!")
        return False


timeline = SingleThreadedTimeline()
timeline.run()

signal = MutableSignal()
timeline.bind(signal, SayHello(signal))
timeline.raise_signal_after(signal, "world", timedelta(seconds=5))
