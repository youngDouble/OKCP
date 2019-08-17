#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
####################################################################################################
Author:yangzhushuang
E-mail:yangzs_chi@yeah.net
Edited by Yang Zhishuang at 2019/08/17
The latest version was edited at : 2019/08/17 By:yangzs
####################################################################################################
Description:

    This script  is used to predict the number of transmembrane areas by TMHMM

    Requirement:
	tmhmm    http://www.cbs.dtu.dk/cgi-bin/nph-sw_request?tmhmm


Usage:
    tmhmm_Parse.py path/to/faa_file.faa

    """
import sys , os,time,shutil ,subprocess


def check_sys_cmd():
    if os.system('which tmhmm >/dev/null 2>&1') != 0:
        print 'tmhmm: command not found\nDownload and install tmhmm from http://www.cbs.dtu.dk/cgi-bin/nph-sw_request?tmhmm . And add tmhmm to the PATH'
        sys.exit()
def tmh_num(faa_file):
    """Return the number of transmembrane areas"""
    command1 = "tmhmm " +   faa_file +  " | grep 'Number of predicted TMHs' "
    proc1 = subprocess.Popen(command1, stdout=subprocess.PIPE, shell=True)
    stout=proc1.stdout.read()
    stout_list = stout.split('\n')

    for result in stout_list[:-1]:
        protein_id  = result.split(' ')[1]
        tmh_num = int(result.split(' ')[-1])
        if tmh_num >=  7:
            report_line = protein_id + '\tNumber of predicted TMHs:\t' +str(tmh_num)
            print report_line
    proc2 = subprocess.check_call("rm -r TMHMM_* ", stdout=subprocess.PIPE, shell=True)
if __name__=='__main__':
    try:
        in_file = sys.argv[1]
        check_sys_cmd()
        tmh_num(in_file)
    except:
        print __doc__
        sys.exit(-1)

