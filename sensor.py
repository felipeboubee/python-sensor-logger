"""Simulated rangefinder, so the acquisition pipeline runs without hardware.

Models the two behaviours the logger has to cope with: additive measurement
noise on every reading, and reads that fail outright.
"""

import random

import config

# Fraction of reads that raise instead of returning a value. Stands in for a
# flaky bus, a loose connector, or a sensor that misses its response window.
FAILURE_RATE = 0.05


class Sensor:

    def __init__(self, true_d):
        self.true_d = true_d

    def read_sensor(self):
        """Return one distance reading in metres, or raise TimeoutError."""
        if random.random() < FAILURE_RATE:
            raise TimeoutError("sensor read exceeded timeout")
        return self.true_d + random.gauss(mu=config.MU, sigma=config.SIGMA)
