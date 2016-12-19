#! /usr/bin/python
import math
from array import array
import ROOT
import os
from HEEP_sel_60 import *

#run with python histos_for_sigma_extra_newID.py
##########################################################################################
tree_MC   = ROOT.TChain("IIHEAnalysis")
samples_path='/pnfs/iihe/cms/store/user/rgoldouz/RunIISpring16DR80/DYToEE_NNPDF30_13TeV-powheg-pythia8/crab_DYToEE_NNPDF30_13TeV-powheg-pythia8/160712_190134/'
label_MC='0'
samples=['0000']

for sample in samples:
    #print str(samples_path+sample+"/")
    for file in os.listdir(str(samples_path+sample+"/")):
        if file.endswith(".root"):
            tree_MC.Add(str(samples_path+sample+"/"+file))

tree_data = ROOT.TChain("IIHEAnalysis")
label_data='runD_20July'
path_data='/group/HEEP/Golden_2016_1290/DoubleEG_Run2016D_PromptReco_v2_AOD/'

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

#var_type=['data','MC']
var_type=['data']
#var_type=['MC']
for var in var_type:
	detector_regions=['BB','BE','EE','BEplus','BEminus']
	for regions in detector_regions:
	    h_mee_MC[regions]   = hBase_mee.Clone('h_mee_MC_%s'%regions)
	    h_mee_data[regions] = hBase_mee.Clone('h_mee_data_%s'%regions)
            h_mee_MC[regions].Sumw2()            
            h_mee_data[regions].Sumw2()
	
	if var in ['MC']:
	    tree=tree_MC
	else:
	    tree=tree_data

	#nEntries=tree.GetEntries()
	nEntries=10000 # just for quick tests
	for iEntry in range(0,nEntries):
	    if iEntry%1000==0:
	        print iEntry , '/' , nEntries
	    tree.GetEntry(iEntry)
            if var in ['data'] and tree.ev_run < 273725: #Do not use runs before this one (dEtaIn cut for EE is broken)
                continue
	    temp_mass=-999
	    index=-10
	
	    for i in range(0,len(tree.Zee_mass_HEEP)):
                Z_leg_index_1=tree.Zee_i1[i]
                Z_leg_index_2=tree.Zee_i2[i]
                if len(tree.gsf_isEB) < (max(Z_leg_index_1,Z_leg_index_2) + 1) or len(tree.gsf_isEE) < (max(Z_leg_index_1,Z_leg_index_2) + 1): 
                    #there are 2 entries in which gsf_isEB is not filled with the leg index (why?)
                    continue
                #print "Z 1", Z_leg_index_1
                #print "Z 2", Z_leg_index_2
                #print "len isEB", len(tree.gsf_isEB)
                #print "len isEE", len(tree.gsf_isEE)
                
                pass_sel_1=HEEP_ID_60(tree,Z_leg_index_1)
                pass_sel_2=HEEP_ID_60(tree,Z_leg_index_2)

                if(pass_sel_1 and pass_sel_2):
                    if(temp_mass<tree.Zee_mass_HEEP[i]):
                        temp_mass=tree.Zee_mass_HEEP[i]
                        index=i
	
	    if (index > -10):
	        barrel_barrel=(abs(tree.gsf_superClusterEta[tree.Zee_i1[index]])<1.4442) * (abs(tree.gsf_superClusterEta[tree.Zee_i2[index]])<1.4442)
	
	        barrel_endcap=(abs(tree.gsf_superClusterEta[tree.Zee_i1[index]])<1.4442) * (abs(tree.gsf_superClusterEta[tree.Zee_i2[index]])>1.566) * (abs(tree.gsf_superClusterEta[tree.Zee_i2[index]])<2.5) + (abs(tree.gsf_superClusterEta[tree.Zee_i2[index]])<1.4442) * (abs(tree.gsf_superClusterEta[tree.Zee_i1[index]])>1.566) * (abs(tree.gsf_superClusterEta[tree.Zee_i1[index]])<2.5)
	
	        barrel_endcap_plus=(abs(tree.gsf_superClusterEta[tree.Zee_i1[index]])<1.4442) * (tree.gsf_superClusterEta[tree.Zee_i2[index]]>1.566) * (tree.gsf_superClusterEta[tree.Zee_i2[index]]<2.5) + (abs(tree.gsf_superClusterEta[tree.Zee_i2[index]])<1.4442) * (tree.gsf_superClusterEta[tree.Zee_i1[index]]>1.566) * (tree.gsf_superClusterEta[tree.Zee_i1[index]]<2.5)
	
	        endcap_endcap=(abs(tree.gsf_superClusterEta[tree.Zee_i1[index]])>1.566) * (abs(tree.gsf_superClusterEta[tree.Zee_i1[index]])<2.5) * (abs(tree.gsf_superClusterEta[tree.Zee_i2[index]])>1.566) * (abs(tree.gsf_superClusterEta[tree.Zee_i2[index]])<2.5)
	
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
	    file_MC= ROOT.TFile('Extra_sigma/MC_Zpeak_2016_'+label_MC+'.root','RECREATE')
	    file_MC.cd()
	    for regions in detector_regions:
	        h_mee_MC[regions]. Write()
	else:
	    file_data= ROOT.TFile('Extra_sigma/data_Zpeak_2016_'+label_data+'.root','RECREATE')
	    file_data.cd()
	    for regions in detector_regions:
	        h_mee_data[regions]. Write()
