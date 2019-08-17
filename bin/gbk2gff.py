#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
####################################################################################################
Author:yangzhushuang  
E-mail:yangzs_chi@yeah.net
Edited by Yang Zhishuang at 2018/01/18
The latest version was edited at : 2018/01/18 By:yangzs 
####################################################################################################
Description:

    This shellscript  is used to convert genbank to gff.

    Requirement:
    BCBio   https://biopython.org/wiki/GFF_Parsing
    Biopython   https://biopython.org
Usage:
    gbk2gff.py path/to/in_gbk.gbk  path/to/out_gff.gff

    """
import sys
from Bio import SeqIO
from BCBio import GFF

def gbk2gff(in_file,out_file):
    """
    Converting data from genbank to GFF
    """
    in_handle = open(in_file)
    out_handle = open(out_file, "w")
    GFF.write(SeqIO.parse(in_handle, "genbank"), out_handle)
    in_handle.close()
    out_handle.close()

if __name__=='__main__':
    try:
        in_file = sys.argv[1]
        out_file =sys.argv[2]
    except:
        print __doc__
        sys.exit(-1)
    gbk2gff(in_file, out_file)