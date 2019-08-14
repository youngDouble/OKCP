import sys,os

print (os.path.abspath(sys.argv[0]))
Bin_dir = os.path.abspath(sys.argv[0])
DB_dir = os.path.join(Bin_dir.split("bin")[0],"DB")
print DB_dir