from abc import ABC, abstractmethod
from datetime import timedelta, datetime
from typing import Any

from datetimerange import DateTimeRange


class Event(ABC):
    @abstractmethod
    def on_raise(self) -> bool:
        pass


class Signal(Event, ABC):
    def __init__(self, initial_value: Any = None):
        self.value = initial_value
        self.modified = False

    def is_valid(self) -> bool:
        return self.value is not None

    def get_value(self) -> Any:
        return self.value

    def _update(self, value):
        self.value = value
        self.modified = True


class MutableSignal(Signal):
    def on_raise(self) -> bool:
        if self.modified:
            self.modified = False
            return True
        else:
            return False

    def set_value(self, value: Any):
        self._update(value)


class Timeline(ABC):
    def __init__(self):
        self.epoch = 0
        self.running = False
        self.run_time = DateTimeRange()

    def get_epoch(self):
        return self.epoch

    def is_running(self) -> bool:
        return self.running

    def get_run_time(self) -> DateTimeRange:
        return self.run_time

    @abstractmethod
    def bind(self, evt1: Event, evt2: Event):
        pass

    @abstractmethod
    def unbind(self, evt1: Event, evt2: Event):
        pass

    @abstractmethod
    def raise_event(self, evt: Event):
        pass

    @abstractmethod
    def raise_event_after(self, evt: Event, duration: timedelta):
        pass

    @abstractmethod
    def raise_event_at(self, evt: Event, at_time: datetime):
        pass

    @abstractmethod
    def raise_signal(self, signal: MutableSignal, value):
        pass

    @abstractmethod
    def raise_signal_after(self, signal: MutableSignal, value, duration: timedelta):
        pass

    @abstractmethod
    def raise_signal_at(self, signal: MutableSignal, value, at_time: datetime):
        pass

    @abstractmethod
    def run(self, run_time: DateTimeRange = DateTimeRange()):
        pass

    @abstractmethod
    def shutdown(self):
        pass

