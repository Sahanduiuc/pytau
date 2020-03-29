from tau.event import Lambda
from tau.signal import From
from tau.testing import TestSchedulerContextManager

with TestSchedulerContextManager() as scheduler:
    signal = From(scheduler, ["world"])
    Lambda(scheduler.get_network(), signal, lambda x: print(f"Hello, {x[0].get_value()}!"))
