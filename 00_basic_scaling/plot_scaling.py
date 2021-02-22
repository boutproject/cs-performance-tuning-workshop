#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np


def get_time_from_log_file(fname):
    """Return run time from BOUT log file output by searching for the line 'Run time :'. This assumes there is only one run per log file."""

    with open(fname, "r") as f:
        for line_number, line in enumerate(f):
            if line.startswith("Run time :"):
                mins = float(line.split()[3])
                secs = float(line.split()[5])
                time = 60.0 * mins + secs
                return time


def read_run_times(nprocs, directory):
    """ Loop over files to read run times """

    times = []
    for p in nprocs:
        times.append(get_time_from_log_file(directory+"/test_run_" + str(p) + ".log"))

    return times


def get_scaling_efficiency(nprocs, times):
    """ Calculate the scaling efficiency """

    return 100.0 * times[0] * nprocs[0] / (times * nprocs)


def plot_strong_scaling(runsets, fname="strong_scaling.png"):
    """ Plot the strong scaling """

    nprocs_union = []
    for r in runsets:

        ideal = r.times[0] * r.nprocs[0] / r.nprocs

        plt.loglog(r.nprocs, r.times, "o-", label=r.name)
        plt.loglog(r.nprocs, ideal, "k-", lw=0.5)
        nprocs_union = np.union1d(nprocs_union, r.nprocs).astype(int)

    ax = plt.gca()
    plt.minorticks_off()
    ax.set_xticks(nprocs_union)
    ax.set_xticklabels(nprocs_union)
    tvec = [100, 200, 300, 400, 500, 600, 700, 1000, 1400, 1800]
    ax.set_yticks(tvec)
    ax.set_yticklabels(tvec)
    plt.ylim(100, 1800)
    plt.legend()
    plt.grid()
    plt.xlabel("MPI ranks")
    plt.ylabel("Run time / secs")
    plt.savefig(fname)
    plt.clf()


def plot_scaling_efficiency(runsets, fname="scaling_efficiency.png"):
    """ Plot the scaling efficiency """

    nprocs_union = []
    for r in runsets:
        plt.semilogx(r.nprocs, r.efficiency, "o-", label=r.name)
        nprocs_union = np.union1d(nprocs_union, r.nprocs).astype(int)

    ax = plt.gca()
    plt.minorticks_off()
    ax.set_xticks(nprocs_union)
    ax.set_xticklabels(nprocs_union)
    plt.legend()
    plt.grid()
    plt.xlabel("MPI ranks")
    plt.ylabel("Scaling efficiency versus 2 cores (%)")
    plt.savefig(fname)
    plt.clf()

class RunSet():
    """ Class holding data for a set of runs """
    def __init__(self, nprocs, times, efficiency, name):
        self.nprocs = nprocs
        self.times = times
        self.efficiency = efficiency
        self.name = name

def main():

    runsets = []

    # gnu-openmpi
    nprocs = np.array([2, 4, 8, 16, 32, 64, 128])
    times = read_run_times(nprocs, "gcc-openmpi")
    efficiency = get_scaling_efficiency(nprocs, times)
    runsets.append(RunSet(nprocs,times,efficiency,"gcc-openmpi"))

    # intel-intelmpi
    nprocs = np.array([2, 4, 8, 16, 32, 64])
    times = read_run_times(nprocs, "intel-intelmpi")
    efficiency = get_scaling_efficiency(nprocs, times)
    runsets.append(RunSet(nprocs,times,efficiency,"intel-intelmpi"))

    plot_strong_scaling(runsets)
    plot_scaling_efficiency(runsets)


if __name__ == "__main__":
    main()
