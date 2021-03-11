import numpy
import pandas as pd
import scaling_parser

class Run:
    """
    Class to hold information about a series of runs
    """

    def __init__(self, name):
        self.name = name

        # Put all data for weak run into pandas dataframe
        lines, weak, _, lines_strong, strong, _ = scaling_parser.read_file(name)
        data_weak = pd.DataFrame.from_dict(weak)
        data_weak.rename(columns = lines, inplace=True)

        # Make separate data frames for C Loop and BOUT_FOR
        # This allows us to use columns for repeat timings
        self.cloop_weak = data_weak[['Nprocs','Nthreads','Num_loops','Local grid','Nx (global)','Ny (global)','Nz (global)','C loop']].copy()
        self.cloop_weak.rename(columns = {'C loop' : '1'}, inplace=True)

        self.boutfor_weak = data_weak[['Nprocs','Nthreads','Num_loops','Local grid','Nx (global)','Ny (global)','Nz (global)','Region (serial)']].copy()
        self.boutfor_weak.rename(columns = {'Region (serial)' : '1'}, inplace=True)

        data_strong = pd.DataFrame.from_dict(strong)
        data_strong.rename(columns = lines_strong, inplace=True)

        # Make separate data frames for C Loop and BOUT_FOR
        # This allows us to use columns for repeat timings
        self.cloop_strong = data_strong[['Nprocs','Nthreads','Num_loops','Local grid','Nx (global)','Ny (global)','Nz (global)','C loop']].copy()
        self.cloop_strong.rename(columns = {'C loop' : '1'}, inplace=True)

        self.boutfor_strong = data_strong[['Nprocs','Nthreads','Num_loops','Local grid','Nx (global)','Ny (global)','Nz (global)','Region (serial)']].copy()
        self.boutfor_strong.rename(columns = {'Region (serial)' : '1'}, inplace=True)

    def append(self, name):
        lines, weak, _, lines_strong, strong, _ = scaling_parser.read_file(name)
        data_weak = pd.DataFrame.from_dict(weak)
        data_weak.rename(columns = lines, inplace=True)

        print(data_weak)

        self.cloop_weak = pd.concat([self.cloop_weak, data_weak['C loop']], axis=1)
        runcount = len(self.cloop_weak.columns) - 7
        self.cloop_weak.rename(columns = {'C loop' : str(runcount)}, inplace=True)

        self.boutfor_weak = pd.concat([self.boutfor_weak, data_weak['Region (serial)']], axis=1)
        runcount = len(self.boutfor_weak.columns) - 7
        self.boutfor_weak.rename(columns = {'Region (serial)' : str(runcount)}, inplace=True)

        print(self.cloop_weak)
        print(self.boutfor_weak)

        data_strong = pd.DataFrame.from_dict(strong)
        data_strong.rename(columns = lines, inplace=True)

        print(data_strong)

        self.cloop_strong = pd.concat([self.cloop_strong, data_strong['C loop']], axis=1)
        runcount = len(self.cloop_strong.columns) - 7
        self.cloop_strong.rename(columns = {'C loop' : str(runcount)}, inplace=True)

        self.boutfor_strong = pd.concat([self.boutfor_strong, data_strong['Region (serial)']], axis=1)
        runcount = len(self.boutfor_strong.columns) - 7
        self.boutfor_strong.rename(columns = {'Region (serial)' : str(runcount)}, inplace=True)

        print(self.cloop_strong)
        print(self.boutfor_strong)

    def calculate_statistics(self):

        calculate_dataframe_averages(self.cloop_weak)
        calculate_dataframe_averages(self.cloop_strong)
        calculate_dataframe_averages(self.boutfor_weak)
        calculate_dataframe_averages(self.boutfor_strong)

    def someotherfunction(self):
        self.stats = pd.DataFrame(
            columns=[
                "nprocs",
                "means",
                "std",
                "ci_up",
                "ci_down",
            ]
        )

        nprocs_u = self.data.nprocs.unique()
        for i, np in enumerate(nprocs_u):
            d = self.data[(self.data.nprocs == np)]
            mean = d.times.mean()
            std = d.times.std()
            minval = d.times.min()
            maxval = d.times.max()

            # Get coefficient for ideal line
            if i == 0:
                ideal_coef = np * mean

            self.stats = self.stats.append(
                {
                    "nprocs": np,
                    "means": mean,
                    "minval": minval,
                    "maxval": maxval,
                    "std": std,
                    "coefficient of variation": std / mean,
                    "ci_up": mean + 1.96 * std,
                    "ci_down": mean - 1.96 * std,
                    "ideal": ideal_coef / np,
                },
                ignore_index=True,
            )

class NormalizedRun:
    """ Class where the data of one run is normalized with respect to a second run. Typically, this will be one mean run time normalized to another run time, but could also include manipulations of confidence intervals, etc.
    """
    def __init__(self, r, r0):
        """ r is the run to be normalized, r0 the normalizing run """

        self.stats = pd.DataFrame()

        nprocs = r.stats.nprocs
        nprocs0 = r0.stats.nprocs
        nps = numpy.sort(list(set(nprocs) & set(nprocs0)))
        for i, np in enumerate(nps):
            run_mean = float(r.stats[r.stats.nprocs==np].means)
            run0_mean = float(r0.stats[r0.stats.nprocs==np].means)

            run_min = float(r.stats[r.stats.nprocs==np].minval)
            run0_min = float(r0.stats[r0.stats.nprocs==np].minval)

            run_max = float(r.stats[r.stats.nprocs==np].maxval)
            run0_max = float(r0.stats[r0.stats.nprocs==np].maxval)
            self.stats = self.stats.append(
                {
                    "nprocs": np,
                    "run_mean": run_mean,
                    "run0_mean": run0_mean,
                    "normalized_means": run_mean/run0_mean,
                    "normalized_means_lower": run_min/run0_max,
                    "normalized_means_upper": run0_min/run_max,
                    "percentage_speed_up" : 100.0*(run0_mean-run_mean)/run0_mean,
                    "percentage_speed_up_lower" : 100.0*(run0_max-run_min)/run0_max,
                    "percentage_speed_up_upper" : 100.0*(run0_min-run_max)/run0_min,
                },
                ignore_index=True,
            )

def calculate_dataframe_averages(df):
    ncol = len(df.columns) - 7
    col = df.loc[: , "1":str(ncol)]
    df['mean'] = col.mean(axis=1)
    df['std'] = col.std(axis=1)
    df['min'] = col.min(axis=1)
    df['max'] = col.max(axis=1)


