# Basic scaling

This contains files and results for a strong scaling of STORM's nonisothermal
test case for intel-intelmpi and gcc-openmpi toolchains.
`sbatch` files should be submitted from `STORM/tests3d/test-nonisothermal`, by
doing

```
$ sbatch scaling_<n>.sbatch
```

Output is written to `test_run_<n>.log`.

To plot the data for both cases, do

```
$ python3 plot_scaling.py
```

in this directory. 
Alternatively, plot the data for one case by doing

```
$ python3 plot_scaling.py
```

from either the intel-intelmpi or gcc-openmpi subdirectory.
