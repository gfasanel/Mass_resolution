#! /usr/bin/python
import math
import ROOT

print "[STATUS] Calling Mass_resolution/Extra_sigma/sigma_extra.py to write Latex table"

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
        with open(str('/user/gfasanel/HEEP/CMSSW_7_2_0_patch1/src/Mass_resolution/Extra_sigma/fit_extra_sigma_'+var+'_'+region+'.dat')) as file_res:
            for line in file_res:  #Line is a string 
                # split the string on whitespace, return a list of numbers as strings
                numbers_str = line.split()                               
                numbers_float = map(float, line.split())
                mean[var][region]       =numbers_float[0]
                mean_error[var][region] =numbers_float[1]
                sigma[var][region]      =numbers_float[2]
                sigma_error[var][region]=numbers_float[3]

latex_table      = open('/user/gfasanel/HEEP/CMSSW_7_2_0_patch1/src/Mass_resolution/Extra_sigma/latex_extra_sigma.tex','w+')
final_sigma_extra={}
for region in det_regions:
    final_sigma_extra[region]= open(str('/user/gfasanel/HEEP/CMSSW_7_2_0_patch1/src/Mass_resolution/Extra_sigma/final_extra_sigma_'+region+'.dat'),'w+')
    sigma_data        = sigma['data'][region]
    sigma_data_error  = sigma_error['data'][region]
    sigma_MC          = sigma['MC'][region]
    sigma_MC_error    = sigma_error['MC'][region]
    sigma_extra       = ROOT.sqrt(sigma['data'][region]*sigma['data'][region] - sigma['MC'][region]*sigma['MC'][region])
    sigma_extra_error = ROOT.sqrt(ROOT.pow(sigma_data*sigma_data_error/sigma_extra,2) + ROOT.pow(sigma_MC*sigma_MC_error/sigma_extra,2)) 
    latex_table.write("%s %lf %lf %lf %lf %lf %lf \n"%(region,sigma_data,sigma_data_error,sigma_MC,sigma_MC_error,sigma_extra,sigma_extra_error))
    final_sigma_extra[region].write("%lf %lf\n"%(sigma_extra,sigma_extra_error))
                       
