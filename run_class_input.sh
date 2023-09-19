#!/bin/bash
#
#SBATCH --job-name=class_input_SRR23387043
#SBATCH --output=/exports/home/jolivieri/data/sicilian/PRJNA930874SRR23387043/log_files/class_input_SRR23387043.%j.out
#SBATCH --error=/exports/home/jolivieri/data/sicilian/PRJNA930874SRR23387043/log_files/class_input_SRR23387043.%j.err
#SBATCH --time=48:00:00
#SBATCH --ntasks-per-node=48
#SBATCH --nodelist=node005
#SBATCH --nodes=1
#SBATCH --dependency=afterok:124304
#SBATCH --kill-on-invalid-dep=yes
date
python3 scripts/light_class_input.py --outpath /exports/home/jolivieri/data/sicilian/PRJNA930874SRR23387043/ --gtf /exports/home/jolivieri/data/genomes/TAIR10/TAIR10_GFF3_genes.gff --annotator /exports/home/jolivieri/data/genomes/annotation_pkl_files/TAIR10.pkl --bams /exports/home/jolivieri/data/sicilian/PRJNA930874SRR23387043/2Aligned.out.bam --stranded_library 
date
