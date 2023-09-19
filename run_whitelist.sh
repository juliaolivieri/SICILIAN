#!/bin/bash
#
#SBATCH --job-name=whitelist_SRR21548619
#SBATCH --output=/exports/home/jolivieri/data/sicilian/GSE213264/Mouse_RNA/SRR21548619/log_files/whitelist_SRR21548619.%j.out
#SBATCH --error=/exports/home/jolivieri/data/sicilian/GSE213264/Mouse_RNA/SRR21548619/log_files/whitelist_SRR21548619.%j.err
#SBATCH --time=24:00:00
#SBATCH --nodes=1
date
mkdir -p /exports/home/jolivieri/data/sicilian/GSE213264/Mouse_RNA/SRR21548619
umi_tools whitelist --stdin /exports/home/jolivieri/data/citeseq/GSE213264/SRR21548619_R2_processed.fastq.gz --bc-pattern=CCCCCCCCCCCCCCCCNNNNNNNNNN --log2stderr > /exports/home/jolivieri/data/citeseq/GSE213264/SRR21548619_whitelist.txt --plot-prefix=/exports/home/jolivieri/data/citeseq/GSE213264/SRR21548619 
date
