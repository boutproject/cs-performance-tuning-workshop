#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np


def get_time_from_log_file(fname):
    """Return run time from BOUT log file output by searching for the line 'Run time :'. This assumes there is only one run per log file."""

    with open(fname, "r") as f:
        for line_number, line in enumerate(f):
            if line.startswith("Run time :"):
                if " h " in line:
                    hrs = float(line.split()[3])
                    mins = float(line.split()[5])
                    secs = float(line.split()[7])
                else:
                    hrs = 0.0
                    mins = float(line.split()[3])
                    secs = float(line.split()[5])
                time = 3600.0 * hrs + 60.0 * mins + secs
                return time


def read_run_times(nprocs):
    """ Loop over files to read run times """

    times = []
    for p in nprocs:
        times.append(get_time_from_log_file("test_run_" + str(p) + ".log"))

    return times


def get_scaling_efficiency(nprocs, times):
    """ Calculate the scaling efficiency """

    return 100.0 * times[0] * nprocs[0] / (times * nprocs)


def plot_strong_scaling(nprocs, times, fname="strong_scaling.png"):
    """ Plot the strong scaling """

    ideal = times[0] * nprocs[0] / nprocs

    plt.loglog(nprocs, times, "o-")
    plt.loglog(nprocs, ideal, "k-", lw=0.5)

    ax = plt.gca()
    plt.minorticks_off()
    ax.set_xticks(nprocs)
    ax.set_xticklabels(nprocs)
    tvec = [70, 100, 200, 300, 400, 500, 600, 700, 1000, 1400, 1800]
    ax.set_yticks(tvec)
    ax.set_yticklabels(tvec)
    plt.ylim(70, 1800)
    plt.grid()
    plt.xlabel("MPI ranks")
    plt.ylabel("Run time / secs")
    plt.savefig(fname)
    plt.clf()


def plot_scaling_efficiency(nprocs, efficiency, fname="scaling_efficiency.png"):
    """ Plot the scaling efficiency """

    plt.semilogx(nprocs, efficiency, "o-")

    ax = plt.gca()
    plt.minorticks_off()
    ax.set_xticks(nprocs)
    ax.set_xticklabels(nprocs)
    plt.grid()
    plt.xlabel("MPI ranks")
    plt.ylabel("Scaling efficiency versus 2 cores (%)")
    plt.savefig(fname)
    plt.clf()


def main():

    nprocs = np.array([1, 2, 4, 8, 16, 32, 48])

    times = read_run_times(nprocs)
    efficiency = get_scaling_efficiency(nprocs, times)

    plot_strong_scaling(nprocs, times)
    plot_scaling_efficiency(nprocs, efficiency)

    nprocs = np.array([1, 2, 4, 8, 16, 32, 48, 96, 192])

    times = read_run_times(nprocs)
    efficiency = get_scaling_efficiency(nprocs, times)

    plot_strong_scaling(nprocs, times, fname="strong_scaling_with_4_nodes.png")
    plot_scaling_efficiency(
        nprocs, efficiency, fname="scaling_efficiency_with_4_nodes.png"
    )


if __name__ == "__main__":
    main()
