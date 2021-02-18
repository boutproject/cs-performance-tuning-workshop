# Building BOUT++ on DINE

The following steps worked for uninstrumented code, 18/2/21

```
module load intel_comp/2018 intel_mpi/2018
module load fftw
module load netcdf
# Needed to manually build netcdf-c++, put relavent things in ~/bin and ~/lib
export PATH=~/bin/:$PATH
export LD_LIBRARY_PATH=~/lib/:$LD_LIBRARY_PATH
./configure --enable-checks=no --enable-optimize=3
make
```

The following fails
```
module load intel_comp/2020-update2 intel_mpi/2020-update2
module load fftw/3.3.8
This package (netcdf/4.6.1) has not been built for intel_comp/2020-update2
```


