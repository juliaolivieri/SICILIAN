#!/bin/bash
#
#SBATCH --job-name=extract_SRR21548619
#SBATCH --output=/exports/home/jolivieri/data/sicilian/GSE213264/Mouse_RNA/SRR21548619/log_files/extract_SRR21548619.%j.out
#SBATCH --error=/exports/home/jolivieri/data/sicilian/GSE213264/Mouse_RNA/SRR21548619/log_files/extract_SRR21548619.%j.err
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --dependency=afterok:122213
#SBATCH --kill-on-invalid-dep=yes
date
umi_tools extract --bc-pattern=CCCCCCCCCCCCCCCCNNNNNNNNNN --stdin /exports/home/jolivieri/data/citeseq/GSE213264/SRR21548619_R2_processed.fastq.gz --stdout /exports/home/jolivieri/data/citeseq/GSE213264/SRR21548619_extracted_R2_processed.fastq.gz --read2-in /exports/home/jolivieri/data/citeseq/GSE213264/SRR21548619_1.fastq.gz --read2-out=/exports/home/jolivieri/data/citeseq/GSE213264/SRR21548619_extracted_1.fastq.gz --whitelist=/exports/home/jolivieri/data/citeseq/GSE213264/SRR21548619_whitelist.txt --error-correct-cell 
date
