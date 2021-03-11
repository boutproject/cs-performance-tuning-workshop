import matplotlib.pyplot as plt


def format_plot(ax, args, defaults):
    """Common routine for formatting plot. Apply given defaults, then apply
    user-provided overrides.
    """

    if args.xlog or args.loglog:
        ax.set_xscale("log")
    if args.ylog or args.loglog:
        ax.set_yscale("log")

    plt.xlabel(defaults.xlabel)
    if args.xlabel:
        plt.xlabel(args.xlabel)

    plt.ylabel(defaults.ylabel)
    if args.ylabel:
        plt.ylabel(args.ylabel)

    if args.xlim:
        xmin, xmax = args.xlim.split(",")
        plt.xlim(float(xmin), float(xmax))
    if args.ylim:
        ymin, ymax = args.ylim.split(",")
        plt.ylim(float(ymin), float(ymax))
