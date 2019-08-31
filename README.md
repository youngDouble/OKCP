 ![OKCP](https://github.com/youngDouble/OKCP/blob/master/okcp.png "OKCP")  
 OKCP (O antigen &amp; K antigen gene cluster prediction) is used to predict the O antigen, K antigen gene cluster on the bacterial genome.      
 O&K-antigen synthesis gene cluster annotation pipeline    
                                                            
  Author: Zhishuang Yang                                    
  E-mail: yangzs_chi@yeah.net                               
  Version: 1.0.0                                            

Description:
 *OKCP is used to annotate genomic proteins to the O&K antigen database.
 
**Requirements:**  
  *python (>= 2.7.9) https://www.python.org  
  *blast+ (>= 2.6.0) ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/  
  *HMMER3 (>= 3.2.1) http://hmmer.org/  
  *Tmhmm2 http://www.cbs.dtu.dk/cgi-bin/nph-sw_request?tmhmm   
  
 *Python packages :*  
  *Biopython (>=1.71) https://biopython.org/wiki/Download  

**Install**  
 `git clone https://github.com/youngDouble/OKCP.git` //bash

Usage:  
```
OKCP.py  -gb gbk_file  -bT blast_thread hmm_db -hT hmm_thread  
ARGUMENTS:  
  -gb gbk_file  
  -bT blast_thread  
  -HMM hmm_db  
  -hT hmm_thread  
 OPTIONAL:  

```
