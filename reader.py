import math
import logging


# Configure logging once
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s %(message)s",
    filename="logger.log",
)

log = logging.getLogger("sensor_logger")


def make_safe_reader(read, default, lo, hi):

    def safe_read():
        try:
            value = read()

        except (TimeoutError, OSError) as e:
            log.warning(f"Sensor problem: {e}")
            return default

        # Reject invalid values
        if value is None:
            log.warning("Sensor returned None")
            return default

        if not math.isfinite(value):
            log.warning(f"Sensor returned non-finite value: {value}")
            return default

        # Clamp value to allowed range
        return min(max(value, lo), hi)

    return safe_read

# TODO: add to config:
# default, lo, hi




