from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.date import DateTrigger

from tau.core.api import Event, Network, NetworkScheduler


class HelloWorld(Event):
    def on_activate(self):
        print("Hello, world!")
        return False


network = Network()

scheduler = BlockingScheduler()
network_scheduler = NetworkScheduler(scheduler, network)
network_scheduler.schedule_event(HelloWorld(), DateTrigger())
scheduler.start()

