#! /usr/bin/python
import os

f_in = open("/user/gfasanel/Mass_resolution_study/jobs.dat","r")
#f_in = open("Extra_sigma/data_files/test.dat","r")
files=f_in.readlines()
for job in files:
    job=job.strip() #strip() is needed to remove leading and ending spaces
    #print job
    os.system("qdel "+str(job))

