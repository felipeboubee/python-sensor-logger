import matplotlib.pyplot as plt

def plot_run(rows, path, default):

    t = [r[0] for r in rows]                # extract time from rows
    d = [r[1] for r in rows]                # extract distance from rows
    plt.plot(t, d)                          # plot time and distances

    bad = [(ti, di) for ti, di in rows if di == default]                    # mark the substituted samples
    if bad:
        plt.scatter([b[0] for b in bad], [b[1] for b in bad], marker="x")   # create scatter plot of bad values

    plt.xlabel("time (s)"); plt.ylabel("distance (m)")
    plt.savefig(path)


