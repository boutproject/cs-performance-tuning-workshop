To generate the results in the folder, do

```
maqao oneview -R1 --config=bout_OV_sbatch.lua -xp=ov_sbatch
```

on command line, not in a submission script. Note that the configure file
`bout_OV_sbatch.lua` will need to be updated so that the **absolute** paths to
the executable, external library and directory in `run_command` are correct.

To view results, do

```
firefox <path_to>/ov_sbatch/RESULTS/blob2d_one_html/index.html &
```
