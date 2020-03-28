from tau.event import Lambda
from tau.signal import OneShot
from tau.testing import TestSchedulerContextManager

with TestSchedulerContextManager() as scheduler:
    signal = OneShot(scheduler, ["world"])
    Lambda(scheduler.get_network(), signal, lambda x: print(f"Hello, {x[0].get_value()}!"))
