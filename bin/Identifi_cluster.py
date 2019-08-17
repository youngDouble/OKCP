#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
####################################################################################################
Author:yangzhushuang  
E-mail:yangzs_chi@yeah.net
Edited by Yang Zhishuang at 2019/08/15
The latest version was edited at : 2019/08/15 By:yangzs
####################################################################################################
Description:

    This script  is used to annotate genomic proteins to the O&K antigen database.
    
    Requirement:
	gff_file
    
Usage:
    Identifi_cluster.py path/to/O_blastout.m6   path/to/gff_file
    
    """

import sys , os,time,shutil,subprocess, math




def read_gff_file(gff_file):
    gff=open(gff_file).readlines()
    return gff

#Return genome average per gene length,Genomic length (bp) divided by number of genes.
def Average_gene_region_length(gff_file_list):
    genome_length = 0
    gff_filted = [line for line in gff_file_list if line.find("##sequence-region") != -1 ]
    for i in gff_filted:
        num_contig = int(i.strip('\n').split(' ')[-1])
        genome_length += num_contig
    gff_filted_cds = [line for line in gff_file_list if line.find("\tgene\t") != -1]
    gene_num = len(gff_filted_cds)
    Average_gene_length = int(math.ceil(genome_length/gene_num))
    return  Average_gene_length

#Return the location of the gene
def gene_locus(gff_file_list,gene_name):
    gff_filted_cds = [line for line in gff_file_list if line.find("\tgene\t") != -1 and line.find("locus_tag="+gene_name) != -1]
    info_line = gff_filted_cds[0].split('\t')
    accession_num = info_line[0]
    start_num = info_line[3]
    end_num = info_line[4]
    gene_locus_list = [accession_num,start_num,end_num]
    return gene_locus_list

#If the adjacent annotation gene interval is greater than 5 times the average gene length, the gene cluster breaks.
def break_judgment(gff_file_list,Average_gene_region_length,gene_name1,gene_name2):
    gene1_locus_list = gene_locus(gff_file_list, gene_name1)
    gene2_locus_list = gene_locus(gff_file_list, gene_name2)
    gene1_accession_num = gene1_locus_list[0]
    gene2_accession_num = gene2_locus_list[0]
    gene1_end = int(gene1_locus_list[2])
    gene2_start =  int(gene2_locus_list[1])
    gap_length  = abs(gene2_start - gene1_end)
    if gene1_accession_num != gene2_accession_num :
        return  False
    elif gap_length >= int(Average_gene_region_length) * 5:
        return False
    else:
        return True


def get_faa_id(gene_start,gene_end,gff_file_list):
    gff_filted_cds = [line for line in gff_file_list if line.find("\tgene\t") != -1 ]
    gff_gene_name_list = [line.split("locus_tag=")[-1].strip("\n") for line in gff_filted_cds]
    start_idx = gff_gene_name_list.index(gene_start)
    end_idx = gff_gene_name_list.index(gene_end)+1
    faa_id_list=gff_gene_name_list[start_idx:end_idx]
    return faa_id_list

def Extract_seq_all(in_file,seq_id,out_file):
    all_the_text = open(in_file).read()
    all_the_text = "\n" + all_the_text
    all_list = all_the_text.split('\n>')[1:]
    out_f = open(out_file,'a+')
    for term in all_list:
        if term.startswith(seq_id + ' '):
            jion_str = ''
            seq_id = term.split('\n')[0]
            seq = jion_str.join(term.split('\n')[1:])
            name_line= '>'+seq_id
            out_f.write(name_line + '\n')
            out_f.write(seq + '\n')
        elif term.startswith(seq_id + '\n'):
            jion_str = ''
            seq_id = term.split('\n')[0]
            seq = jion_str.join(term.split('\n')[1:])
            name_line= '>'+seq_id
            out_f.write(name_line + '\n')
            out_f.write(seq + '\n')
    out_f.close()

def read_m6_2_list(in_file,gff_file,faa_file):
    m6_file=open(in_file).readlines()
    m6_file_filted = [line.split('\t')[0:2] for line in m6_file]
    #return m6_file_filted
    gff_file_list = read_gff_file(gff_file)
    len_per_gene = Average_gene_region_length(gff_file_list)
    cluster_list = []
    cluster_num = 1
    for term_num in  range(len(m6_file_filted)):
        if term_num == 0:
            cluster_list.append(m6_file_filted[term_num][0])
        else:
            gene_name1 = m6_file_filted[term_num-1][0]
            gene_name2 = m6_file_filted[term_num][0]
            if break_judgment(gff_file_list, len_per_gene, gene_name1, gene_name2):
                cluster_list.append(gene_name2)
            elif break_judgment(gff_file_list, len_per_gene, gene_name1, gene_name2) == False and len(cluster_list) >=5:
                cluster_start = cluster_list[0]
                cluster_end = cluster_list[-1]
                cluster_start_num = gene_locus(gff_file_list,cluster_start)[1]
                cluster_end_num = gene_locus(gff_file_list,cluster_end)[1]
                seq_id = gene_locus(gff_file_list,cluster_end)[0]

                print "Predicted gene cluster", str(cluster_num) ,": " ,cluster_start, "\tto\t" , cluster_end,"\t(", seq_id,":" ,cluster_start_num, "--",cluster_end_num,")\tGene number of cluster: ",int(len(cluster_list))
                cluster_faa_list = get_faa_id(cluster_start, cluster_end, gff_file_list)
                out_file = "Predicted_gene_cluster_No" + str(cluster_num) + ".faa"
                for seq_id in cluster_faa_list:
                    Extract_seq_all(faa_file,seq_id,out_file)
                cluster_list  = []
                cluster_num += 1
            else:
                cluster_list = [gene_name2]




#Bin_dir = os.path.abspath(sys.argv[0])

in_file = "G:\\py_project\\OKCP\\test\\O_blastout.m6"
gff_file = "G:\\py_project\\OKCP\\test\\RA-CH-2.gff"
faa_file = "G:\\py_project\\OKCP\\test\\RA-CH-2.faa"

if __name__=='__main__':
    try:
        in_file = sys.argv[1]
        gff_file = sys.argv[2]
        faa_file = sys.argv[3]
    except:
        print __doc__
        sys.exit(-1)
    read_m6_2_list(in_file, gff_file,faa_file)