##########################################################################################
##########################################################################################
# Giuseppe Fasanella (ULB)                                                               #
# Contact: aidan.randleconde@gmail.com, giuseppe.fasanella@cern.ch                       #
# Github:                                 #
##########################################################################################

import math

##########################################################################################
#                                  Settings for the job                                  #
##########################################################################################

##########################################################################################
#                             Import ROOT and apply settings                             #
##########################################################################################
import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)


##########################################################################################
#                                 Fitting histograms                                     #
##########################################################################################

file_mass= ROOT.TFile('~gfasanel/public/HEEP/Eff_plots/histograms_mass_res.root','READ')
file_mass_fit= ROOT.TFile('~gfasanel/public/HEEP/Eff_plots/histograms_mass_res_fit.root','RECREATE')

file_res_BB = open('/user/gfasanel/public/HEEP/Eff_plots/histograms_mass_res_BB.txt','w+') #if you use ~gfasanel it doesn't work
file_res_BE = open('/user/gfasanel/public/HEEP/Eff_plots/histograms_mass_res_BE.txt','w+') #if you use ~gfasanel it doesn't work
file_res_EE = open('/user/gfasanel/public/HEEP/Eff_plots/histograms_mass_res_EE.txt','w+') #if you use ~gfasanel it doesn't work

file_scale_BB = open('/user/gfasanel/public/HEEP/Eff_plots/histograms_mass_scale_BB.txt','w+') #if you use ~gfasanel it doesn't work
file_scale_BE = open('/user/gfasanel/public/HEEP/Eff_plots/histograms_mass_scale_BE.txt','w+') #if you use ~gfasanel it doesn't work
file_scale_EE = open('/user/gfasanel/public/HEEP/Eff_plots/histograms_mass_scale_EE.txt','w+') #if you use ~gfasanel it doesn't work

hBase_mee_mr = file_mass.Get('hBase_mee_mr') #Taken from the file, binning decided in histos_.py

for regions in ['BB','BE','EE']:
    for i in range(1, hBase_mee_mr.GetNbinsX()+1):# for each mass bin
        file_mass_fit.cd()
        hist_res = file_mass.Get(str('h_resolution_'+regions+'_%d'%i))
        if(hist_res.GetMaximum()<=5):
            hist_res.Rebin(2)
        #Do it with crystal ball (maybe two)
        fit_function=ROOT.TF1("fit_function","gaus",-0.03,0.03);
        hist_res .Fit("fit_function","RL") #R means range; L : minimization with likelihood function
        hist_res.Write()

        fit_function_scale=ROOT.TF1("fit_function_scale","gaus",0.97,1.03);
        hist_scale = file_mass.Get(str('h_scale_'+regions+'_%d'%i))
        hist_scale .Fit("fit_function_scale","RL")
        hist_scale.Write()

        ####Write on a file the fitted parameters#####
        if hist_res.GetFunction("fit_function")!= None: #In case bin empty or no fit available
            if regions=='BB':
                file_res_BB.write("%lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hist_res.GetFunction("fit_function").GetParameter(2), hist_res.GetFunction("fit_function").GetParError(2)))
            elif regions=='BE':
                #if hist_res.Integral()>40:
                file_res_BE.write("%lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hist_res.GetFunction("fit_function").GetParameter(2), hist_res.GetFunction("fit_function").GetParError(2)))
            elif regions=='EE':
                #if hist_res.Integral()>40:
                file_res_EE.write("%lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hist_res.GetFunction("fit_function").GetParameter(2), hist_res.GetFunction("fit_function").GetParError(2)))


        if hist_scale.GetFunction("fit_function_scale")!= None: #In case bin empty or no fit available. For the scale I want the mean of the gaussian
            if regions=='BB':
                file_scale_BB.write("%lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hist_scale.GetFunction("fit_function_scale").GetParameter(1), hist_scale.GetFunction("fit_function_scale").GetParError(1)))
            elif regions=='BE':                                                                                                                                                
                file_scale_BE.write("%lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hist_scale.GetFunction("fit_function_scale").GetParameter(1), hist_scale.GetFunction("fit_function_scale").GetParError(1)))
            elif regions=='EE':                                                                                                                                                
                file_scale_EE.write("%lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hist_scale.GetFunction("fit_function_scale").GetParameter(1), hist_scale.GetFunction("fit_function_scale").GetParError(1)))



file_mass.Close()
file_mass_fit.Close()

