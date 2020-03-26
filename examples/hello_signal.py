from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.date import DateTrigger

from tau.core.api import Event, Signal, MutableSignal, Network, NetworkScheduler


class SayHello(Event):
    def __init__(self, name: Signal):
        super().__init__()
        self.name = name

    def on_activate(self):
        print(f"Hello, {self.name.get_value()}!")


network = Network()
signal = MutableSignal()
network.connect(signal, SayHello(signal))

scheduler = BlockingScheduler()
network_scheduler = NetworkScheduler(scheduler, network)
network_scheduler.schedule_update(signal, "world", DateTrigger())
scheduler.start()
