#!/bin/bash
#
#SBATCH --job-name=postprocess_pollen
#SBATCH --output=/exports/home/jolivieri/data/sicilian/PRJNA930874/pollen/postprocess_log_files/postprocess_pollen.%j.out
#SBATCH --error=/exports/home/jolivieri/data/sicilian/PRJNA930874/pollen/postprocess_log_files/postprocess_pollen.%j.err
#SBATCH --time=48:00:00
#SBATCH -p node004
#SBATCH --nodes=1
#SBATCH --mem=200Gb
date
Rscript scripts/post_processing.R /exports/home/jolivieri/data/sicilian/PRJNA930874/pollen/ pollen  0 
date
