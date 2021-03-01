#!/bin/bash
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
module load hdf5
module load netcdf

export PATH=~/netcdf-c++-intel-2018/bin/:~/local/bin/:$PATH
export LD_LIBRARY_PATH=~/netcdf-c++-intel-2018/lib/:$LD_LIBRARY_PATH

source ~/BOUT-dev/bout-env/bin/activate

printenv | grep SLURM_ | sort
# benchmark configuration
set -x
export I_MPI_FABRICS=shm:tcp
export OMP_NUM_THREADS=1
cd $SLURM_SUBMIT_DIR
./runtest.py $SLURM_NTASKS
mv test_run.log test_run_${SLURM_NTASKS}.log

