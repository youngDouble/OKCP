#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
####################################################################################################
Author:yangzhushuang
E-mail:yangzs_chi@yeah.net
Edited by Yang Zhishuang at 2019/09/18
The latest version was edited at : 2019/08/18 By:yangzs
####################################################################################################

Description:

    This shellscript  is used to convert genbank to faa.

    Requirement:
    Biopython   https://biopython.org

Usage:
    gbk2faa.py path/to/gbk_file.gbk

    """
from Bio import GenBank
from Bio import SeqIO
import sys ,os 

def gb2faa(gbk_filename, faa_filename):
    input_handle = open(gbk_filename, "r")
    output_handle = open(faa_filename, "w")
    sys.stdout.write("Dealing with GenBank record:\n")
    for seq_record in SeqIO.parse(input_handle, "genbank"):
        #sys.stdout.write(' ' * (28+len(seq_record.id)) + '\r')  # Avoid excessive long line retention
        #sys.stdout.flush()  # Avoid excessive long line retention
        sys.stdout.write("\t%s \n" % seq_record.id)
        #sys.stdout.flush()
        for seq_feature in seq_record.features:
            try:  # Without "try", it crashes when it finds a CDS without translation (pseudogene).
                if seq_feature.type == "CDS":
                    assert len(seq_feature.qualifiers['translation']) == 1
                    output_handle.write(">%s %s %s %s\n%s\n" % (
                        seq_feature.qualifiers['locus_tag'][0],
                        seq_feature.qualifiers['product'][0],
                        seq_record.id,
                        seq_record.description,
                        seq_feature.qualifiers['translation'][0]))
                    pass
            except:
                continue

    output_handle.close()
    input_handle.close()


if __name__=='__main__':
    try:
        gbk_filename = sys.argv[1]
        faa_filename = "%s_out.faa" % os.path.split(gbk_filename)[1]
    except:
        print __doc__
        sys.exit(-1)
    gb2faa(gbk_filename, faa_filename)
