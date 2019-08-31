#cp O-antigen_DB_from_NCBI_fasta_cds_aa.faa O-antigen_DB_from_NCBI_fasta_cds_aa.faa.b
perl -p -i -e 's/\>.+?\[gene=/\>/;s/\[/ /g;s/\]//g;s/lcl\|.+?_prot_(.+?) /$1/'  O-antigen_DB_from_NCBI_fasta_cds_aa.faa
makeblastdb  -in O-antigen_DB_from_NCBI_fasta_cds_aa.faa   -input_type fasta -dbtype prot  -out O-antigen_DB_from_NCBI_fasta_cds_aa

perl -p -i -e 's/\>.+?\[gene=/\>/;s/\[/ /g;s/\]//g;s/lcl\|.+?_prot_(.+?) /$1/'   K-antigen_DB_from_NCBI_fasta_cds_aa.faa
makeblastdb  -in K-antigen_DB_from_NCBI_fasta_cds_aa.faa  -input_type fasta -dbtype prot  -out K-antigen_DB_from_NCBI_fasta_cds_aa

