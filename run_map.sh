#!/bin/bash
#
#SBATCH --job-name=map_SRR23387043
#SBATCH --output=/exports/home/jolivieri/data/sicilian/PRJNA930874SRR23387043/log_files/map_SRR23387043.%j.out
#SBATCH --error=/exports/home/jolivieri/data/sicilian/PRJNA930874SRR23387043/log_files/map_SRR23387043.%j.err
#SBATCH --time=24:00:00
#SBATCH --ntasks-per-node=48
#SBATCH --nodelist=node005
#SBATCH --nodes=1
date
mkdir -p /exports/home/jolivieri/data/sicilian/PRJNA930874SRR23387043
STAR --version
STAR --runThreadN 4 --genomeDir /exports/home/jolivieri/data/genomes/STAR_indices/TAIR10 --readFilesIn /exports/home/jolivieri/data/bulk/PRJNA930874/SRR23387043_2.fastq.gz --readFilesCommand zcat --twopassMode Basic --alignIntronMax 1000000 --outFileNamePrefix /exports/home/jolivieri/data/sicilian/PRJNA930874SRR23387043/2 --outSAMtype BAM Unsorted --outSAMattributes All --chimOutType WithinBAM SoftClip Junctions --chimJunctionOverhangMin 10 --chimSegmentReadGapMax 0 --chimOutJunctionFormat 1 --chimSegmentMin 12 --chimScoreJunctionNonGTAG -4 --chimNonchimScoreDropMin 10 --quantMode GeneCounts --sjdbGTFfile /exports/home/jolivieri/data/genomes/TAIR10/TAIR10_GFF3_genes.gff --outReadsUnmapped Fastx 


date
