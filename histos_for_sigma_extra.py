#! /usr/bin/python
import math
from array import array
sname = 'ZprimeToEE_M5000_20bx25'
import ROOT

##########
samples_path='/user/gfasanel/public/HEEP_samples/'
tree      = ROOT.TChain("IIHEAnalysis")
tree_data = ROOT.TChain("IIHEAnalysis")

tree.Add('/user/aidan/public/HEEP/samples/RunIISpring15DR74/RunIISpring15DR74_DYToEE_50_25ns/outfile_1.root')
#tree.Add(str(samples_path+'crab_20150128_PHYS14_DYToEEMM_120_200_20bx25__120_200/outfile_PHYS14_DYToEEMM_120_200_20bx25__120_200.root'))
#tree.Add(str('/user/gfasanel/public/HEEP_samples/crab_20150126_PHYS14_ZprimeToEE_M5000_20bx25/outfile_PHYS14_%s.root'%sname))

tree_data.Add('/user/aidan/public/HEEP/data2015/DoubleEG_Run2015D_GoldenLumimask.root')


##########################################################################################
#                                 Declare and fill histograms
##########################################################################################
hBase_mee = ROOT.TH1F('hBase_mee', '', 60, 60, 120)
hBase_mee.GetXaxis().SetTitle('m(ee) [GeV]')
hBase_mee.GetYaxis().SetTitle('entries per 1 GeV')

h_mee_MC   = {}
h_mee_data = {}
for regions in ['BB','BE','EE']:
    h_mee_MC[regions]   = hBase_mee.Clone('h_mee_MC_%s'%regions)
    h_mee_data[regions] = hBase_mee.Clone('h_mee_data_%s'%regions)

#nEntries = 1000
nEntries = tree.GetEntries()
nEventsWithEE = 0
region_fail_counter=0
nEventsWithEE=0
nEventsWithEEreco=0
nEventsWithNegMass=0


for iEntry in range(0,nEntries):
    if iEntry%1000==0:
        print iEntry , '/' , nEntries
    tree.GetEntry(iEntry)
    for i in range(0,len(tree.Zee_mass_HEEP)):
        if tree.HEEP_cutflow60_total[tree.Zee_i1[i]] and tree.HEEP_cutflow60_total[tree.Zee_i2[i]]: #if both electrons passes the full HEEP

            barrel_barrel=(abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i1[i]])<1.4442) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i2[i]])<1.4442)

            barrel_endcap=(abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i1[i]])<1.4442) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i2[i]])>1.566) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i2[i]])<2.5) + (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i2[i]])<1.4442) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i1[i]])>1.566) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i1[i]])<2.5)

            endcap_endcap=(abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i1[i]])>1.566) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i1[i]])<2.5) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i2[i]])>1.566) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i2[i]])<2.5)

            if barrel_barrel:
                h_mee_MC['BB'].Fill(tree.Zee_mass_HEEP[i],barrel_barrel)
            if barrel_endcap:
                h_mee_MC['BE'].Fill(tree.Zee_mass_HEEP[i],barrel_endcap)            
            if endcap_endcap:
                h_mee_MC['EE'].Fill(tree.Zee_mass_HEEP[i],endcap_endcap)

#HEEP_cutflow60_acceptance is true for a gsf that passes the Et and eta requirements.
#HEEP_cutflow60_ID is true for a gsf electron that passes the acceptance and ID.
#HEEP_cutflow60_total is true for a gsf electrons that passes all cuts.


file_mass= ROOT.TFile('test.root','RECREATE')
file_mass.cd()
for regions in ['BB','BE','EE']:
    h_mee_MC[regions]. Write()






