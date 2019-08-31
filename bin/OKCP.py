#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
##############################################################
       ######    ####  ###     ######   #######
     ####  ###    ## ####    ###   ##    ##  ###
    ###     ##   ######     ##           ##  ###
   ###     ###   ####      ###          #######
   ##     ###   ##  ##     ###          ##
   ###  ####    ##  ####    ########   ##
     #####     #### #####    ######   ####
##############################################################

  O&K-antigen synthesis gene cluster annotation pipeline    
                                                         
	OKCP (O antigen & K antigen gene cluster prediction)is
  used to predict the O antigen, K antigen gene cluster on  
  on the bacterial genome.                                  
                                                            
  Author: Zhishuang Yang                                    
  E-mail: yangzs_chi@yeah.net                               
  Version: 1.0.0                                            

Description:
    OKCP is used to annotate genomic proteins to the O&K antigen database.
    
Usage:
    
    OKCP.py  -gb gbk_file  -bT blast_thread hmm_db -hT hmm_thread
    ARGUMENTS:
            -gb gbk_file
            -bT blast_thread
            -HMM hmm_db
            -hT hmm_thread
    OPTIONAL:

    """

import sys , os,shutil,subprocess, glob,re


#def get_arg():




def check_script():
    self_path = os.path.abspath(sys.argv[0])
    Bin_dir = os.path.split(self_path)[0]
    script_list = ["gbk2gff.py","gbk2faa.py","blast2OKDB.py","Identifi_cluster.py" ,"hmmscan_parse.py","tmhmm_Parse.py"]
    for script in script_list:
        script_path = os.path.join(Bin_dir,script)
        if not os.path.exists(script_path):
            print script ,"not in the correct position: " ,Bin_dir
            sys.exit(-1)
def create_work_dir(gbk_file):
    file_name=os.path.split(gbk_file)[1].rsplit(".",1)[0]
    if not os.path.exists(file_name):
        try:
            os.makedirs(file_name)
        except:
            print "Cannot create working directory ./%s in current location" % file_name
    else:
        sys.stdout.write(file_name +" already exists and will be overwritten" )
        os.remove(file_name)
        os.makedirs(file_name)
    try:
        os.chdir(file_name)
    except:
        print "Can't change directory to ./" , file_name


def Prepare_file(gbk_file):
    self_path = os.path.abspath(sys.argv[0])
    Bin_dir = os.path.split(self_path)[0]
    gff_file_name =  os.path.split(gbk_file)[1] + ".gff"
    print "Convert gbk to gff annotation file...\n"
    cmd1 =  "python " + os.path.join(Bin_dir,"gbk2gff.py") + " " + gbk_file + " " + gff_file_name
    p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, shell=True)
    stout=p1.stdout.read()
    print stout
    print "Convert gbk to protein  file...\n"
    cmd2 = "python " + os.path.join(Bin_dir, "gbk2faa.py") + " " + gbk_file
    p2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, shell=True)
    stout = p2.stdout.read()
    print stout

def  blast_to_OKdb(in_faa,thread):
    self_path = os.path.abspath(sys.argv[0])
    Bin_dir = os.path.split(self_path)[0]
    cmd3 = "python " + os.path.join(Bin_dir, "blast2OKDB.py") + " " + in_faa + " " +thread
    print "Annotating to the O&K antigen database"
    p3 = subprocess.Popen(cmd3, stdout=subprocess.PIPE, shell=True)
    stout = p3.stdout.read()
    print stout


def Predicted_gene_cluster(m6_file,gff_file,faa_file):
    self_path = os.path.abspath(sys.argv[0])
    Bin_dir = os.path.split(self_path)[0]
    cmd5 = "python " + os.path.join(Bin_dir, "Identifi_cluster.py") + " " + m6_file + " " +gff_file + " " +faa_file
    p5 = subprocess.Popen(cmd5, stdout=subprocess.PIPE, shell=True)
    stout = p5.stdout.read()
    print stout

def hmmsearch(faa_file,hmm_db,thread):
   " hmmscan -o ${faa %.faa *}.txt - -domtblout ${faa %.faa *}.tab - E 1e-5 - -cpu 10 - -domE 1e-5.. /../ DB / wza_wzc_wzx_wzy / wza_wzc_wzx_wzy.hmm $faa"
   txt_out = faa_file.split(".faa")[0] + ".txt"
   tab_out = faa_file.split(".faa")[0] + ".tab"
   cmd4 = "hmmscan""  -E 1e-5  --domE  1e-5 --cpu  " + thread + " -o " +  txt_out  + " --domtblout  " + tab_out + "  " + hmm_db + "  " + faa_file
   p4 = subprocess.Popen(cmd4, stdout=subprocess.PIPE, shell=True)
   stout = p4.stdout.read()
   print stout

def get_file_name(file_pattern):
    #return a list
    return  glob.glob(file_pattern)


def print_out(cluster_faa):
    self_path = os.path.abspath(sys.argv[0])
    Bin_dir = os.path.split(self_path)[0]
    tab_out = cluster_faa.split(".faa")[0] + ".tab"
    cmd5 = "python " + os.path.join(Bin_dir, "hmmscan_parse.py") + " " + tab_out +"   1e-5  0.35 "
    p5 = subprocess.Popen(cmd5, stdout=subprocess.PIPE, shell=True)
    out5, err = p5.communicate()
    status = p5.wait()
    stout5 = out5
    cmd6 = "python " + os.path.join(Bin_dir, "tmhmm_Parse.py ") + " " +cluster_faa
    p6 = subprocess.Popen(cmd6, stdout=subprocess.PIPE, shell=True)
    out6, err = p6.communicate()
    status = p6.wait()
    stout6 = out6
    for gene in ["wza" ,"wzc" ,"wzt","wzm"]:
        pattern = gene + "_.+?\n"
        line_list = re.findall(pattern, stout5)
        if len(line_list) >=1:
            sys.stdout.write( ''.join(line_list))
    thm_result_list=[term.split("\t")[0] for term in  stout6.split("\n")]
    for gene in thm_result_list:
        line_list = [item for item in stout5.split("\n") if item.find("\t"+gene + "\t") != -1]
        if len(line_list) >=1:
            sys.stderr.write('\n'.join(line_list) + "\n")




def main(gbk_file,blast_thread,hmm_db,hmm_thread):
    gbk_file = os.path.abspath(gbk_file)
    #check input file
    try:
        f = open(gbk_file)
        f.close()
    except IOError:
        print "File is not accessible:" ,gbk_file
        sys.exit(-1)
    check_script()
    create_work_dir(gbk_file)
    input_name = os.path.split(gbk_file)[1]
    in_faa = input_name + "_out.faa"
    gff_file = input_name + ".gff"
    Prepare_file(gbk_file)
    blast_to_OKdb(in_faa, blast_thread)

    name_pattern =  "*_Predicted_gene_cluster_No*.faa"
    for faa in get_file_name(name_pattern):
        os.remove(faa)

    for type in ["K" ,"O"]:
        m6_file = type + "_blastout.m6"
        print "Candidate ", type ,"antigen gene cluster:"
        Predicted_gene_cluster(m6_file, gff_file, in_faa)

    print "\n           Oligosaccharide unit processing enzyme gene           \n"
    for type in ["K", "O"]:
        print "\n       For ",type," antigen cluster\n"
        name_pattern = type + "_Predicted_gene_cluster_No*.faa"
        for faa in get_file_name(name_pattern):
            hmmsearch(faa,hmm_db, hmm_thread)
            print faa
            print_out(faa)


    for tem_file in  get_file_name("*_Predicted_gene_cluster_No*.t*"):
        os.remove(tem_file)



if __name__=='__main__':
    try:
        gbk_file = sys.argv[1]
        blast_thread = sys.argv[2]
        hmm_db  = sys.argv[3]
        hmm_thread = sys.argv[4]
    except:
        print __doc__
        sys.exit(-1)
    main(gbk_file,blast_thread,hmm_db,hmm_thread)

#print __doc__