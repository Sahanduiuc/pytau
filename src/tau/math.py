import sys
from math import sqrt

from tau.core import Signal, Network
from tau.signal import Function


class RunningSum(Function):
    """
    Real-time calculation of a running sum of a numeric signal.
    """
    def __init__(self, network: Network, values: Signal):
        super().__init__(network, [values])
        self._update(0.0)

    def _call(self):
        if self.parameters[0].is_valid():
            self._update(self.get_value() + self.parameters[0].get_value())


class Min(Function):
    def __init__(self, network: Network, values: Signal):
        super().__init__(network, [values])
        self._update(sys.maxsize)

    def _call(self):
        if self.parameters[0].is_valid():
            self._update(min(self.get_value(), self.parameters[0].get_value()))


class Max(Function):
    def __init__(self, network: Network, values: Signal):
        super().__init__(network, [values])
        self._update(-sys.maxsize - 1)

    def _call(self):
        if self.parameters[0].is_valid():
            self._update(max(self.get_value(), self.parameters[0].get_value()))


class Mean(Function):
    """
    Real-time calculation of the mean of a numeric signal.
    """
    def __init__(self, network: Network, values: Signal):
        super().__init__(network, [values])
        self.count = 0
        self._update(0.0)

    def _call(self):
        if self.parameters[0].is_valid():
            self.count = self.count + 1
            prev_mean = self.get_value()
            self._update(prev_mean + (self.parameters[0].get_value() - prev_mean) / self.count)


class Stddev(Function):
    """
    Real-time calculation of the standard deviation of a numeric signal.
    """
    def __init__(self, network: Network, values: Signal):
        super().__init__(network, [values])
        self.count = 0.0
        self.mean = 0.0
        self._update(0.0)

    def _call(self):
        if self.parameters[0].is_valid():
            self.count = self.count + 1
            prev_mean = self.mean
            next_val = self.parameters[0].get_value()
            self.mean = self.mean + (next_val - self.mean) / self.count
            prev_stddev = self.get_value()
            variance = prev_stddev + (next_val - self.mean) * (next_val - prev_mean)
            self._update(sqrt(variance))


class ExponentialMovingAverage(Function):
    """
    Real-time calculation of EMA (Exponential Moving Average) of a numeric signal.
    """
    def __init__(self, network: Network, values: Signal):
        super().__init__(network, [values])
        self.values = values
        self.count = 0.0
        self._update(0.0)

    def _call(self):
        if self.values.is_valid():
            self.count = self.count + 1
            prev_ema = self.get_value()
            next_val = self.values.get_value()
            self._update((next_val - prev_ema) * (2 / (self.count + 1)) + prev_ema)


class WeightedMovingAverage(Function):
    """
    Real-time calculation of WMA (Weighted Moving Average) of a numeric signal.
    """
    def __init__(self, network: Network, values: Signal, weighting_factor: float):
        super().__init__(network, [values])
        self.values = values
        self.weighting_factor = weighting_factor
        self.prev_val = 0.0
        self._update(0.0)

    def _call(self):
        if self.values.is_valid():
            next_val = self.values.get_value()
            self._update((next_val * self.weighting_factor + (self.prev_val * (self.weighting_factor-1))))
            self.prev_val = next_val
