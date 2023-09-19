#!/bin/bash
## this is a wrapper for passing the input arguments to the SICILIAN postprocessing script


############ Input arguments ###########################
OUT_DIR="/exports/home/jolivieri/data/sicilian/PRJNA930874"   #SICILIAN output folders for  all samples in a dataset should be in ${OUT_DIR}/${RUN_NAME}#
RUN_NAME="pollen"
GENOME_NAME="TAIR10"
GTF_FILE="/exports/home/jolivieri/data/genomes/${GENOME_NAME}/${GENOME_NAME}_GFF3_genes.gff"
EXON_PICKLE_FILE="/exports/home/jolivieri/data/genomes/annotation_pkl_files/${GENOME_NAME}_exon_bounds.pkl"
SPLICE_PICKLE_FILE="/exports/home/jolivieri/data/genomes/annotation_pkl_files/${GENOME_NAME}_splices.pkl"
DATA_FORMAT="ss2"  # scRNA-Seq data format, should be either 10x or SS2
QUEUE="node004"   # the queue for submitting jobs
########################################################

######## the three steps required for SICILIAN postprocessing #########
## For running each step, its corresponding flag should be set to True, otherwise it should be set to False
RUN_consolidate="True"
RUN_process="True"
RUN_postprocess="True"
######################################################################


python3 SICILIAN_post_process.py -d ${OUT_DIR} -r ${RUN_NAME} -g ${GTF_FILE} -e ${EXON_PICKLE_FILE} -s ${SPLICE_PICKLE_FILE} -f ${DATA_FORMAT} -q ${QUEUE} -a ${RUN_consolidate} -b ${RUN_process} -c ${RUN_postprocess}

