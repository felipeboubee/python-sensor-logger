"""CSV persistence for acquisition runs."""

import csv


def write_rows(path, rows):
    """Write (time, distance) rows to `path`, with a header."""
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "distance"])
        writer.writerows(rows)


def load_rows(path):
    """Read `path` back into a list of (time, distance) float tuples."""
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader)                                        # discard header
        return [(float(t), float(d)) for t, d in reader]
