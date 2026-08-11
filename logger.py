import time

def run(duration, hz):

    dt = 1.0 / hz
    next_t = time.perf_counter()

    while True:

        next_t += dt 
        sleep = next_t - time.perf_counter()
        if sleep > 0:
            time.sleep(sleep)


print(run(5.0, 20))


# For config file:
# duration, hz