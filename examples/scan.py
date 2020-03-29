from tau.event import Do
from tau.signal import Interval, Scan

from tau.testing import TestSchedulerContextManager

with TestSchedulerContextManager(shutdown_delay=30) as scheduler:
    network = scheduler.get_network()
    values = Interval(scheduler)
    accumulator = Scan(network, values)
    Do(network, accumulator, lambda: print(f"{accumulator.get_value()}"))




