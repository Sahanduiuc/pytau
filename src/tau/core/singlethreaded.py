from abc import ABC
from datetime import datetime, timedelta

from datetimerange import DateTimeRange

from tau.core.api import Timeline, MutableSignal, Event


class SingleThreadedTimeline(Timeline):
    def bind(self, evt1: Event, evt2: Event):
        pass

    def unbind(self, evt1: Event, evt2: Event):
        pass

    def raise_event(self, evt: Event):
        pass

    def raise_event_after(self, evt: Event, duration: timedelta):
        pass

    def raise_event_at(self, evt: Event, at_time: datetime):
        pass

    def raise_signal(self, signal: MutableSignal, value: object):
        pass

    def raise_signal_after(self, signal: MutableSignal, value: object, duration: timedelta):
        pass

    def raise_signal_at(self, signal: MutableSignal, value: object, at_time: datetime):
        pass

    def run(self, run_time: DateTimeRange = DateTimeRange()):
        pass

    def shutdown(self):
        pass
