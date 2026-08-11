import random
# Define sensor class and add Gaussian error to read. Raise exception on 5% of calls
class Sensor:

    def __init__(self, true_d):
        self.true_d = true_d

    def read_sensor(self):
        if random.random() < 0.05:
            raise TimeoutError(f"Timeour error. Read took too long.")
        return self.true_d + random.gauss(0, 0.05)

    def safe_read(default):
        try:
            read_sensor(self)
        except (TimeoutError, OSError) as e:
            # log error

# Delete before finishing
sensor = Sensor(2.0)
print(sensor.read_sensor())


# For config file:
# true_d, default