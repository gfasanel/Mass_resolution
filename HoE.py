#! /usr/bin/python
import math
import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE) 

###################Take the histograms#################

#file_mass=ROOT.TFile('~gfasanel/public/HEEP/Eff_plots/histograms_mass_res.root','READ')
file_mass=ROOT.TFile('Resolution/histograms_mass_res.root','READ')

HoE_types=['HoverE','HTotoverETot']

for HoE_type in HoE_types:
    file_res_BB = open(str('Resolution/histograms_mass_'+HoE_type+'_BB.txt'),'w+') 
    file_res_BE = open(str('Resolution/histograms_mass_'+HoE_type+'_BE.txt'),'w+') 
    file_res_EE = open(str('Resolution/histograms_mass_'+HoE_type+'_EE.txt'),'w+') 

    hBase_mee_mr = file_mass.Get('hBase_mee_mr') #Taken from the file, binning decided in histos_for_resolution.py

    for regions in ['BB','BE','EE']:
        for i in range(1, hBase_mee_mr.GetNbinsX()+1):# for each mass bin
            #print str('h_'+HoE_type+'_'+regions+'_%d'%i)
            hist   = file_mass.Get(str('h_'+HoE_type+'_'+regions+'_%d'%i))
            if regions=='BB':
                file_res_BB.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i),hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i),hist.GetMean(),hist.GetRMS()/math.sqrt(hist.GetSize()-2)))
                #the error on the mean is RMS/sqrt(N)
            elif regions=='BE':
                file_res_BE.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i),hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i),hist.GetMean(),hist.GetRMS()/math.sqrt(hist.GetSize()-2)))
            elif regions=='EE':
                file_res_EE.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i),hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i),hist.GetMean(),hist.GetRMS()/math.sqrt(hist.GetSize()-2)))


##Low, High Eta study
#HoE_types=['HoverE_lowEta','HTotoverETot_lowEta','HoverE_highEta','HTotoverETot_highEta']
#
#for HoE_type in HoE_types:
#    file_res_BB = open(str('Resolution/histograms_mass_'+HoE_type+'_BB.txt'),'w+') 
#    file_res_BE = open(str('Resolution/histograms_mass_'+HoE_type+'_BE.txt'),'w+') 
#    file_res_EE = open(str('Resolution/histograms_mass_'+HoE_type+'_EE.txt'),'w+') 
#
#    hBase_mee_mr = file_mass.Get('hBase_mee_mr') #Taken from the file, binning decided in histos_for_resolution.py
#
#    for regions in ['BB']:
#        for i in range(1, hBase_mee_mr.GetNbinsX()+1):
#            hist   = file_mass.Get(str('h_'+HoE_type+regions+'_%d'%i))
#            file_res_BB.write("%lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i),hist.GetMean(),hist.GetRMS()/math.sqrt(hist.GetSize()-2)))
#    for regions in ['BE']:
#            file_res_BE.write("%lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i),0,0))
#    for regions in ['EE']:
#            file_res_EE.write("%lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i),0,0))
#






