#!/bin/bash
#SBATCH -J vesselSegmentationMri1  
#SBATCH -N 1         
#SBATCH --gres=gpu:1          
#SBATCH --mem-per-cpu=5500    
#SBATCH --ntasks-per-node 1   
#SBATCH --cpus-per-task 10    
#SBATCH --time 48:00:00        
. /usr/local/bin/slurmProlog.sh  
testenv=py36pt     
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/bin/virtualenv
export WORKON_HOME=/opt/pythonenv/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
workon $testenv #  deactivate to leave it
cd /scratch/$USER/; echo "pwd=$(pwd)"; python -V  
srun python3 /home/kprabhu/code/executor.py >slurm-$SLURM_JOBID.pyout 2>&1
deactivate  # workoff :)
. /usr/local/bin/slurmEpilog.sh   