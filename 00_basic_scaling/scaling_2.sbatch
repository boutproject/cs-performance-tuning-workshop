#!/bin/bash
#
#SBATCH -n2
#SBATCH --time=30:00
#SBATCH --account=do008
#SBATCH --partition=bluefield1
#SBATCH --output=slurm-%A.out  # Job output file
#SBATCH --error=error-%A.out  # Job output file
#SBATCH --exclusive     # No sharing of compute nodes

# set up environment
module purge
module load python/3.6.5
#pip install --user boutdata
module load intel_comp
module load intel_mpi/2018
module load fftw
module load hdf5

source ~/BOUT-dev/bout-env/bin/activate

printenv | grep SLURM_ | sort
# benchmark configuration
set -x
export OMP_NUM_THREADS=1
cd $SLURM_SUBMIT_DIR
./runtest.py $SLURM_NTASKS
mv test_run.log test_run_${SLURM_NTASKS}.log
