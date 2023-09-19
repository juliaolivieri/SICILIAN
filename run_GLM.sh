#!/bin/bash
#
#SBATCH --job-name=GLM_SRR23387043
#SBATCH --output=/exports/home/jolivieri/data/sicilian/PRJNA930874SRR23387043/log_files/GLM_SRR23387043.%j.out
#SBATCH --error=/exports/home/jolivieri/data/sicilian/PRJNA930874SRR23387043/log_files/GLM_SRR23387043.%j.err
#SBATCH --time=48:00:00
#SBATCH --ntasks-per-node=48
#SBATCH --nodelist=node005
#SBATCH --nodes=1
#SBATCH --dependency=afterok:124304:124305
#SBATCH --kill-on-invalid-dep=yes
date
Rscript scripts/GLM_script_light.R /exports/home/jolivieri/data/sicilian/PRJNA930874SRR23387043/ /exports/home/jolivieri/data/genomes/TAIR10/TAIR10_GFF3_genes.gff  1  0  0  0 /exports/home/jolivieri/data/citeseq/GSE213264/41587_2023_1676_MOESM3_ESM.csv /exports/home/jolivieri/data/genomes/annotation_pkl_files/TAIR10_exon_bounds.pkl /exports/home/jolivieri/data/genomes/annotation_pkl_files/TAIR10_splices.pkl 
date
