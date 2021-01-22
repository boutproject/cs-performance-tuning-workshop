# Basic scaling

This contains files and results for a strong scaling of STORM's nonisothermal
test case.  `sbatch` files should be submitted from
`STORM/tests3d/test-nonisothermal`, by doing

```
$ sbatch scaling_<n>.sbatch
```

Output is written to `test_run_<n>.log`.

To plot the data, do

```
$ python plot_scaling.py
```
