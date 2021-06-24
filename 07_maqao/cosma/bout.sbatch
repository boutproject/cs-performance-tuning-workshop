#!/bin/bash -l

#SBATCH -p bluefield1
#SBATCH -A do008
#SBATCH --time=5 # 5 minutes
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16

#module purge
module load intel_comp/2020-update2 intel_mpi/2020-update2
module load fftw/3.3.8
module load hdf5/1.10.6
export PATH=~/local/bin/:$PATH
export LD_LIBRARY_PATH=~/local/lib/:$LD_LIBRARY_PATH

echo $PATH
echo $LD_LIBRARY_PATH

source ~/BOUT-dev/bout-env/bin/activate

printenv | grep SLURM_ | sort
# benchmark configuration
set -x
export I_MPI_FABRICS=shm:tcp
export OMP_NUM_THREADS=1
export MPS_STAT_LEVEL=2
export APS_ARGS="--collection-mode=mpi"

cd $SLURM_SUBMIT_DIR
mpiexec -np $SLURM_NTASKS -genv UCX_NET_DEVICES mlx5_1:1 ./blob2d -d delta_0.25
