import time

def run(read, duration, hz):

    dt = 1.0 / hz
    t0 = next_t = time.perf_counter()
    rows = []

    while time.perf_counter() - t0 < duration:

        rows.append((round(time.perf_counter() - t0, 3), read()))
        next_t += dt 
        sleep = next_t - time.perf_counter()
        if sleep > 0:
            time.sleep(sleep)

    return rows

        

# TODO: delete this after writing main and config
print(run(lambda: 0.0, 5.0, 20))


# TODO: Add to config file:
# duration, hz
