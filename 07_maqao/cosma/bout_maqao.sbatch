#!/bin/bash -l
# submit from ./bin subdirectory with "sbatch bt.sbatch"

#SBATCH -p bluefield1
#SBATCH -A do008
#SBATCH --time=5 # 5 minutes
#SBATCH --nodes=<number_nodes>
#SBATCH --ntasks-per-node=<number_processes_per_node>
#SBATCH --ntasks=<number_processes>

#module purge
module load intel_comp/2020-update2 intel_mpi/2020-update2
module load fftw/3.3.8
module load hdf5/1.10.6
export PATH=~/local/bin/:$PATH
export LD_LIBRARY_PATH=~/local/lib/:~/BOUT-dev-may/lib/:$LD_LIBRARY_PATH
echo $LD_LIBRARY_PATH
module load maqao

source ~/BOUT-dev/bout-env/bin/activate

<mpi_command> <run_command>
