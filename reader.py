import math
import logging


def make_safe_reader(read, default, lo, hi):

    def safe_read():
        try:
            value = read()

        except (TimeoutError, OSError) as e:
            logging.warning("Sensor problem: %s", e)
            return default

        # Reject invalid values
        if value is None:
            logging.warning("Sensor returned None")
            return default

        if not math.isfinite(value):
            logging.warning("Sensor returned non-finite value: %.2f", value)
            return default

        # Clamp value to allowed range
        return min(max(value, lo), hi)

    return safe_read






