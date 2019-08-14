#!/usr/bin/env python
# -*- coding: utf-8 -*-

help_info="""
####################################################################################################
Author:yangzhushuang  
E-mail:yangzs_chi@yeah.net
Edited by Yang Zhishuang at 2018/01/18
The latest version was edited at : 2018/01/18 By:yangzs 
####################################################################################################
Description:

    This shellscript  is used to annotate genomic proteins to the O&K antigen database.
    
    Requirement:
	BLAST+ >= 2.6.0  (Test version: BLAST 2.6.0+)
    
Usage:
    $0 path/to/amino_acid_file  thread [default:8]
    
    """
import sys , os,time,shutil,subprocess


def chech_before_run():
    print "#"*10 ,"Check the necessary conditions", "#"*10
    if  os.path.exists(in_file):
        print "Input file:\t" , in_file ,"\tok"
    else:
        print "Input file:\t" , in_file ,"\tnot exists"
        sys.exit()
    if not  os.path.exists(O_DB_PATH+".phr"):
        print "Database of O-antigen does not exist,please check:", DB_dir
        sys.exit()
    if not  os.path.exists(K_DB_PATH+".phr"):
        print "Database of K-antigen does not exist,please check:", DB_dir
        sys.exit()
    #Check if blastp can be successfully executed
    if os.system('blastp -h >/dev/null') != 0:
        print 'blastp: command not found\nDownload and install BLAST+ from ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST . And add BLAST+ to the PATH'
        sys.exit()
    print "#"*10 ,"Check completed", "#"*10
def run_annot():
    command1 = "blastp -query " + in_file  + " -db " + O_DB_PATH  + " -max_target_seqs 1  -max_hsps 1 -num_threads " + thread + " -outfmt 6  -evalue 1e-5 -out O_blastout.m6"
    command2 = "blastp -query " + in_file  + " -db " + K_DB_PATH  + " -max_target_seqs 1  -max_hsps 1 -num_threads " + thread + " -outfmt 6  -evalue 1e-5 -out K_blastout.m6"
    proc1 = subprocess.check_call(command1, stdout=subprocess.PIPE, shell=True)
    proc2 = subprocess.check_call(command2, stdout=subprocess.PIPE, shell=True)


Bin_dir = os.path.abspath(sys.argv[0])
DB_dir = os.path.join(Bin_dir.split("bin")[0],"DB")
O_DB_PATH=os.path.join(DB_dir,"O-antigen_DB_from_NCBI_fasta_cds_aa")
K_DB_PATH=os.path.join(DB_dir,"K-antigen_DB_from_NCBI_fasta_cds_aa")

if len(sys.argv) == 2:
    in_file = sys.argv[1]
    thread = str(8)
    chech_before_run()
    run_annot()
elif len(sys.argv) == 3:
    in_file = sys.argv[1]
    thread = str(sys.argv[2])
    chech_before_run()
    run_annot()
else:
    print help_info
    sys.exit() 