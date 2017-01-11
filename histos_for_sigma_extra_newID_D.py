#! /usr/bin/python
import math
from array import array
import ROOT
import os
from HEEP_sel_70 import *

#run with python histos_for_sigma_extra_newID.py
##########################################################################################
#tree_MC   = ROOT.TChain("IIHEAnalysis")
#samples_path='/pnfs/iihe/cms/store/user/wenxing/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_PUMoriond17_new/161207_094659/'
#label_MC='Moriond17'
##samples=['0000','0001','0002','0003','0004'] #-->maybe too many files for a chain
#samples=['0000']
#
#for sample in samples:
#    #print str(samples_path+sample+"/")
#    for file in os.listdir(str(samples_path+sample+"/")):
#        if file.endswith(".root"):
#            #print file
#            tree_MC.Add(str(samples_path+sample+"/"+file))

#################            DATA                        ################################

##########RUNB
tree_data = ROOT.TChain("IIHEAnalysis")
f_in = open("/user/gfasanel/Mass_resolution_study/Extra_sigma/data_files/data_files_runD_Moriond17.dat","r")
#f_in = open("Extra_sigma/data_files/test.dat","r")
files=f_in.readlines()
for file in files:
    tree_data.Add(file.strip())     #strip() is needed to remove leading and ending spaces

label_data='runD_Moriond17'


##########################################################################################
#                                 Declare and fill histograms
##########################################################################################
from optparse import OptionParser
parser=OptionParser()
parser.add_option("-i","--index",dest="index",default=0,type=int) #python parser option.py -i 0 => options.index is 0
(options,args)=parser.parse_args()

print "##################### STARTING TO NTUPLIZE #####################"
hBase_mee = ROOT.TH1F('hBase_mee', '', 400, 0, 200)#Normally, we fit from 60-120
hBase_mee.GetXaxis().SetTitle('m(ee) [GeV]')
hBase_mee.GetYaxis().SetTitle('entries per 1 GeV')

h_mee_MC   = {}
h_mee_data = {}

#GetEntries() is extremely slow, GetEntriesFast() does not work properly
#print "data entries ",tree_data.GetEntries()
#print "MC entries ",tree_MC.GetEntries()

#var_type=['data','MC']
var_type=['data']
#var_type=['MC']

for var in var_type:
	detector_regions=['BB','BE','EE','BEplus','BEminus']

        if var in ['MC']:
            tree=tree_MC
        else:
            tree=tree_data

        nEntries = tree.GetEntries()
        #nEntries = tree.GetEntriesFast() #not safe: I get 1234567890 (but yes, it's fast) !!!
        slot=2000000
        #slot=2000
        steps=nEntries/slot
        Ranges=[]
        for step in range(0,steps + 1):
            Ranges.append(step*slot)
        Ranges.append(nEntries)
        print "index max job is ", len(Ranges) -2
        print "You are running in range: ",Ranges[options.index], Ranges[options.index + 1]
	for regions in detector_regions:
	    h_mee_MC[regions]   = hBase_mee.Clone('h_mee_MC_%s'%regions)
	    h_mee_data[regions] = hBase_mee.Clone('h_mee_data_%s'%regions)
            h_mee_MC[regions].Sumw2()            
            h_mee_data[regions].Sumw2()

	#nEntries=10000 # just for quick tests
	#for iEntry in range(0,nEntries):
	for iEntry in range(Ranges[options.index],Ranges[options.index + 1]):
	    if iEntry%1000==0:
	        print iEntry , '/' , nEntries
	    tree.GetEntry(iEntry)
            #if var in ['data'] and tree.ev_run < 273725: #Do not use runs before this one (dEtaIn cut for EE was broken)
            #    continue
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
                
                pass_sel_1=HEEP_ID_70(tree,Z_leg_index_1)
                pass_sel_2=HEEP_ID_70(tree,Z_leg_index_2)

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
	    file_MC= ROOT.TFile('/user/gfasanel/Mass_resolution_study/Extra_sigma/Histos/MC_Zpeak_2016_'+label_MC+'_'+str(options.index)+'.root','RECREATE')
	    file_MC.cd()
	    for regions in detector_regions:
	        h_mee_MC[regions]. Write()
	else:
            #'+str(options.index)+'
	    file_data= ROOT.TFile('/user/gfasanel/Mass_resolution_study/Extra_sigma/Histos/data_Zpeak_2016_'+label_data+'_'+str(options.index)+'.root','RECREATE')
	    file_data.cd()
	    for regions in detector_regions:
	        h_mee_data[regions]. Write()
