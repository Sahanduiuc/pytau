from threading import Timer

from apscheduler.schedulers.background import BackgroundScheduler

from tau.core import NetworkScheduler


class TestSchedulerContextManager:
    def __init__(self, scheduler=BackgroundScheduler(daemon=False), shutdown_delay=1):
        self.scheduler = scheduler
        self.shutdown_delay = shutdown_delay

    def __enter__(self):
        return NetworkScheduler(self.scheduler)

    def __exit__(self, *args):
        self.scheduler.start()

        # use a simple timer to schedule the scheduler shutdown
        t = Timer(self.shutdown_delay, lambda: self.scheduler.shutdown(wait=False))
        t.start()
