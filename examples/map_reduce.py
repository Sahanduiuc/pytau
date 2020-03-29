from tau.event import Do
from tau.signal import From, Map, Scan

from tau.testing import TestSchedulerContextManager

with TestSchedulerContextManager() as scheduler:
    network = scheduler.get_network()
    values = From(scheduler, [0.0, 3.2, 2.1, 2.9, 8.3, 5.7])
    mapper = Map(network, values, lambda x: round(x))
    accumulator = Scan(network, mapper)
    Do(network, accumulator, lambda: print(f"{accumulator.get_value()}"))




