#!/usr/bin/python3

import argparse
import format_plot
import Run

import pylab
import matplotlib
import matplotlib.pyplot

matplotlib.use(
    "Agg"
)  # to avoid some DISPLAY issues on compute nodes, we do not need display anyways
from matplotlib.pylab import *
import matplotlib.colors as colors  # palette and co.


class Plot_Defaults:
    def __init__(self):
        self.xlog = True
        self.ylog = True
        self.loglog = True
        self.xlabel = ""
        self.ylabel = ""

def plot_runset(df,labelstr,colorstr):

    ncol = len(df.columns)-11

    for nc in range(ncol):
        df.plot(
                    x="Local grid",
                    y=str(nc+1),
                    ax=plt.gca(),
                    marker='_',
                    lw=0,
                    color=colorstr,
                    #label="",
                    legend=False
                )

    ax = df.plot(
                x="Local grid",
                y="mean",
                ax=plt.gca(),
                marker='.',
                lw=1,
                color=colorstr,
                label=labelstr,
            )
    return ax

def main():

    gcc7 = Run.Run('gcc_7.3/slurm-2989705.out')
    gcc7.append('gcc_7.3/slurm-2989716.out')
    gcc7.append('gcc_7.3/slurm-2989748.out')
    gcc7.calculate_statistics()

    gcc10 = Run.Run('gcc_10.2/slurm-2990366.out')
    gcc10.append('gcc_10.2/slurm-2990371.out')
    gcc10.append('gcc_10.2/slurm-2990378.out')
    gcc10.calculate_statistics()

    intel18 = Run.Run('intel_18/slurm-2991164.out')
    intel18.calculate_statistics()

    parser = argparse.ArgumentParser(
        description="Plot the growth rate against the timestep."
    )

    #parser.add_argument("file", help="Name of file(s) in the GS2 timing format", nargs="+")
    parser.add_argument("--xlog", help="Use logscale on x axis", action="store_true")
    parser.add_argument("--ylog", help="Use logscale on y axis", action="store_true")
    parser.add_argument(
        "--loglog", help="Use logscale on both x and y axis", action="store_true"
    )
    parser.add_argument(
        "--ideal", help="Use logscale on both x and y axis", action="store_true"
    )
    parser.add_argument("--xlabel", help="x axis label")
    parser.add_argument("--ylabel", help="y axis label")
    parser.add_argument("--xlim", help="x axis limits, two numbers, comma-separated")
    parser.add_argument("--ylim", help="y axis limits, two numbers, comma-separated")
    parser.add_argument("--markers", help="Unspaced list of markers to use for each line")
    parser.add_argument("--colours", help="Unspaced list of colours to use for each line")
    parser.add_argument("--grid", help="Include grid lines", action="store_true")
    parser.add_argument(
        "--legend", help='Legend entries in the format: "legend1,legend2,multi-word legend3'
    )
    parser.add_argument(
        "--legend_fontsize", help="Fontsize for the legend", type=int, default=10
    )
    parser.add_argument("--title", help="Plot title")
    parser.add_argument("--yvar", help="Dependent variable to plot, default time")
    parser.add_argument("--xticks", help="Space separated list of xticks to use")
    parser.add_argument("--yticks", help="Space separated list of yticks to use")
    parser.add_argument("--output", help="Output filename")

    args = parser.parse_args()



    # Set this graph's defaults
    defaults = Plot_Defaults()
    defaults.ylabel = "time"
    defaults.xlabel = "local grid size"
    defaults.loglog = True

    ax = plot_runset(gcc7.cloop_weak,'gcc 7.3 C loop','b')
    ax = plot_runset(gcc7.boutfor_weak,'gcc 7.3 BOUT for','g')

    ax = plot_runset(gcc10.cloop_weak,'gcc 10.2 C loop','r')
    ax = plot_runset(gcc10.boutfor_weak,'gcc 10.2 BOUT for','Orange')

    ax = plot_runset(intel18.cloop_weak,'intel 18 C loop','k')
    ax = plot_runset(intel18.boutfor_weak,'intel 18 BOUT for','m')

###    if leg:
###        plt.legend(loc=0, fontsize=args.legend_fontsize)

    if args.title:
        plt.title(args.title)

    if args.grid:
        plt.grid()

    format_plot.format_plot(gca(), args, defaults)

    if args.xticks:
        plt.gca().tick_params(axis="x", which="minor", bottom=False)
        xt = [str(i) for i in args.xticks.split()]
        a = []
        b = []
        for i in xt:
            a.append(float(i))
            b.append(str(i))
        plt.xticks(a, b)

    if args.yticks:
        yt = [str(i) for i in args.yticks.split()]
        a = []
        b = []
        for i in yt:
            a.append(float(i))
            b.append(str(i))
        plt.yticks(a, b)

    if args.output:
        plt.savefig(args.output)
    else:
        plt.savefig("time_vs_nproc.pdf")
        #plt.savefig(args.yvar + "_vs_nproc.pdf")

    plt.clf()
    


if __name__ == "__main__":
    main()
