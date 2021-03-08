#!/bin/bash
#
#SBATCH -n1
#SBATCH --time=1:00:00
#SBATCH --account=do008
#SBATCH --partition=bluefield1
#SBATCH --output=slurm-%A.out  # Job output file
#SBATCH --error=error-%A.out  # Job output file
#SBATCH --exclusive     # No sharing of compute nodes

# set up environment
module purge
module load python/3.6.5
module load intel_comp/2018-update2
module load intel_mpi/2018
module load fftw/3.3.9
module load hdf5
module load netcdf/4.6.1
module load advisor

export LD_LIBRARY_PATH=~/netcdf-c++-intel-2018/lib/:~/local/lib/:$LD_LIBRARY_PATH
export PATH=~/netcdf-c++-intel-2018/bin/:~/local/bin/:$PATH

source ~/BOUT-dev/bout-env/bin/activate

#printenv | grep SLURM_ | sort
# benchmark configuration
set -x
#export I_MPI_FABRICS=shm:ofi
export OMP_NUM_THREADS=1
export MPS_STAT_LEVEL=2
cd $SLURM_SUBMIT_DIR

EXE=iterator
#RUNCMD="mpirun --mca btl_tcp_if_include p1p2 -x UCX_NET_DEVICES=mlx5_1:1"
RUNCMD="mpirun"

$RUNCMD -n 1 -gtool "advixe-cl -collect survey -project-dir results-1m1p-single:0" ./${EXE}
$RUNCMD -n 1 -gtool "advixe-cl -collect tripcounts -flop -project-dir results-1m1p-single:0" ./${EXE}

#$RUNCMD -n 32 advixe-cl -collect survey -project-dir results-32 -- ./${EXE}
#$RUNCMD -n 32 advixe-cl -collect tripcounts -flop -project-dir results-32 -- ./${EXE}
