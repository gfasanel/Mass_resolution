#! /usr/bin/python
##########################################################################################
# HISTOGRAMS MAKER FOR HEEP RESOLUTION (MC only)#
##########################################################################################
# Giuseppe Fasanella (ULB)     
##########################################################################################
import math
from array import array
import os
import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)
from HEEP_sel_70_MC import *
#from HEEP_sel_70 import *

##########
#Since this is just for the mass resolution you don't need to reweight the histograms as long as you don't mix the binning
#https://twiki.cern.ch/twiki/bin/viewauth/CMS/IiheHeepAnalysis#RunIISpring16DR80_campaign_new_t
samples_path='/pnfs/iihe/cms/store/user/wenxing/RunIISpring16DR80_20161120/'
tree= ROOT.TChain("IIHEAnalysis")
samples=[
    'ZToEE_NNPDF30_13TeV-powheg_M_50_120/crab_ZToEE_NNPDF30_13TeV-powheg_M_50_120_reHLT/161119_213630/0000/',
    'ZToEE_NNPDF30_13TeV-powheg_M_120_200/crab_ZToEE_NNPDF30_13TeV-powheg_M_120_200_reHLT/161119_213833/0000/',
    'ZToEE_NNPDF30_13TeV-powheg_M_200_400/crab_ZToEE_NNPDF30_13TeV-powheg_M_200_400_reHLT/161119_214242/0000/',
    'ZToEE_NNPDF30_13TeV-powheg_M_400_800/crab_ZToEE_NNPDF30_13TeV-powheg_M_400_800_reHLT/161119_214423/0000/',
    'ZToEE_NNPDF30_13TeV-powheg_M_800_1400/crab_ZToEE_NNPDF30_13TeV-powheg_M_800_1400_reHLT/161119_214629/0000/',
    'ZToEE_NNPDF30_13TeV-powheg_M_1400_2300/crab_ZToEE_NNPDF30_13TeV-powheg_M_1400_2300_reHLT/161119_214824/0000/',
    'ZToEE_NNPDF30_13TeV-powheg_M_2300_3500/crab_ZToEE_NNPDF30_13TeV-powheg_M_2300_3500_reHLT/161119_215026/0000/',
    'ZToEE_NNPDF30_13TeV-powheg_M_3500_4500/crab_ZToEE_NNPDF30_13TeV-powheg_M_3500_4500_reHLT/161119_215251/0000/',
    'ZToEE_NNPDF30_13TeV-powheg_M_4500_6000/crab_ZToEE_NNPDF30_13TeV-powheg_M_4500_6000_reHLT/161119_215703/0000/',
    'ZToEE_NNPDF30_13TeV-powheg_M_6000_Inf/crab_ZToEE_NNPDF30_13TeV-powheg_M_6000_Inf_reHLT/161119_215841/0000/'
    ]

for sample in samples:
    print str(samples_path+sample+"/")
    for file in os.listdir(str(samples_path+sample+"/")):
        if file.endswith(".root"):
            tree.Add(str(samples_path+sample+"/"+file))

nEntries = tree.GetEntries()
#slot=1000
slot=1000000
steps=nEntries/slot
Ranges=[]
for step in range(0,steps + 1):
    Ranges.append(step*slot)
Ranges.append(nEntries)
print "index max job is ", len(Ranges) -2

from optparse import OptionParser
parser=OptionParser()
parser.add_option("-i","--index",dest="index",default=0,type=int) #python parser option.py -i 0 => options.index is 0
(options,args)=parser.parse_args()

print "You are running in range: ",Ranges[options.index], Ranges[options.index + 1]
#################################CLASS DEFINITION###############################################
##########################################################################################
#                       Functions and classes to read from the tree                      #
##########################################################################################
def get_HEEP_vars(tree):
    branches = dir(tree)
    HEEP_vars = []
    for leaf in tree.GetListOfLeaves():
        b = leaf.GetName()
        if '_n' in b:
            continue
        if 'HEEP_' in b or 'gsf_' in b:
            HEEP_vars.append(b)
    return HEEP_vars
HEEP_vars = get_HEEP_vars(tree)

class Zboson_object:
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
        self.p4 = e1.p4 + e2.p4
        self.regions = 'none'
        if self.e1.region=='barrel' and self.e2.region=='barrel':
            self.regions = 'BB'
        elif self.e1.region=='barrel' and self.e2.region=='endcap':
            self.regions = 'BE'
        elif self.e1.region=='endcap' and self.e2.region=='barrel':
            self.regions = 'BE'
        elif self.e1.region=='endcap' and self.e2.region=='endcap':
            self.regions = 'EE'

class Zboson_object_supercluster:#The energy is the supercluster energy
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
        self.p4 = e1.p4_supercluster + e2.p4_supercluster
        self.regions = 'none'
        if self.e1.region=='barrel' and self.e2.region=='barrel':
            self.regions = 'BB'
        elif self.e1.region=='barrel' and self.e2.region=='endcap':
            self.regions = 'BE'
        elif self.e1.region=='endcap' and self.e2.region=='barrel':
            self.regions = 'BE'
        elif self.e1.region=='endcap' and self.e2.region=='endcap':
            self.regions = 'EE'

class Zboson_object_h_recover:#The energy is corrected for the energy loss
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2
        self.p4 = e1.p4_h_recover + e2.p4_h_recover
        self.regions = 'none'
        if self.e1.region=='barrel' and self.e2.region=='barrel':
            self.regions = 'BB'
        elif self.e1.region=='barrel' and self.e2.region=='endcap':
            self.regions = 'BE'
        elif self.e1.region=='endcap' and self.e2.region=='barrel':
            self.regions = 'BE'
        elif self.e1.region=='endcap' and self.e2.region=='endcap':
            self.regions = 'EE'

class gen_electron_from_tree:
    def __init__(self, index, tree):
        self.p4 = ROOT.TLorentzVector( tree.mc_px[index], tree.mc_py[index], tree.mc_pz[index], tree.mc_energy[index])
        self.charge = tree.mc_charge[index]        
        # Variable to store reco-matched gsf
        # For now put this to False, and set it later if we find a match
        self.gsf_electron = False
        self.matched_gsf_electron = False
        self.matched_HEEPID       = False
        #self.matched_HEEPAcc      = False
        self.matched_HEEPAcc      = True

        self.region = 'none'
        if abs(self.p4.Eta()) < 1.4442:
            self.region =  'barrel'
        elif abs(self.p4.Eta())>1.566  and abs(self.p4.Eta())<2.5:
            self.region = 'endcap'

class gsf_electron_from_tree:
    def __init__(self, index, tree):
        for var in HEEP_vars:
            # Quick sanity check- it looks like some values may be missing from the ntuples
            if len(getattr(tree,var)) >index:
                setattr(self, var, getattr(tree,var)[index])
        #tree.gsf_px[index]
        #self.p4 = ROOT.TLorentzVector( self.gsf_px, self.gsf_py, self.gsf_pz, self.gsf_energy)
        self.p4 = ROOT.TLorentzVector( self.gsf_px, self.gsf_py, self.gsf_pz, self.gsf_caloEnergy)
        self.charge = tree.gsf_charge[index]        
        self.p4_supercluster = ROOT.TLorentzVector( self.gsf_px, self.gsf_py, self.gsf_pz, self.gsf_superClusterEnergy)#E is superClusterEnergy
        self.p4_h_recover = ROOT.TLorentzVector( self.gsf_px, self.gsf_py, self.gsf_pz, self.gsf_energy + self.gsf_energy*self.gsf_hadronicOverEm)#adding the H component
        self.HoverE=self.gsf_hadronicOverEm
        self.HEEPID = HEEP_ID_70(tree,index)
        #self.HEEPID  = self.HEEP_cutflow60_ID
        #self.HEEPAcc = self.HEEP_cutflow60_acceptance

        self.region = 'none'
        if abs(self.gsf_eta) < 1.4442:
            self.region =  'barrel'
        elif abs(self.gsf_eta)>1.566  and abs(self.gsf_eta)<2.5:
            self.region = 'endcap'
        

def make_gen_electrons(tree):
    mc_n = tree.mc_n
    gen_electrons = []
    for i in range(0,mc_n):
        if abs(tree.mc_pdgId[i])==11:# and tree.mc_pdgId[]==32: #an electron or positron with Z' for mother
            #print tree.mc_mother_index[i][0]# you can have more than one mother
            gen_electrons.append( gen_electron_from_tree(i, tree) )
    return gen_electrons

def make_gsf_electrons(tree):
    gsf_n = tree.gsf_n
    gsf_electrons = []
    for i in range(0,gsf_n):
        gsf_electrons.append( gsf_electron_from_tree(i, tree) )
    return gsf_electrons
##########################################################################################
#                                 Declare some histograms                                #
##########################################################################################
#hBase_mee = ROOT.TH1F('hBase_mee', '', 800, 0, 8000)
hBase_mee = ROOT.TH1F('hBase_mee', '', 800, 0, 8000)
hBase_mee.GetXaxis().SetTitle('m(ee) [GeV]')
hBase_mee.GetYaxis().SetTitle('entries per 100 GeV')

h_mee_gen             = {}
h_mee_gen_matchedGsf  = {}
h_mee_gen_matchedHEEP = {}
for regions in ['BB','BE','EE']:
    h_mee_gen[regions]             = hBase_mee.Clone('h_mee_gen_%s'%regions            )
    h_mee_gen_matchedGsf[regions]  = hBase_mee.Clone('h_mee_gen_matchedGsf_%s'%regions )
    h_mee_gen_matchedHEEP[regions] = hBase_mee.Clone('h_mee_gen_matchedHEEP_%s'%regions )

######## Mass resolution #################################################################
hBase_resolution = ROOT.TH1F('hBase_resolution', '', 100, -0.3, 0.1)
hBase_resolution.Sumw2()
hBase_scale      = ROOT.TH1F('hBase_scale'     , '', 100,  0.94, 1.06)
hBase_scale.Sumw2()
hBase_HoverE     = ROOT.TH1F('hBase_HoverE', '', 100, 0, 0.15)
hBase_HoverE.Sumw2()

HoverE_eta       = ROOT.TH2F('HoverE_eta', '',50,0,2.5,100, 0, 0.15,)
HoverE_eta.Sumw2()
eta_eleBarrel_BE = ROOT.TH1F('eta_eleBarrel_BE', '', 25, 0, 1.5)
eta_eleBarrel_BE.Sumw2()
eta_eleBarrel_BB = ROOT.TH1F('eta_eleBarrel_BB', '', 25, 0, 1.5)
eta_eleBarrel_BB.Sumw2()

#h_mee_resolution and h_mee_scale depend on region and mass bin
h_mee_resolution              = {}
h_mee_reco                    = {}
h_mee_gene                     = {}
h_mee_scale                   = {}
h_mee_scale_supercluster      = {}
h_mee_resolution_supercluster = {}
h_mee_scale_h_recover         = {}
h_mee_resolution_h_recover    = {}
h_mee_HoverE                  = {}
h_mee_HTotoverETot            = {}
h_mee_HoverE_lowEta           = {}
h_mee_HoverE_highEta          = {}
h_mee_HTotoverETot_lowEta     = {}
h_mee_HTotoverETot_highEta    = {}
h_mee_resolution_HoE_cut      = {}
h_mee_scale_HoE_cut           = {}

for regions in ['BB','BE','EE']:
    h_mee_resolution[regions]             ={}
    h_mee_reco[regions]                   ={}
    h_mee_gene[regions]                   ={}
    h_mee_resolution_supercluster[regions]={}
    h_mee_resolution_h_recover[regions]   ={}
    h_mee_scale[regions]                  ={}
    h_mee_scale_supercluster[regions]     ={}
    h_mee_scale_h_recover[regions]        ={}
    h_mee_HoverE[regions]                 ={}
    h_mee_HTotoverETot[regions]           ={}
    h_mee_HoverE_lowEta[regions]          ={}
    h_mee_HoverE_highEta[regions]         ={}
    h_mee_HTotoverETot_lowEta[regions]    ={}
    h_mee_HTotoverETot_highEta[regions]   ={}
    h_mee_resolution_HoE_cut[regions]     ={}
    h_mee_scale_HoE_cut[regions]          ={}


#I want different bin width. This defines my 3 regions
#hBase_mee_mr1 = ROOT.TH1F('hBase_mee_mr1', '', 5, 0, 1000)
#hBase_mee_mr2 = ROOT.TH1F('hBase_mee_mr2', '', 16, 1000, 5200)
#hBase_mee_mr3 = ROOT.TH1F('hBase_mee_mr3', '', 1, 5200, 6000)
#hBase_mee_mr4 = ROOT.TH1F('hBase_mee_mr4', '', 1, 6000, 7000)
#nbins= hBase_mee_mr1.GetSize() + hBase_mee_mr2.GetSize() + hBase_mee_mr3.GetSize() + hBase_mee_mr4.GetSize() -8
#now define the mass bin regions:
#bins=[]
#for i in range(1,hBase_mee_mr1.GetSize() -1):
#    bins.append(hBase_mee_mr1.GetBinLowEdge(i))
#    print hBase_mee_mr1.GetBinLowEdge(i)
#for i in range(1,hBase_mee_mr2.GetSize() -1):
#    bins.append(hBase_mee_mr2.GetBinLowEdge(i))
#    print hBase_mee_mr2.GetBinLowEdge(i)
#for i in range(1,hBase_mee_mr3.GetSize() -1):
#    bins.append(hBase_mee_mr3.GetBinLowEdge(i))
#    print hBase_mee_mr3.GetBinLowEdge(i)
#for i in range(1,hBase_mee_mr4.GetSize() -1):
#    bins.append(hBase_mee_mr4.GetBinLowEdge(i))
#    print hBase_mee_mr4.GetBinLowEdge(i)
#bins.append(7000)
#print "Last point is 7000"

#hBase_mee_mr1 = ROOT.TH1F('hBase_mee_mr1', '', 1, 50, 120)
#hBase_mee_mr2 = ROOT.TH1F('hBase_mee_mr2', '', 1, 120, 200)
#hBase_mee_mr3 = ROOT.TH1F('hBase_mee_mr3', '', 1, 200, 400)
#hBase_mee_mr4 = ROOT.TH1F('hBase_mee_mr4', '', 1, 400, 800)
#hBase_mee_mr5 = ROOT.TH1F('hBase_mee_mr5', '', 1, 800, 1400)
#hBase_mee_mr6 = ROOT.TH1F('hBase_mee_mr6', '', 1, 1400, 2300)
#hBase_mee_mr7 = ROOT.TH1F('hBase_mee_mr7', '', 1, 2300, 3500)
#hBase_mee_mr8 = ROOT.TH1F('hBase_mee_mr8', '', 1, 3500, 4500)
#hBase_mee_mr9 = ROOT.TH1F('hBase_mee_mr9', '', 1, 4500, 6000)
#hBase_mee_mr10 = ROOT.TH1F('hBase_mee_mr10', '', 1, 6000, 8000)
nbins=10
bins=[50,120,200,400,800,1400,2300,3500,4500,6000,8000]

bins_=array("d",bins) #to make everything work; "d" stands for double

hBase_mee_mr = ROOT.TH1F('hBase_mee_mr', '',nbins , bins_)

for regions in ['BB','BE','EE']:
    for i in range(1, hBase_mee_mr.GetNbinsX()+2):# for each mass bin (+2 in case of overflows)
        h_mee_resolution[regions][i]              = hBase_resolution.Clone(str('h_resolution_'+regions+'_%d'%i))             
        h_mee_reco[regions][i]                    = ROOT.TH1F(str('h_mee_reco_'+regions+'_%d'%i),str('h_mee_reco_'+regions+'_%d'%i),1000,50,120)             
        h_mee_gene[regions][i]                    = ROOT.TH1F(str('h_mee_gen_'+regions+'_%d'%i),str('h_mee_gen_'+regions+'_%d'%i),1000,50,120)
        h_mee_resolution_supercluster[regions][i] = hBase_resolution.Clone(str('h_resolution_supercluster_'+regions+'_%d'%i))
        h_mee_resolution_h_recover[regions][i]    = hBase_resolution.Clone(str('h_resolution_h_recover_'+regions+'_%d'%i))
        h_mee_scale[regions][i]                   = hBase_scale     .Clone(str('h_scale_'+regions+'_%d'    %i))
        h_mee_scale_supercluster[regions][i]      = hBase_scale     .Clone(str('h_scale_supercluster_'+regions+'_%d'    %i))
        h_mee_scale_h_recover[regions][i]         = hBase_scale     .Clone(str('h_scale_h_recover_'+regions+'_%d'    %i))
        h_mee_HoverE[regions][i]                  = hBase_HoverE    .Clone(str('h_HoverE_'+regions+'_%d'    %i))
        h_mee_HTotoverETot[regions][i]            = hBase_HoverE    .Clone(str('h_HTotoverETot_'+regions+'_%d'    %i))
        h_mee_HoverE_lowEta[regions][i]           = hBase_HoverE    .Clone(str('h_HoverE_lowEta'+regions+'_%d'    %i))
        h_mee_HoverE_highEta[regions][i]          = hBase_HoverE    .Clone(str('h_HoverE_highEta'+regions+'_%d'    %i))
        h_mee_HTotoverETot_lowEta[regions][i]     = hBase_HoverE    .Clone(str('h_HTotoverETot_lowEta'+regions+'_%d'    %i))
        h_mee_HTotoverETot_highEta[regions][i]    = hBase_HoverE    .Clone(str('h_HTotoverETot_highEta'+regions+'_%d'    %i))
        h_mee_resolution_HoE_cut[regions][i]      = hBase_resolution.Clone(str('h_resolution_HoE_cut_'+regions+'_%d'%i))             
        h_mee_scale_HoE_cut[regions][i]           = hBase_scale     .Clone(str('h_scale_HoE_cut_'+regions+'_%d'%i))

##########################################################################################
#                                    Now loop and plot                                   #
##########################################################################################
DeltaRCut = 0.15
nEventsWithEE = 0
#nEntries = 1000 #for quick Tests
#nEntries = tree.GetEntries()
region_fail_counter=0
nEventsWithEE=0
nEventsWithEEreco=0
nEventsWithNegMass=0
#print step*slot, (step+1)*slot
print "Number of mass bins for resolution", hBase_mee_mr.GetNbinsX()
#for iEntry in range(0,nEntries):
for iEntry in range(Ranges[options.index],Ranges[options.index + 1]):
    if iEntry%1000==0:
        print iEntry , '/' , nEntries
    tree.GetEntry(iEntry)
    
    #taking, for each entry, gen electrons and reco electrons
    gen_electrons = make_gen_electrons(tree)
    gsf_electrons = make_gsf_electrons(tree)
    if len(gen_electrons)<2: #those are electrons and positrons
        continue
    nEventsWithEE += 1
    
    #Taking the 2 eles with opposite charge
    gen1 = gen_electrons[0]
    s=1
    while(s<len(gen_electrons) and (gen_electrons[0].charge * gen_electrons[s].charge)==1):
        s+=1
    if(s<len(gen_electrons)):
        gen2 = gen_electrons[s]
    else:
        #print "pair not found"
        continue
    
    # Match gen to gsf electrons
    smallestDR1 = 1e6
    smallestDR2 = 1e6
    smallestDRGsf1 = -1 #this is the "number" which identifies the mathced gsf1
    smallestDRGsf2 = -1 #this is the "number" which identifies the mathced gsf2
    for gsf in gsf_electrons:
        DR1 = gsf.p4.DeltaR(gen1.p4)
        DR2 = gsf.p4.DeltaR(gen2.p4)
        
        if DR1 < smallestDR1:
            smallestDR1 = DR1
            smallestDRGsf1 = gsf
        if DR2 < smallestDR2:
            smallestDR2 = DR2
            smallestDRGsf2 = gsf
    
    # If successful (it means we found two matched reco ele), attach the gsf electrons to the gen electrons and change the status of the gen object
    if smallestDR1 < DeltaRCut:
        gen1.gsf_electron = smallestDRGsf1
        gen1.matched_gsf_electron = True
        gen1.matched_HEEPID = smallestDRGsf1.HEEPID
        #if(gen1.matched_HEEPID==1):
        #    print "HEEP ID 1", gen1.matched_HEEPID
        #gen1.matched_HEEPAcc = smallestDRGsf1.HEEPAcc -->set to true now
        
    if smallestDR2 < DeltaRCut:
        gen2.gsf_electron = smallestDRGsf2
        gen2.matched_gsf_electron = True
        gen2.matched_HEEPID = smallestDRGsf2.HEEPID
        #if(gen2.matched_HEEPID==1):
        #    print "HEEP ID 2", gen2.matched_HEEPID
        #gen2.matched_HEEPAcc = smallestDRGsf2.HEEPAcc -->set to true now
    
    #At this point, the gen eles have specified inside their class if they match a reco (and which one), and if they fire the HEEPID and the HEEPAcc
    # Now make the Z boson
    #For each entry:
    gen_Zboson = Zboson_object(gen1, gen2)
    
    # Now we can fill the histograms!
    regions = gen_Zboson.regions
    if regions=='none':
        region_fail_counter +=1
        continue
    if gen_Zboson.p4.M() < 0:
        nEventsWithNegMass+=1
        continue

    h_mee_gen[regions]            .Fill(gen_Zboson.p4.M()) # just fill with the gen eles
    if gen_Zboson.e1.matched_gsf_electron and gen_Zboson.e2.matched_gsf_electron:
        nEventsWithEEreco +=1
        h_mee_gen_matchedGsf[regions] .Fill(gen_Zboson.p4.M()) #eles gen and reco

    #print gen_Zboson.e1.matched_HEEPAcc 
    #print gen_Zboson.e2.matched_HEEPAcc
    if gen_Zboson.e1.matched_HEEPAcc and gen_Zboson.e1.matched_HEEPID and gen_Zboson.e2.matched_HEEPAcc and gen_Zboson.e2.matched_HEEPID:
        h_mee_gen_matchedHEEP[regions] .Fill(gen_Zboson.p4.M()) #eles gen and heep
        ##Mass resolution (Mreco-Mgen)/Mgen
        reco_Zboson = Zboson_object(gen1.gsf_electron, gen2.gsf_electron)
        reco_Zboson_supercluster = Zboson_object_supercluster(gen1.gsf_electron, gen2.gsf_electron)
        reco_Zboson_h_recover = Zboson_object_h_recover(gen1.gsf_electron, gen2.gsf_electron)
        reco_mass=reco_Zboson.p4.M()
        reco_mass_supercluster=reco_Zboson_supercluster.p4.M()
        reco_mass_h_recover=reco_Zboson_h_recover.p4.M()

        gen_mass=gen_Zboson.p4.M()
        i=hBase_mee_mr.GetXaxis().FindBin(gen_Zboson.p4.M())
        if (iEntry <100):
            print reco_mass, gen_mass
        if(gen_mass > 60):
            h_mee_resolution[regions][i]             .Fill((reco_mass-gen_mass)/gen_mass)
            h_mee_reco[regions][i]                   .Fill(reco_mass)
            h_mee_gene[regions][i]                   .Fill(gen_mass)
            h_mee_resolution_supercluster[regions][i].Fill((reco_mass_supercluster -gen_mass)/gen_mass)
            h_mee_resolution_h_recover[regions][i].Fill((reco_mass_h_recover -gen_mass)/gen_mass)
            h_mee_scale[regions][i].Fill(reco_mass/gen_mass)
            h_mee_scale_supercluster[regions][i].Fill(reco_mass_supercluster/gen_mass)
            h_mee_scale_h_recover[regions][i].Fill(reco_mass_h_recover/gen_mass)
            h_mee_HoverE[regions][i].Fill(gen1.gsf_electron.HoverE + gen2.gsf_electron.HoverE)
            if(abs(gen1.gsf_electron.p4.Eta()<0.75) and abs(gen2.gsf_electron.p4.Eta()<0.75)):
                h_mee_HoverE_lowEta[regions][i].Fill(gen1.gsf_electron.HoverE + gen2.gsf_electron.HoverE)
                if(abs(gen1.gsf_electron.p4.Eta()>0.75) and abs(gen2.gsf_electron.p4.Eta()>0.75)):
                    h_mee_HoverE_highEta[regions][i].Fill(gen1.gsf_electron.HoverE + gen2.gsf_electron.HoverE)

            H1=gen1.gsf_electron.HoverE*gen1.gsf_electron.p4.E()
            H2=gen2.gsf_electron.HoverE*gen2.gsf_electron.p4.E()
            E1=gen1.gsf_electron.p4.E()
            E2=gen2.gsf_electron.p4.E()
            h_mee_HTotoverETot[regions][i].Fill((H1 + H2)/(E1+E2)) #This is Htot/Etot
            if(abs(gen1.gsf_electron.p4.Eta()<0.75) and abs(gen2.gsf_electron.p4.Eta()<0.75)):
                h_mee_HTotoverETot_lowEta[regions][i].Fill((H1 + H2)/(E1 + E2))
            if(abs(gen1.gsf_electron.p4.Eta()>0.75) and abs(gen2.gsf_electron.p4.Eta()>0.75)):
                h_mee_HTotoverETot_highEta[regions][i].Fill((H1 + H2)/(E1 + E2))
            HoverE_eta.Fill(abs(gen1.gsf_electron.p4.Eta()),gen1.gsf_electron.HoverE) #2D histograms (Another check H/E)
            HoverE_eta.Fill(abs(gen2.gsf_electron.p4.Eta()),gen2.gsf_electron.HoverE)
            if regions == "BE":#Either 1 or 2 will be in the Barrel, the other one will go in the overflow (because its eta is in the EE)
                eta_eleBarrel_BE.Fill(abs(gen1.gsf_electron.p4.Eta()))
                eta_eleBarrel_BE.Fill(abs(gen2.gsf_electron.p4.Eta()))
            if regions == "BB":#
                eta_eleBarrel_BB.Fill(abs(gen1.gsf_electron.p4.Eta()))
                eta_eleBarrel_BB.Fill(abs(gen2.gsf_electron.p4.Eta()))
       
            if((gen1.gsf_electron.HoverE + gen2.gsf_electron.HoverE)<=0.01):#below the mean of HoE in barrel (only the good electron)
                h_mee_resolution_HoE_cut[regions][i].Fill((reco_mass -gen_mass)/gen_mass)
                h_mee_scale_HoE_cut[regions][i].Fill(reco_mass/gen_mass)

#loop over entries finished

print "Number of events with at least 2 ele in acceptance ",nEventsWithEE 
print "Number of events with Neg Mass ",nEventsWithNegMass 
print "Number of events where the gen ele are reconstructed ",nEventsWithEEreco 
print "Number of events outside the regions ",region_fail_counter

file_mass= ROOT.TFile('/user/gfasanel/Mass_resolution_study/Resolution/Histos/histograms_mass_res_'+str(options.index)+'_2016.root','RECREATE')
file_mass.cd()
for regions in ['BB','BE','EE']:
    for i in range(1, hBase_mee_mr.GetNbinsX()+1):# for each mass bin
        h_mee_resolution[regions][i]              . Write()
        h_mee_reco[regions][i]                    . Write()
        h_mee_gene[regions][i]                    . Write()
        h_mee_resolution_supercluster[regions][i] . Write()
        h_mee_resolution_h_recover[regions][i]    . Write()
        h_mee_scale[regions][i]                   . Write()
        h_mee_scale_supercluster[regions][i]      . Write()
        h_mee_scale_h_recover[regions][i]         . Write()
        h_mee_HoverE[regions][i]                  . Write()
        h_mee_HTotoverETot[regions][i]            . Write()
        h_mee_HoverE_lowEta[regions][i]           . Write()
        h_mee_HoverE_highEta[regions][i]          . Write()
        h_mee_HTotoverETot_lowEta[regions][i]     . Write()
        h_mee_HTotoverETot_highEta[regions][i]    . Write()
        h_mee_resolution_HoE_cut[regions][i]      . Write()
        h_mee_scale_HoE_cut[regions][i]           . Write()
        h_mee_gen[regions]                        . Write()
        h_mee_gen_matchedGsf[regions]             . Write()

HoverE_eta      .Write()
eta_eleBarrel_BE.Write()
eta_eleBarrel_BB.Write()
hBase_mee_mr    .Write()
#This dummy histogram is used to decide the mass binning

print "Check the output here"
print "./Resolution/Histos/histograms_mass_res_*_2016.root"





