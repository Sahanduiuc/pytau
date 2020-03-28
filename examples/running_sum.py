from tau.event import ForEach
from tau.math import RunningSum
from tau.signal import OneShot

from tau.testing import TestSchedulerContextManager

with TestSchedulerContextManager() as scheduler:
    network = scheduler.get_network()
    values = OneShot(scheduler, [0.0, 3.2, 2.1, 2.9, 8.3, 5.7])
    total = RunningSum(network, values)
    ForEach(network, total, lambda x: print(f'{x:.2f}'))
