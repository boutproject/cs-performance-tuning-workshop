#!/bin/bash

#SBATCH -n32
#SBATCH --time=1:00:00
#SBATCH --account=do008
#SBATCH --partition=bluefield1
#SBATCH --output test.log
#SBATCH --error error.log

module purge
module load python/3.6.5 gnu_comp/10.2.0 openmpi/4.0.5 sundials/5.1.0 hdf5/1.10.6 fftw/3.3.8

cd $SLURM_SUBMIT_DIR
./runtest.py $SLURM_NTASKS
mv test_run.log test_run_${SLURM_NTASKS}.log
