from datetime import timedelta

from apscheduler.schedulers.blocking import BlockingScheduler

from tau.core import NetworkScheduler
from tau.trigger import DelayTrigger


class TestSchedulerContextManager:
    def __init__(self, delay: int = 1):
        self.scheduler = BlockingScheduler()
        self.delay = delay

    def __enter__(self):
        return NetworkScheduler(self.scheduler)

    def __exit__(self, *args):
        # start and then shut down scheduler after one second
        self.scheduler.add_job(lambda: self.scheduler.shutdown(wait=False), DelayTrigger(timedelta(seconds=self.delay)))
        self.scheduler.start()
