Intel Vtune profiling tools are available on Marconi. Documentation on profiling is here https://wiki.u-gov.it/confluence/display/SCAIUS/UG3.1%3A+MARCONI+UserGuide#UG3.1:MARCONIUserGuide-DebuggersandProfilers

To get the maximum information (e.g. on vectorisation) from `aps`, it is necessary to add a line
```
#SBATCH -C vtune
```
to the submission script.

Then, taking `aps_storm` as the name of the output directory for this example, run the program like
```
mpirun -np 48 aps -r aps_storm filaments
```
and produce a report with the command
```
aps-report -r aps_storm
```

Optionally, more detailed information on MPI operation can be produced with some extra options
```
APS_STAT_LEVEL=4 mpirun -np 48 aps -r aps_storm filaments
```
```
aps-report --all -r aps_storm
```

Some example reports are included in this directory.
* `aps_storm-intel2018` used intel-2018/intelmpi-2018 and `-O3 -no-inline-max-size -no-inline-max-total-size`
* `aps_storm-intel2020-noflags` used intel-2020/intelmpi-2020 and `-O3`
* `aps_storm-intel2020-extraopt-noflags` used intel-2020/intelmpi-2020 and `-Ofast -funroll-loops -xCORE-AVX512 -mtune=skylake`
* `aps_storm-intel2020-extraopt` used intel-2020/intelmpi-2020 and `-Ofast -funroll-loops -xCORE-AVX512 -mtune=skylake -no-inline-max-size -no-inline-max-total-size`

The extra optimization flags improved vectorisation minimally: 7.00% for `aps_storm-intel2020-noflags`; 7.90% for `aps_storm-intel2020-extraopt-noflags`; and 8.90% for `aps_storm-intel2020-extraopt`.
