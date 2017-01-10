#! /usr/bin/python
import math
from array import array
import ROOT
import os

#run with python histos_for_sigma_extra.py
##########################################################################################
tree_MC   = ROOT.TChain("IIHEAnalysis")
#samples_path='/user/aidan/public/HEEP/samples/RunIISpring15DR74/'
#samples=['RunIISpring15DR74_ZToEE_NNPDF30_13TeV-powheg_50_120']#,
samples_path='/pnfs/iihe/cms/store/user/wenxing/ZToEE_NNPDF30_13TeV-powheg_M_50_120/crab_ZToEE_NNPDF30_13TeV-powheg_M_50_120_RunIISpring16DR80/160517_090136/0000/'
samples=['']

for sample in samples:
    #print str(samples_path+sample+"/")
    for file in os.listdir(str(samples_path+sample+"/")):
        if file.endswith(".root"):
            tree_MC.Add(str(samples_path+sample+"/"+file))

tree_data = ROOT.TChain("IIHEAnalysis")
#str("/pnfs/iihe/cms/store/user/wenxing/DoubleEG/crab_DoubleEG_Run2016B-PromptReco-v2_AOD_0520_golden/160520_173946/0000/")
path_data='/group/HEEP/Golden_2016/DoubleEG_Run2016B_PromptReco_v2_AOD/'
for file in os.listdir(path_data):
    if file.endswith(".root"):
        tree_data.Add(str(path_data+file))


##########################################################################################
#                                 Declare and fill histograms
##########################################################################################
hBase_mee = ROOT.TH1F('hBase_mee', '', 400, 0, 200)#Normally, we fit from 60-120
hBase_mee.GetXaxis().SetTitle('m(ee) [GeV]')
hBase_mee.GetYaxis().SetTitle('entries per 1 GeV')

h_mee_MC   = {}
h_mee_data = {}

print "data entries ",tree_data.GetEntries()
print "MC entries ",tree_MC.GetEntries()
#var_type=['MC','data']
var_type=['data']

for var in var_type:
	detector_regions=['BB','BE','EE','BEplus','BEminus']
	for regions in detector_regions:
	    h_mee_MC[regions]   = hBase_mee.Clone('h_mee_MC_%s'%regions)
	    h_mee_data[regions] = hBase_mee.Clone('h_mee_data_%s'%regions)
            h_mee_MC[regions].Sumw2()            
            h_mee_data[regions].Sumw2()
	#HEEP_cutflow60_acceptance is true for a gsf that passes the Et and eta requirements.
	#HEEP_cutflow60_ID is true for a gsf electron that passes the acceptance and ID.
	#HEEP_cutflow60_total is true for a gsf electrons that passes all cuts.
	
	if var in ['MC']:
	    tree=tree_MC
	else:
	    tree=tree_data
	
	nEntries=tree.GetEntries()
	#nEntries=10000 # just for quick tests
	for iEntry in range(0,nEntries):
	    if iEntry%1000==0:
	        print iEntry , '/' , nEntries
	    tree.GetEntry(iEntry)
	    temp_mass=-999
	    index=-10
	
	    for i in range(0,len(tree.Zee_mass_HEEP)):
	        if (tree.HEEP_cutflow60_total[tree.Zee_i1[i]] and tree.HEEP_cutflow60_total[tree.Zee_i2[i]]): #if both electrons passes the full HEEP
	            if(temp_mass<tree.Zee_mass_HEEP[i]):
	                temp_mass=tree.Zee_mass_HEEP[i]
	                index=i
	
	    if (index > -10):
	        barrel_barrel=(abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i1[index]])<1.4442) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i2[index]])<1.4442)
	
	        barrel_endcap=(abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i1[index]])<1.4442) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i2[index]])>1.566) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i2[index]])<2.5) + (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i2[index]])<1.4442) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i1[index]])>1.566) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i1[index]])<2.5)
	
	        barrel_endcap_plus=(abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i1[index]])<1.4442) * (tree.HEEP_cutflow60_eta_value[tree.Zee_i2[index]]>1.566) * (tree.HEEP_cutflow60_eta_value[tree.Zee_i2[index]]<2.5) + (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i2[index]])<1.4442) * (tree.HEEP_cutflow60_eta_value[tree.Zee_i1[index]]>1.566) * (tree.HEEP_cutflow60_eta_value[tree.Zee_i1[index]]<2.5)
	
	        endcap_endcap=(abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i1[index]])>1.566) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i1[index]])<2.5) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i2[index]])>1.566) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i2[index]])<2.5)
	
	        if barrel_barrel:
	            if var in ['MC']:
	                h_mee_MC['BB'].Fill(tree.Zee_mass_HEEP[index],barrel_barrel)
	            else:
	                h_mee_data['BB'].Fill(tree.Zee_mass_HEEP[index],barrel_barrel)
	        if barrel_endcap:
	            if var in ['MC']:
	                h_mee_MC['BE'].Fill(tree.Zee_mass_HEEP[index],barrel_endcap)            
	                if barrel_endcap_plus:
	                    h_mee_MC['BEplus'].Fill(tree.Zee_mass_HEEP[index])            
	                else:
	                    h_mee_MC['BEminus'].Fill(tree.Zee_mass_HEEP[index])
	            else:
	                h_mee_data['BE'].Fill(tree.Zee_mass_HEEP[index],barrel_endcap)            
	                if barrel_endcap_plus:
	                    h_mee_data['BEplus'].Fill(tree.Zee_mass_HEEP[index])            
	                else:
	                    h_mee_data['BEminus'].Fill(tree.Zee_mass_HEEP[index])
	        if endcap_endcap:
	            if var in ['MC']:
	                h_mee_MC['EE'].Fill(tree.Zee_mass_HEEP[index],endcap_endcap)
	            else:
	                h_mee_data['EE'].Fill(tree.Zee_mass_HEEP[index],endcap_endcap)
	
	if var in ['MC']:
	    file_MC= ROOT.TFile('Extra_sigma/MC_Zpeak_2016.root','RECREATE')
	    file_MC.cd()
	    for regions in detector_regions:
	        h_mee_MC[regions]. Write()
	else:
	    file_data= ROOT.TFile('Extra_sigma/data_Zpeak_2016.root','RECREATE')
	    file_data.cd()
	    for regions in detector_regions:
	        h_mee_data[regions]. Write()
