import csv

# Writing data in csv format
def write_rows(path, rows):
    with open(path, "w", newline="") as f:          # using with open to close the file automatically at block end
        writer = csv.writer(f)
        writer.writerow(["time", "distance"])       # header
        writer.writerows(rows)                      # data

# Loading csv data
def load_rows(path):
    with open(path, newline="") as f:
        reader = csv.reader(f)
        next(reader)                                # skip the header

        return [(float(t), float(d)) for t, d in reader]    # parse strings to numbers
        
