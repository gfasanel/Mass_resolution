#! /usr/bin/python
import math
from array import array
import ROOT
import os

#run with python histos_for_sigma_extra.py
##########################################################################################
tree      = ROOT.TChain("IIHEAnalysis")
for file in os.listdir("/user/aidan/public/HEEP/samples/RunIISpring15DR74/RunIISpring15DR74_DYToEE_50_25ns/"):
    if file.endswith(".root"):
        tree.Add(str("/user/aidan/public/HEEP/samples/RunIISpring15DR74/RunIISpring15DR74_DYToEE_50_25ns/"+file))

tree_data = ROOT.TChain("IIHEAnalysis")
tree_data.Add("~aidan/public/HEEP/data2015/DoubleEG_Run2015B_GoldenLumimask.root")
tree_data.Add("~aidan/public/HEEP/data2015/DoubleEG_Run2015C_GoldenLumimask.root")
tree_data.Add("~aidan/public/HEEP/data2015/DoubleEG_Run2015D_GoldenLumimask.root")

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

#HEEP_cutflow60_acceptance is true for a gsf that passes the Et and eta requirements.
#HEEP_cutflow60_ID is true for a gsf electron that passes the acceptance and ID.
#HEEP_cutflow60_total is true for a gsf electrons that passes all cuts.

###DY MC##########################################################
nEntries=tree.GetEntries()
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

        endcap_endcap=(abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i1[index]])>1.566) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i1[index]])<2.5) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i2[index]])>1.566) * (abs(tree.HEEP_cutflow60_eta_value[tree.Zee_i2[index]])<2.5)

        if barrel_barrel:
            h_mee_MC['BB'].Fill(tree.Zee_mass_HEEP[index],barrel_barrel)
        if barrel_endcap:
            h_mee_MC['BE'].Fill(tree.Zee_mass_HEEP[index],barrel_endcap)            
        if endcap_endcap:
            h_mee_MC['EE'].Fill(tree.Zee_mass_HEEP[index],endcap_endcap)

#####DATA###########################################
nEntries=tree_data.GetEntries()
for iEntry in range(0,nEntries):
    if iEntry%1000==0:
        print iEntry , '/' , nEntries
    tree_data.GetEntry(iEntry)
    temp_mass=-999
    index=-10

    for i in range(0,len(tree_data.Zee_mass_HEEP)):
        if (tree_data.HEEP_cutflow60_total[tree_data.Zee_i1[i]] and tree_data.HEEP_cutflow60_total[tree_data.Zee_i2[i]]): #if both electrons passes the full HEEP
            if(temp_mass<tree_data.Zee_mass_HEEP[i]):
                temp_mass=tree_data.Zee_mass_HEEP[i]
                index=i

    if (index > -10):
        barrel_barrel=(abs(tree_data.HEEP_cutflow60_eta_value[tree_data.Zee_i1[index]])<1.4442) * (abs(tree_data.HEEP_cutflow60_eta_value[tree_data.Zee_i2[index]])<1.4442)

        barrel_endcap=(abs(tree_data.HEEP_cutflow60_eta_value[tree_data.Zee_i1[index]])<1.4442) * (abs(tree_data.HEEP_cutflow60_eta_value[tree_data.Zee_i2[index]])>1.566) * (abs(tree_data.HEEP_cutflow60_eta_value[tree_data.Zee_i2[index]])<2.5) + (abs(tree_data.HEEP_cutflow60_eta_value[tree_data.Zee_i2[index]])<1.4442) * (abs(tree_data.HEEP_cutflow60_eta_value[tree_data.Zee_i1[index]])>1.566) * (abs(tree_data.HEEP_cutflow60_eta_value[tree_data.Zee_i1[index]])<2.5)

        endcap_endcap=(abs(tree_data.HEEP_cutflow60_eta_value[tree_data.Zee_i1[index]])>1.566) * (abs(tree_data.HEEP_cutflow60_eta_value[tree_data.Zee_i1[index]])<2.5) * (abs(tree_data.HEEP_cutflow60_eta_value[tree_data.Zee_i2[index]])>1.566) * (abs(tree_data.HEEP_cutflow60_eta_value[tree_data.Zee_i2[index]])<2.5)

        if barrel_barrel:
            h_mee_data['BB'].Fill(tree_data.Zee_mass_HEEP[index],barrel_barrel)
        if barrel_endcap:
            h_mee_data['BE'].Fill(tree_data.Zee_mass_HEEP[index],barrel_endcap)            
        if endcap_endcap:
            h_mee_data['EE'].Fill(tree_data.Zee_mass_HEEP[index],endcap_endcap)


file_mass= ROOT.TFile('test.root','RECREATE')
file_mass.cd()
for regions in ['BB','BE','EE']:
    h_mee_MC[regions]. Write()
    h_mee_data[regions]. Write()






