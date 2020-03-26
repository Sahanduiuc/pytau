from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.date import DateTrigger

from tau.core.api import MutableSignal, Network, NetworkScheduler
from tau.event import ForEach
from tau.event.statistics import RunningSum

network = Network()
values = MutableSignal()
total = RunningSum(network, values)

ForEach(network, total, lambda x: print(f'{x:.2f}'))

scheduler = BlockingScheduler()
network_scheduler = NetworkScheduler(scheduler, network)

network_scheduler.schedule_update(values, 0.0, DateTrigger())
network_scheduler.schedule_update(values, 3.2, DateTrigger())
network_scheduler.schedule_update(values, 2.1, DateTrigger())
network_scheduler.schedule_update(values, 2.9, DateTrigger())
network_scheduler.schedule_update(values, 8.3, DateTrigger())
network_scheduler.schedule_update(values, 5.7, DateTrigger())

scheduler.start()

