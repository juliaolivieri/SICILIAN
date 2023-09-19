#!/bin/bash
#
#SBATCH --job-name=process_Mouse_intestine_RNA
#SBATCH --output=/exports/home/jolivieri/data/sicilian/GSE213264/Mouse_intestine_RNA/postprocess_log_files/process_Mouse_intestine_RNA.%j.out
#SBATCH --error=/exports/home/jolivieri/data/sicilian/GSE213264/Mouse_intestine_RNA/postprocess_log_files/process_Mouse_intestine_RNA.%j.err
#SBATCH --time=12:00:00
#SBATCH -p horence
#SBATCH --nodes=1
##SBATCH --mem=350Gb
date
python3 scripts/Process_CI_10x.py -d /exports/home/jolivieri/data/sicilian/GSE213264/Mouse_intestine_RNA/ -o Mouse_intestine_RNA -g /exports/home/jolivieri/data/genomes/mm10/mm10.ensGene.gtf -e /exports/home/jolivieri/data/genomes/annotation_pkl_files/mm10_exon_bounds.pkl -s /exports/home/jolivieri/data/genomes/annotation_pkl_files/mm10_splices.pkl
date
