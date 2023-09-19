#!/bin/bash
#
#SBATCH --job-name=consolidate_pollen
#SBATCH --output=/exports/home/jolivieri/data/sicilian/PRJNA930874/pollen/postprocess_log_files/consolidate_pollen.%j.out
#SBATCH --error=/exports/home/jolivieri/data/sicilian/PRJNA930874/pollen/postprocess_log_files/consolidate_pollen.%j.err
#SBATCH --time=48:00:00
#SBATCH -p node004
#SBATCH --nodes=1
#SBATCH --mem=150Gb
date
Rscript scripts/consolidate_GLM_output_files.R /exports/home/jolivieri/data/sicilian/PRJNA930874/pollen/ pollen /exports/home/jolivieri/data/genomes/annotation_pkl_files/TAIR10_exon_bounds.pkl /exports/home/jolivieri/data/genomes/annotation_pkl_files/TAIR10_splices.pkl  0 
date
