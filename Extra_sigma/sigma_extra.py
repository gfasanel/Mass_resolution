#! /usr/bin/python
import math
import ROOT

var_type=['data','MC']
det_regions=['BB','BE','EE']

mean       ={}
mean_error ={}
sigma      ={}
sigma_error={}
for var in var_type:
    mean[var]       ={}
    mean_error[var] ={}
    sigma[var]      ={}
    sigma_error[var]={}

for region in det_regions:
    for var in var_type:
        with open(str('fit_extra_sigma_'+var+'_'+region+'.dat')) as file_res:
            for line in file_res:  #Line is a string 
                # split the string on whitespace, return a list of numbers as strings
                numbers_str = line.split()                               
                numbers_float = map(float, line.split())
                mean[var][region]       =numbers_float[0]
                mean_error[var][region] =numbers_float[1]
                sigma[var][region]      =numbers_float[2]
                sigma_error[var][region]=numbers_float[3]

for region in det_regions:
    print sigma['data'][region], sigma['MC'][region]
