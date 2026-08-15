import logging
import config
from sensor import Sensor
from reader import make_safe_reader
from logger import run
from recorder import write_rows, load_rows
from plotting import plot_run

sensor = Sensor(config.TRUE_D)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    rows = run(read=make_safe_reader(sensor.read_sensor, default=config.DEFAULT, lo=config.LO, hi=config.HI), duration=config.DURATION, hz=config.HZ)
    write_rows("sensor_log.csv", rows)
    plot_run(load_rows("sensor_log.csv"), "sensor_log.png", default=config.DEFAULT)