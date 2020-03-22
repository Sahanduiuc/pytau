from math import sqrt

from tau.core.api import Signal, Timeline
from tau.event import Function


class RunningSum(Function):
    """
    Real-time calculation of a running sum of a numeric event.
    """
    def __init__(self, timeline: Timeline, values: Signal):
        super().__init__(timeline, [values])
        self.values = values
        self.sum = 0

    def _call(self):
        if self.values.is_valid():
            self._update(self.get_value() + self.values.get_value())


class Mean(Function):
    """
    Real-time calculation of the mean of a numeric event.
    """
    def __init__(self, timeline: Timeline, values: Signal):
        super().__init__(timeline, [values])
        self.values = values
        self.count = 0

    def _call(self):
        if self.values.is_valid():
            self.count = self.count + 1
            prev_mean = self.get_value()
            self._update(prev_mean + (self.values.get_value() - prev_mean) / self.count)


class Stddev(Function):
    """
    Real-time calculation of the standard deviation of a numeric event.
    """
    def __init__(self, timeline: Timeline, values: Signal):
        super().__init__(timeline, [values])
        self.values = values
        self.count = 0.0
        self.mean = 0.0

    def _call(self):
        if self.values.is_valid():
            self.count = self.count + 1
            prev_mean = self.mean
            next_val = self.values.get_value()
            self.mean = self.mean + (next_val - self.mean) / self.count
            prev_stddev = self.get_value()
            variance = prev_stddev + (next_val - self.mean) * (next_val - prev_mean)
            self._update(sqrt(variance))


class ExponentialMovingAverage(Function):
    """
    Real-time calculation of EMA (Exponential Moving Average).
    """
    def __init__(self, timeline: Timeline, values: Signal):
        super().__init__(timeline, [values])
        self.values = values
        self.count = 0.0

    def _call(self):
        if self.values.is_valid():
            self.count = self.count + 1
            prev_ema = self.get_value()
            next_val = self.values.get_value()
            self._update((next_val - prev_ema) * (2 / (self.count + 1)) + prev_ema)


class WeightedMovingAverage(Function):
    """
    Real-time calculation of WMA (Weighted Moving Average).
    """
    def __init__(self, timeline: Timeline, values: Signal, weighting_factor: float):
        super().__init__(timeline, [values])
        self.values = values
        self.weighting_factor = weighting_factor
        self.prev_val = 0.0

    def _call(self):
        if self.values.is_valid():
            next_val = self.values.get_value()
            self._update((next_val * self.weighting_factor + (self.prev_val * (self.weighting_factor-1))))
            self.prev_val = next_val
