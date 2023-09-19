# Wrapper script for running SICILIAN

import glob
import os
import subprocess
import sys
import time
import argparse
import pandas as pd
import random

def get_args(samplesheet):
  args = {}
  arg_df = pd.read_csv(samplesheet)
  bools = ["single","paired","tenX","stranded_library","run_whitelist","run_extract","run_map","run_class","run_GLM"]
  for index,row in arg_df.iterrows():
      var = row["variable"]
      val = row["value"]
      if var in bools:
          if val == "True":
              args[var] = True
          elif val == "False":
              args[var] = False
          else:
              raise ValueError("boolean variable must be set to True or False")
      elif var == "r_ends":
          args[var] = val.split(";")
      elif var == "name_file":
          args["names"] = list(pd.read_csv(val,header=None)[0])
      else:
          args[var] = val
  return args


def sbatch_file(file_name,out_path, name, job_name, time, mem, command, dep="", dep_type = "afterok"):
  """Write sbatch script given parameters"""
  job_file = open(file_name, "w")
  job_file.write("#!/bin/bash\n#\n")
  job_file.write("#SBATCH --job-name=" + job_name + "\n")
  job_file.write("#SBATCH --output={}{}/log_files/{}.%j.out\n".format(out_path, name,job_name))
  job_file.write("#SBATCH --error={}{}/log_files/{}.%j.err\n".format(out_path, name,job_name))
  job_file.write("#SBATCH --time={}\n".format(time))
  job_file.write("#SBATCH --ntasks-per-node={}\n".format(48))
  job_file.write("#SBATCH --nodelist=node00{}\n".format(random.choice([5,6,7,8])))
#  job_file.write("#SBATCH --nodelist=node005,node006,node007,node008")


 
  #job_file.write("#SBATCH --qos=high_p\n")
#  job_file.write("#SBATCH -p horence,owners,quake\n")
#  job_file.write("#SBATCH --account=horence\n")
#  job_file.write("#SBATCH --partition=nih_s10\n")
  job_file.write("#SBATCH --nodes=1\n")
#  job_file.write("#SBATCH --mem={}\n".format(mem)) 
  if dep != "":
    job_file.write("#SBATCH --dependency={}:{}\n".format(dep_type,dep))
    job_file.write("#SBATCH --kill-on-invalid-dep=yes\n")
  job_file.write("date\n")
  job_file.write(command + "\n")
  job_file.write("date\n")
  job_file.close()


def GLM(out_path, name, gtf_file, single, tenX, stranded_library, domain_file, exon_pickle_file, splice_pickle_file, paired, dep = ""):
  """Run the GLM script to compute the statistical scores for junctions in the class input file"""
  command = "Rscript scripts/GLM_script_light.R {}{}/ {} ".format(out_path, name, gtf_file)
  if single:
    command += " 1 "
  else:
    command += " 0 "
  if tenX:
    command += " 1 "
  else:
    command += " 0 "
  if stranded_library:
    command += " 1 "
  else:
    command += " 0 "
  if paired:
    command += " 1 "
  else:
    command += " 0 "

  command += "{} {} {} ".format(domain_file, exon_pickle_file, splice_pickle_file)
  sbatch_file("run_GLM.sh", out_path, name,"GLM_{}".format(name), "48:00:00", "150Gb", command, dep=dep)  # used 200Gb for CML 80Gb for others and 300 for 10x blood3 
  return submit_job("run_GLM.sh")

def whitelist(data_path,out_path, name, bc_pattern, r_ends):
  command = "mkdir -p {}{}\n".format(out_path, name)
  command += "umi_tools whitelist "
  command += "--stdin {}{}{} ".format(data_path, name, r_ends[0])
  command += "--bc-pattern={} ".format(bc_pattern)
  command += "--log2stderr > {}{}_whitelist.txt ".format(data_path,name)
  command += "--plot-prefix={}{} ".format(data_path, name)
 # command += "--knee-method=density "
  sbatch_file("run_whitelist.sh",out_path, name, "whitelist_{}".format(name), "24:00:00", "20Gb", command)
#  return "run_whitelist.sh"
  return submit_job("run_whitelist.sh")

def extract(out_path, data_path, name, bc_pattern, r_ends, dep = ""):
  command = "umi_tools extract "
  command += "--bc-pattern={} ".format(bc_pattern)
  command += "--stdin {}{}{} ".format(data_path, name, r_ends[0])
  command += "--stdout {}{}_extracted{} ".format(data_path, name, r_ends[0])
  command += "--read2-in {}{}{} ".format(data_path, name, r_ends[1])
  command += "--read2-out={}{}_extracted{} ".format(data_path, name, r_ends[1])
#  command += "--read2-stdout "
#  command += "--filter-cell-barcode "
  command += "--whitelist={}{}_whitelist.txt ".format(data_path, name)
  command += "--error-correct-cell "
  sbatch_file("run_extract.sh", out_path, name,"extract_{}".format(name), "24:00:00", "20Gb", command, dep = dep)
#  return "run_extract.sh"
  return submit_job("run_extract.sh")


def class_input(out_path, name, gtf_file, annotator_file, tenX, single, stranded_library, paired, dep=""):
  """Run script to create class input file"""
  command = "python3 scripts/light_class_input.py --outpath {}{}/ --gtf {} --annotator {} --bams ".format(out_path, name, gtf_file,annotator_file) 
  if single:
    command += "{}{}/2Aligned.out.bam ".format(out_path,name)
  elif not paired:
    command += "{}{}/1Aligned.out.bam ".format(out_path,name)

  else:
    command += "{}{}/1Aligned.out.bam ".format(out_path,name)
    command += "{}{}/2Aligned.out.bam ".format(out_path,name)
  if tenX:
    command += "--UMI_bar "
#  if stranded_library:
  command += "--stranded_library "
  if not single and not paired:
    command += "--paired "
  sbatch_file("run_class_input.sh", out_path, name,"class_input_{}".format(name), "48:00:00", "200Gb", command, dep=dep)  # 96:00:00, and 210 Gb for Lu, 100 for others
  return submit_job("run_class_input.sh")


def STAR_map(out_path, data_path, name, r_ends, gzip, single, gtf_file, tenX, star_path, star_ref_path, dep = ""):
  """Run script to perform mapping job for STAR"""
  command = "mkdir -p {}{}\n".format(out_path, name)
  command += "{} --version\n".format(star_path)
  if single or len(r_ends) == 1:
    l = 1
  else:
    l = 0
  for i in range(l,2):
    if len(r_ends) == 1:
      i = 0 
    command += "{} --runThreadN 4 ".format(star_path)
    command += "--genomeDir {} ".format(star_ref_path)
    if tenX:
      command += "--readFilesIn {}{}_extracted{} ".format(data_path, name, r_ends[i])
    else:
      command += "--readFilesIn {}{}{} ".format(data_path, name, r_ends[i])
    if gzip:
      command += "--readFilesCommand zcat "
    command += "--twopassMode Basic "
    command += "--alignIntronMax 1000000 "
    command += "--outFileNamePrefix {}{}/{} ".format(out_path, name, i + 1)
    command += "--outSAMtype BAM Unsorted "
    command += "--outSAMattributes All "
    command += "--chimOutType WithinBAM SoftClip Junctions "
    command += "--chimJunctionOverhangMin 10 "
    command += "--chimSegmentReadGapMax 0 "
    command += "--chimOutJunctionFormat 1 "
    command += "--chimSegmentMin 12 "
  #  command += "--chimMultimapNmax 20 "
    command += "--chimScoreJunctionNonGTAG -4 "
    command += "--chimNonchimScoreDropMin 10 "
  #  command += "--chimMultimapScoreRange 3 "
    command += "--quantMode GeneCounts "
    command += "--sjdbGTFfile {} ".format(gtf_file)
    command += "--outReadsUnmapped Fastx \n\n"
  sbatch_file("run_map.sh", out_path, name,"map_{}".format(name), "24:00:00", "60Gb", command, dep = dep)
  return submit_job("run_map.sh")


def submit_job(file_name):
  """Submit sbatch job to cluster"""
  status, job_num = subprocess.getstatusoutput("sbatch {}".format(file_name))
  if status == 0:
    print("{} ({})".format(job_num, file_name))
    return job_num.split()[-1]
  else:
    print("Error submitting job {} {} {}".format(status, job_num, file_name))

def main():
  samplesheet = sys.argv[1]
  args = get_args(samplesheet)

  if not args["single"]:
    args["run_whitelist"] = False
    args["run_extract"] = False

  if args["r_ends"][0].split(".")[-1] == "gz":
    gzip = True
  else:
    gzip = False

        
  total_jobs = []
  total_job_names = []
  for name in args["names"]:
    jobs = []
    job_nums = []

    if not os.path.exists("{}{}/log_files".format(args["out_path"], name)):
      os.makedirs("{}{}/log_files".format(args["out_path"], name))

    if args["run_whitelist"]:
      whitelist_jobid = whitelist(args["data_path"],args["out_path"], name, args["bc_pattern"], args["r_ends"])
      jobs.append("whitelist_{}.{}".format(name, whitelist_jobid))
      job_nums.append(whitelist_jobid)
    else:
      whitelist_jobid = ""

    if args["run_extract"]:
      extract_jobid = extract(args["out_path"], args["data_path"], name, args["bc_pattern"], args["r_ends"], dep = ":".join(job_nums))
      jobs.append("extract_{}.{}".format(name, extract_jobid))
      job_nums.append(extract_jobid)
    else:
      extract_jobid = ""

    if args["run_map"]:
      map_jobid = STAR_map(args["out_path"], args["data_path"], name, args["r_ends"], gzip, args["single"], args["gtf_file"], args["tenX"], args["star_path"], args["star_ref_path"], dep = ":".join(job_nums))
      jobs.append("map_{}.{}".format(name,map_jobid))
      job_nums.append(map_jobid)

    if args["run_class"]:
      class_input_jobid = class_input(args["out_path"], name, args["gtf_file"], args["annotator_file"], args["tenX"], args["single"], args["stranded_library"], args["paired"], dep=":".join(job_nums))
      jobs.append("class_input_{}.{}".format(name,class_input_jobid))
      job_nums.append(class_input_jobid)
    else:
      class_input_jobid = ""

    if args["run_GLM"]:
      GLM_jobid = GLM(args["out_path"], name, args["gtf_file"], args["single"], args["tenX"], args["stranded_library"], args["domain_file"], args["exon_pickle_file"], args["splice_pickle_file"], args["paired"], dep=":".join(job_nums))
      jobs.append("GLM_{}.{}".format(name,GLM_jobid))
      job_nums.append(GLM_jobid)
    else:
      GLM_jobid =  ""

main()
