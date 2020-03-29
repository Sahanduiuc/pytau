from tau.event import Do
from tau.math import RunningSum
from tau.signal import From

from tau.testing import TestSchedulerContextManager

with TestSchedulerContextManager() as scheduler:
    network = scheduler.get_network()
    values = From(scheduler, [0.0, 3.2, 2.1, 2.9, 8.3, 5.7])
    total = RunningSum(network, values)
    Do(network, total, lambda x: print(f'{x:.2f}'))
