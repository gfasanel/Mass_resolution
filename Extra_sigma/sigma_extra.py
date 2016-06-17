#! /usr/bin/python
import math
import ROOT

print "[STATUS] Calling Mass_resolution/Extra_sigma/sigma_extra.py to write Latex table"

var_type=['data','MC']
#det_regions=['BB','BE','EE']
det_regions=['BB','BE']
mean       ={}
mean_error ={}
sigma      ={}
sigma_error={}
sigma_eff  ={}
for var in var_type:
    mean[var]       ={}
    mean_error[var] ={}
    sigma[var]      ={}
    sigma_error[var]={}
    sigma_eff[var]  ={}

for region in det_regions:
    for var in var_type:
        with open(str('/user/gfasanel/HEEP/CMSSW_7_2_0_patch1/src/Mass_resolution/Extra_sigma/fit_extra_sigma_2016_'+var+'_'+region+'.dat')) as file_res:
            for line in file_res:  #Line is a string 
                # split the string on whitespace, return a list of numbers as strings
                numbers_str = line.split()                               
                numbers_float = map(float, line.split())
                mean[var][region]       =numbers_float[0]
                mean_error[var][region] =numbers_float[1]
                sigma[var][region]      =numbers_float[2]
                sigma_error[var][region]=numbers_float[3]
                sigma_eff[var][region]  =numbers_float[4]

latex_table      = open('/user/gfasanel/HEEP/CMSSW_7_2_0_patch1/src/Mass_resolution/Extra_sigma/latex_extra_sigma_2016.tex','w+')
final_sigma_extra={}
#error: if Q=sqrt(a2 + b2), Error(Q)=sqrt( (a/Q)^2 * Err(a) + (b/Q)^2 * Err(b) )

latex_table.write("\\begin{table}[htb]\n")
latex_table.write("\\begin{center}\n")
latex_table.write("\\begin{tabular}{ccccccc}\n")
latex_table.write("\\hline\n")
latex_table.write("Category & $\sigma_{data}$ [\%] & $\sigma_{MC}$ [\%] & $\sigma_{extra}$ [\%] & $\sigma_{data}^{eff}$ [\%] & $\sigma_{MC}^{eff}$ [\%] & $\sigma_{extra}^{eff}$ [\%]\\\\ \hline\n")                                                                                   
#      BB & 1.77 & 1.32 & 1.171 \\
#      BE & 2.84 & 2.27 & 1.699\\
#      EE & 3.25 & 2.0  & 2.504\\

print "File is /user/gfasanel/HEEP/CMSSW_7_2_0_patch1/src/Mass_resolution/Extra_sigma/latex_extra_sigma_2016.tex"

for region in det_regions:
    #print "File is ",str('/user/gfasanel/HEEP/CMSSW_7_2_0_patch1/src/Mass_resolution/Extra_sigma/final_extra_sigma_2016_'+region+'.dat')
    final_sigma_extra[region]= open(str('/user/gfasanel/HEEP/CMSSW_7_2_0_patch1/src/Mass_resolution/Extra_sigma/final_extra_sigma_2016_'+region+'.dat'),'w+')
    sigma_data        = sigma['data'][region]
    sigma_data_error  = sigma_error['data'][region]
    sigma_MC          = sigma['MC'][region]
    sigma_MC_error    = sigma_error['MC'][region]
    sigma_extra       = ROOT.sqrt(sigma['data'][region]*sigma['data'][region] - sigma['MC'][region]*sigma['MC'][region])
    sigma_extra_error = ROOT.sqrt(ROOT.pow(sigma_data*sigma_data_error/sigma_extra,2) + ROOT.pow(sigma_MC*sigma_MC_error/sigma_extra,2)) 
    sigma_eff_final   = ROOT.sqrt(sigma_eff['data'][region]*sigma_eff['data'][region] - sigma_eff['MC'][region]*sigma_eff['MC'][region])
    final_sigma_extra[region].write("%lf %lf %lf %lf %lf\n"%(sigma_extra,sigma_extra_error,sigma_eff['data'][region],sigma_eff['MC'][region],sigma_eff_final))

    latex_table.write("%s %s %.2lf %s %.2lf %s %.2lf %s %.2lf %s %.2lf %s %.2lf %s %.2lf %s %.2lf %s %.2lf %s\n"
                      %(region,"&",sigma_data*100.,"$\pm$", sigma_data_error*100.,"&",sigma_MC*100.,"$\pm$",sigma_MC_error*100.,"&",sigma_extra*100.,"$\pm$",sigma_extra_error*100.,"&",sigma_eff['data'][region]*100,"&",sigma_eff['MC'][region]*100,"&",sigma_eff_final*100,"\\\\"))


latex_table.write("\\hline\n")
latex_table.write("\\end{tabular}\n")
latex_table.write("\\caption{Results per category for the $\sigma_{extra}$ parameter. \label{tab:extra}} \n")
latex_table.write("\\end{center}\n")
latex_table.write("\\end{table}\n")                       
