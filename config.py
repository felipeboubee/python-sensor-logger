"""Run parameters for the sensor logger.

All distances are in metres, all times in seconds.
"""

# --- Acquisition ---------------------------------------------------------
DURATION = 5.0      # length of one run
HZ = 20             # target sample rate, i.e. a 50 ms period

# --- Validation ----------------------------------------------------------
LO = 0.0            # smallest physically plausible reading; lower values clamp up
HI = 10.0           # sensor's rated maximum range; higher values clamp down

# Sentinel written when a read fails or returns something unusable. Chosen
# outside [LO, HI] and deliberately never clamped, so a substituted sample can
# always be recovered from the CSV alone with `distance == DEFAULT` and can
# never be confused with a real measurement.
DEFAULT = 99.0

# --- Simulated sensor (sensor.py) ----------------------------------------
# Stands in for hardware so the whole pipeline runs anywhere.
TRUE_D = 2.0        # fixed distance to the simulated target
MU = 0.0            # mean of the additive noise; non-zero models a calibration bias
SIGMA = 1.0         # standard deviation of the additive noise
