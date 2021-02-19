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
$ python3 plot_scaling.py
```

## gcc/openmpi scaling

Branch above used icc/intelmpi. Data for code compiled with gcc/opnmpi is in
the `gcc-openmpi` subdirectory.

To plot do

```
$ cd gcc-openmpi
$ python3 plot_scaling.py
```
