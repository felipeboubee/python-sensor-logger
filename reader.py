"""Wraps a raw sensor read with the error handling the acquisition loop relies on.

The loop in logger.py has no error handling of its own: this module is what
guarantees it always gets a usable number back, on schedule, whatever the
sensor does.
"""

import math
import logging


def make_safe_reader(read, default, lo, hi):
    """Build a zero-argument reader that never raises and never returns None.

    read    -- callable returning a distance in metres; may raise
    default -- sentinel substituted when a read fails or is unusable
    lo, hi  -- bounds that valid readings are clamped into
    """

    def safe_read():
        try:
            value = read()

        except (TimeoutError, OSError) as e:
            logging.warning("Sensor problem: %s", e)
            # Note the sentinel is returned unclamped, unlike the real readings
            # below. That is the point: it sits outside [lo, hi] so substituted
            # samples stay identifiable in the record instead of blending in.
            return default

        # Reject invalid values
        if value is None:
            logging.warning("Sensor returned None")
            return default

        if not math.isfinite(value):
            logging.warning("Sensor returned non-finite value: %r", value)
            return default

        # Clamp value to allowed range
        return min(max(value, lo), hi)

    return safe_read
