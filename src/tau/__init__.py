from abc import ABC, abstractmethod
from datetime import timedelta, datetime

from datetimerange import DateTimeRange


class Event(ABC):
    @abstractmethod
    def on_raise(self) -> bool:
        pass


class Signal(Event):
    def __init__(self):
        self.current = None

    def on_raise(self):
        new_value = self.recompute()
        if new_value is None:
            return False
        else:
            self.current = new_value

    def is_valid(self) -> bool:
        return self.current is not None

    def get_value(self) -> object:
        return self.current

    @abstractmethod
    def recompute(self) -> object:
        pass


class MutableSignal(Signal):
    def set_value(self, value: object):
        self.current = value

    def recompute(self) -> object:
        return self.current


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
    def raise_signal(self, signal: MutableSignal, value: object):
        pass

    @abstractmethod
    def raise_signal_after(self, signal: MutableSignal, value: object, duration: timedelta):
        pass

    @abstractmethod
    def raise_signal_at(self, signal: MutableSignal, value: object, at_time: datetime):
        pass

    @abstractmethod
    def run(self, run_time: DateTimeRange = DateTimeRange()):
        pass

    @abstractmethod
    def shutdown(self):
        pass

