from datetime import timedelta

from tau.event import Do
from tau.signal import Interval, BufferWithCount, BufferWithTime

from tau.testing import TestSchedulerContextManager

with TestSchedulerContextManager(shutdown_delay=30) as scheduler:
    network = scheduler.get_network()
    values = Interval(scheduler)
    Do(network, values, lambda: print(f"input values: {values.get_value()}"))

    buffer1 = BufferWithCount(network, values, count=2)
    Do(network, buffer1, lambda: print(f"buffer1 values: {buffer1.get_value()}"))

    buffer2 = BufferWithTime(network, values, timedelta(seconds=5), scheduler=scheduler.get_native_scheduler())
    Do(network, buffer2, lambda: print(f"buffer2 values: {buffer2.get_value()}"))



