"""Fixed-rate acquisition loop."""

import time


def run(read, duration, hz):
    """Sample `read` at `hz` for `duration` seconds.

    Returns a list of (elapsed_seconds, value) tuples. `read` is expected to
    handle its own errors — see reader.make_safe_reader.
    """

    dt = 1.0 / hz
    t0 = next_t = time.perf_counter()
    rows = []

    while time.perf_counter() - t0 < duration:

        # The timestamp marks when the read was issued, not when the value
        # arrived. Fine while reads are fast relative to dt; worth revisiting
        # for a sensor with a long, variable response time.
        rows.append((round(time.perf_counter() - t0, 3), read()))

        # Advance an absolute deadline instead of sleeping a flat dt. Time
        # spent inside read() is absorbed by a correspondingly shorter sleep
        # rather than accumulating as drift over the run.
        #
        # Assumes a read costs well under dt. If one overruns, `sleep` goes
        # negative and the loop simply stays behind by that much — it does not
        # skip samples to catch up, which keeps the record contiguous at the
        # cost of a small permanent offset.
        next_t += dt
        sleep = next_t - time.perf_counter()
        if sleep > 0:
            time.sleep(sleep)

    return rows
