#!/bin/bash

#SBATCH --time=12:00:00
#SBATCH -A kropko-ds6001
#SBATCH -o output1254.out
#SBATCH -e error1254.out

module load miniforge/24.3.0-py3.11
conda activate legiscan_env
python get_session_bills.py 1254