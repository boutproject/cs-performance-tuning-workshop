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

## Scorep

The Scorep module only works with:
```
This package (scorep/6.0) has not been built for intel_2018_intel_mpi_2018
Available builds are:
        gnu_comp/10.2.0         with openmpi/4.0.5
        intel_comp/2020-update2         with intel_mpi/2020-update2
```
but netcdf only works with
```
This package (netcdf/4.6.1) has not been built for intel_comp/2020-update2
It can be used with the following compilers:
        gnu_comp/7.3.0
        intel_comp/2018
```
These are the only versions of netcdf and Scorep available.

Manually installing netcdf:
```
module load intel_comp/2020-update2 intel_mpi/2020-update2
module load fftw/3.3.8
module load hdf5/1.10.6

# First build zlib (not sure this is necessary when using the hdf5 module)
wget https://www.zlib.net/zlib-1.2.11.tar.gz
tar xvf zlib-1.2.11.tar.gz
cd zlib-1.2.11
./configure --prefix=$HOME/local
make check install

# Now install netcdf
cd ~/
wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-c-4.7.4.tar.gz
tar xvf netcdf-c-4.7.4.tar.gz
cd netcdf-c-4.7.4
export LD_LIBRARY_PATH=/cosma/local/hdf5//intel_2020-update2/1.10.6/lib:$LD_LIBRARY_PATH
CPPFLAGS=-I/cosma/local/hdf5//intel_2020-update2/1.10.6/include LDFLAGS=-L/cosma/local/hdf5//intel_2020-update2/1.10.6/lib ./configure --prefix=$HOME/local
make check install
# wait a long, long time

# Now install netcdf-c++
cd ~/
wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-cxx4-4.3.1.tar.gz
tar xvf netcdf-cxx4-4.3.1.tar.gz
cd netcdf-cxx4-4.3.1
autoreconf -if
mkdir build
cd build
CPPFLAGS=-I$HOME/local/include LDFLAGS=-L$HOME/local/lib ../configure --prefix=$HOME/local
make
make check
make install

# Now install BOUT
cd path/to/BOUT-dev
./configure --enable-checks=no --enable-optimize=3 --with-scorep
make
```



