#!/bin/bash
# ARM Performance Reports
#
#SBATCH -n64
#SBATCH --time=20:00
#SBATCH --account=do008
#SBATCH --partition=bluefield1
#SBATCH --output=slurm-%A.out  # Job output file
#SBATCH --error=error-%A.out  # Job output file
#SBATCH --exclusive     # No sharing of compute nodes

# set up environment
module purge
module load python/3.6.5
module load intel_comp
module load intel_mpi/2018
module load fftw
module load netcdf
module load hdf5
module load allinea/ddt/20.2.1

export LD_LIBRARY_PATH=~/lib/:$LD_LIBRARY_PATH 
export PATH=~/bin/:$PATH

source ~/BOUT-dev/bout-env/bin/activate

printenv | grep SLURM_ | sort
# benchmark configuration
set -x
export I_MPI_FABRICS=shm:tcp
export OMP_NUM_THREADS=1
export MPS_STAT_LEVEL=2
export APS_ARGS="--collection-mode=mpi"
export executable="../../storm3d/filaments"
cd $SLURM_SUBMIT_DIR
#./runtest.py $SLURM_NTASKS
perf-report --mpi=intel-mpi  -np $SLURM_NTASKS  $executable
