from datetime import timedelta

from apscheduler.triggers.base import BaseTrigger


class ImmediateTrigger(BaseTrigger):
    def __init__(self):
        self.scheduled = False

    def get_next_fire_time(self, previous_fire_time, now):
        if self.scheduled:
            return None
        self.scheduled = True
        return now


class DelayTrigger(BaseTrigger):
    def __init__(self, delay: timedelta):
        self.scheduled = False
        self.delay = delay

    def get_next_fire_time(self, previous_fire_time, now):
        if self.scheduled:
            return None
        self.scheduled = True
        return now + self.delay
