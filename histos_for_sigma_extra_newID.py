#! /usr/bin/python
import math
from array import array
import ROOT
import os
from HEEP_sel_60 import *

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

for file in os.listdir(str("/pnfs/iihe/cms/store/user/wenxing/DoubleEG/crab_DoubleEG_Run2016B-PromptReco-v2_AOD_0520_golden/160520_173946/0000/")):
    if file.endswith(".root"):
        tree_data.Add(str("/pnfs/iihe/cms/store/user/wenxing/DoubleEG/crab_DoubleEG_Run2016B-PromptReco-v2_AOD_0520_golden/160520_173946/0000/"+file))


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

var_type=['data','MC']
for var in var_type:
	detector_regions=['BB','BE','EE','BEplus','BEminus']
	for regions in detector_regions:
	    h_mee_MC[regions]   = hBase_mee.Clone('h_mee_MC_%s'%regions)
	    h_mee_data[regions] = hBase_mee.Clone('h_mee_data_%s'%regions)
            h_mee_MC[regions].Sumw2()            
            h_mee_data[regions].Sumw2()

        #Define the HEEP selection by hand
	
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
	    temp_mass=-999
	    index=-10
	
	    for i in range(0,len(tree.Zee_mass_HEEP)):
	        #if (tree.HEEP_cutflow60_total[tree.Zee_i1[i]] and tree.HEEP_cutflow60_total[tree.Zee_i2[i]]): #if both electrons passes the full HEEP
#abs(gsf_superClusterEta)<1.442 or (abs(gsf_superClusterEta)>1.566 and abs(gsf_superClusterEta)<2.5)
                Z_leg_index_1=tree.Zee_i1[i]
                Z_leg_index_2=tree.Zee_i2[i]
                pass_sel_1=HEEP_ID_60(tree,Z_leg_index_1)
                pass_sel_2=HEEP_ID_60(tree,Z_leg_index_2)
#                if(tree.gsf_isEB[Z_leg_index]):
#                    pass_sel_1=(tree.gsf_pt[Z_leg_index]>35)*\
#                        (tree.gsf_ecaldrivenSeed[Z_leg_index]==1)*\
#                        (abs(tree.gsf_deltaEtaSeedClusterTrackAtCalo[Z_leg_index])<0.004)*\
#                        (abs(tree.gsf_deltaPhiSeedClusterTrackAtCalo[Z_leg_index])<0.06)*\
#                        (tree.gsf_hadronicOverEm[Z_leg_index] < (1./tree.gsf_caloEnergy[Z_leg_index] + 0.05))*\
#                        (tree.gsf_scE2x5Max[Z_leg_index]/tree.gsf_scE5x5[Z_leg_index] > 0.94 or tree.gsf_scE1x5[Z_leg_index]/tree.gsf_scE5x5[Z_leg_index] > 0.83 )*\
#                        (tree.gsf_hcalDepth1OverEcal[Z_leg_index] < 2 +0.03*tree.gsf_pt[Z_leg_index] + 0.28*tree.ev_fixedGridRhoFastjetAll)*\
#                        (tree.gsf_nLostInnerHits[Z_leg_index]<2)*\
#                        (abs(tree.gsf_dxy[Z_leg_index])<0.02)
#
#
#                elif(tree.gsf_isEE[Z_leg_index]):
#                    pass_sel_1=(tree.gsf_pt[Z_leg_index]>35)*\
#                        (tree.gsf_ecaldrivenSeed[Z_leg_index]==1)*\
#                        (abs(tree.gsf_deltaEtaSeedClusterTrackAtCalo[Z_leg_index])<0.006)*\
#                        (abs(tree.gsf_deltaPhiSeedClusterTrackAtCalo[Z_leg_index])<0.06)
#
#                Z_leg_index=tree.Zee_i2[i]
#                if(tree.gsf_isEB[Z_leg_index]):
#                    pass_sel_2=(tree.gsf_pt[Z_leg_index]>35)*\
#                        (tree.gsf_ecaldrivenSeed[Z_leg_index]==1)*\
#                        (abs(tree.gsf_deltaEtaSeedClusterTrackAtCalo[Z_leg_index])<0.004)*\
#                        (abs(tree.gsf_deltaPhiSeedClusterTrackAtCalo[Z_leg_index])<0.06)*\
#                        (tree.gsf_hadronicOverEm[Z_leg_index] < (1./tree.gsf_caloEnergy[Z_leg_index] + 0.05))*\
#                        (tree.gsf_scE2x5Max[Z_leg_index]/tree.gsf_scE5x5[Z_leg_index] > 0.94 or tree.gsf_scE1x5[Z_leg_index]/tree.gsf_scE5x5[Z_leg_index] > 0.83 )*\
#                        (tree.gsf_hcalDepth1OverEcal[Z_leg_index] < 2 +0.03*tree.gsf_pt[Z_leg_index] + 0.28*tree.ev_fixedGridRhoFastjetAll)*\
#                        (abs(tree.gsf_dxy[Z_leg_index])<0.02)
#                        #(tree.gsf_nLostInnerHits[Z_leg_index]<2)*\
#
#                elif(tree.gsf_isEE[Z_leg_index]):
#                    pass_sel_2=(tree.gsf_pt[Z_leg_index]>35)*\
#                        (tree.gsf_ecaldrivenSeed[Z_leg_index]==1)*\
#                        (abs(tree.gsf_deltaEtaSeedClusterTrackAtCalo[Z_leg_index])<0.006)*\
#                        (abs(tree.gsf_deltaPhiSeedClusterTrackAtCalo[Z_leg_index])<0.06)
                    


#                if(tree.gsf_isEB[tree.Zee_i1[i]]):
#                    pass_sel_1=(tree.gsf_pt[tree.Zee_i1[i]]>35)*(tree.gsf_ecaldrivenSeed[tree.Zee_i1[i]]==1)*(abs(tree.gsf_deltaEtaSeedClusterTrackAtCalo[tree.Zee_i1[i]])<0.004)*(abs(tree.gsf_deltaPhiSeedClusterTrackAtCalo[tree.Zee_i1[i]])<0.06)*(tree.gsf_hadronicOverEm[tree.Zee_i1[i]] < (1./tree.gsf_caloEnergy[tree.Zee_i1[i]] + 0.05))*(tree.gsf_scE2x5Max[tree.Zee_i1[i]]/tree.gsf_scE5x5[tree.Zee_i1[i]] > 0.94 or tree.gsf_scE1x5[tree.Zee_i1[i]]/tree.gsf_scE5x5[tree.Zee_i1[i]] > 0.83 )*(gsf_hcalDepth1OverEcal[tree.Zee_i1[i]] < 2 +0.03*tree.gsf_pt[tree.Zee_i1[i]] + 0.28*tree.ev_fixedGridRhoFastjetAll[tree.Zee_i1[i]])*(tree.gsf_nLostInnerHits[tree.Zee_i1[i]]<2)*(abs(tree.gsf_dxy[tree.Zee_i1[i]]<0.02))
#                elif(tree.gsf_isEE[tree.Zee_i1[i]]):
#                    pass_sel_1=(tree.gsf_pt[tree.Zee_i1[i]]>35)*(tree.gsf_ecaldrivenSeed[tree.Zee_i1[i]]==1)*(abs(tree.gsf_deltaEtaSeedClusterTrackAtCalo[tree.Zee_i1[i]])<0.006)*(abs(tree.gsf_deltaPhiSeedClusterTrackAtCalo[tree.Zee_i1[i]])<0.06)

#                if(tree.gsf_isEB[tree.Zee_i2[i]]):
#                    pass_sel_2=(tree.gsf_pt[tree.Zee_i2[i]]>35)*(tree.gsf_ecaldrivenSeed[tree.Zee_i2[i]]==1)*(abs(tree.gsf_deltaEtaSeedClusterTrackAtCalo[tree.Zee_i2[i]])<0.004)*(abs(tree.gsf_deltaPhiSeedClusterTrackAtCalo[tree.Zee_i2[i]])<0.06)
#                elif(tree.gsf_isEE[tree.Zee_i2[i]]):
#                    pass_sel_2=(tree.gsf_pt[tree.Zee_i2[i]]>35)*(tree.gsf_ecaldrivenSeed[tree.Zee_i2[i]]==1)*(abs(tree.gsf_deltaEtaSeedClusterTrackAtCalo[tree.Zee_i2[i]])<0.006)*(abs(tree.gsf_deltaPhiSeedClusterTrackAtCalo[tree.Zee_i2[i]])<0.06)

                #(tree.gsf_hadronicOverEm[tree.Zee_i1[i]]
                #tree.gsf_sigmaIetaIeta[tree.Zee_i1[i]]
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
	    file_MC= ROOT.TFile('Extra_sigma/MC_Zpeak_2016.root','RECREATE')
	    file_MC.cd()
	    for regions in detector_regions:
	        h_mee_MC[regions]. Write()
	else:
	    file_data= ROOT.TFile('Extra_sigma/data_Zpeak_2016.root','RECREATE')
	    file_data.cd()
	    for regions in detector_regions:
	        h_mee_data[regions]. Write()
