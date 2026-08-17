"""Entry point: wire the modules together and perform one acquisition run."""

import logging

import config
from sensor import Sensor
from reader import make_safe_reader
from logger import run
from recorder import write_rows, load_rows
from plotting import plot_run

CSV_PATH = "results/sensor_log.csv"
# One PNG per theme, so the same run can be embedded on a light or a dark page.
PNG_PATHS = {"light": "results/sensor_log.png",
             "dark": "results/sensor_log_dark.png"}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")

    sensor = Sensor(config.TRUE_D)

    # All error handling lives in the wrapped reader, so the acquisition loop
    # below can stay a pure timing concern.
    safe_read = make_safe_reader(sensor.read_sensor,
                                 default=config.DEFAULT,
                                 lo=config.LO,
                                 hi=config.HI)

    rows = run(read=safe_read, duration=config.DURATION, hz=config.HZ)
    write_rows(CSV_PATH, rows)

    # Plot from the file rather than from `rows`, so every run also exercises
    # the CSV round-trip that anyone reusing this data depends on. Both themes
    # are drawn from that single read, so they can never disagree.
    logged = load_rows(CSV_PATH)
    for theme, png_path in PNG_PATHS.items():
        plot_run(logged, png_path, default=config.DEFAULT, theme=theme)
