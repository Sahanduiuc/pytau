from tau.core.api import MutableSignal
from tau.core.singlethreaded import SingleThreadedTimeline
from tau.event.statistics import RunningSum, Mean, Stddev

timeline = SingleThreadedTimeline()
timeline.run()

values = MutableSignal()
total = RunningSum(timeline, values)
avg = Mean(timeline, values)
stddev = Stddev(timeline, values)


timeline.raise_signal(values, 0.0)
timeline.raise_signal(values, 3.2)
timeline.raise_signal(values, 2.1)
timeline.raise_signal(values, 2.9)
timeline.raise_signal(values, 8.3)
timeline.raise_signal(values, 5.6)
