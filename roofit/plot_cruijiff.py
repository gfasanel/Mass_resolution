import ROOT
import math
ROOT.gSystem.Load("libRooFit")
ROOT.gSystem.Load("RooDCBShape_cxx.so") #This is the way to handle user defined pdf (generated with RooClassFactory). Compile once and for all in ROOT and then add it as a library
ROOT.gSystem.Load("RooCruijff_cc.so")
#from ROOT import RooFit, RooRealVar, RooGaussian, RooDataSet, RooArgList, RooTreeData, RooArgSet
from ROOT import *
ROOT.gROOT.SetBatch(ROOT.kTRUE) 
ROOT.gSystem.Load("rootlogon_style_C.so")
ROOT.gSystem.Load("../EffSigma/EffSigma_C.so")
ROOT.rootlogon_style()

import sys,getopt

def main(argv):# defining the main function, called later
   try:
      opts, args = getopt.getopt(argv,"ht:",["type=","help"])#getopt takes three args: a list (argv),short options, long options
   except getopt.GetoptError:
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-h","--help"):#this doesn't work properly....
         print 'python cb_fitter.py -t resolution'
         print 'or'
         print 'python cb_fitter.py --type=resolution'
         sys.exit(2)
      elif opt in ("-t","--type"):
         global _t #defining a global variable _t
         _t=arg

#def getResolution(mass):
#   return res_scale*0.01*(sqrt(res_s*res_s/mass+res_n*res_n/mass/mass+res_c*res_c)+res_slope*mass)

def getResolution(mass):
   parameters={}
   parameters['alphaL']={}
   parameters['alphaR']={}
   parameters['scale'] ={}
   parameters['sigma'] ={}

   #####alphaL BB
   a_BB=1850
   b_BB=2.2
   c_BB=0.7
   d_BB=8.56e-9
   e_BB=0.24
   parameters['alphaL']['BB']=(mass<a_BB)*(pow(mass,-b_BB) -b_BB*pow(a_BB,-c_BB)) + (mass>a_BB)*d_BB*(mass-a_BB)*(mass-a_BB) +e_BB #power law + parabola

   #####alphaL BE
   a_BE=3.9
   b_BE=10
   c_BE=0.17
   d_BE=1.35e-5
   parameters['alphaL']['BE']=sqrt(a_BE*a_BE/mass + b_BE*b_BE/mass/mass + c_BE*c_BE) + d_BE*mass #resolution function with linear term

   #####alphaR BB
   a_BB=1.3e-3
   b_BB=2218
   c_BB=1.1e-8
   parameters['alphaR']['BB']=a_BB + c_BB*(mass-b_BB)*(mass-b_BB) #parabola

   #####alphaR BE
   a_BE=2.27e-2
   b_BE=2400
   c_BE=-4.31e-9
   parameters['alphaR']['BE']=a_BE + c_BE*(mass-b_BE)*(mass-b_BE) #parabola

   #####scale BB
   a_BB=1.
   b_BB=814.8
   c_BB=-4.1e-9
   d_BB=-3.81e-10
   parameters['scale']['BB']=a_BB + (mass<b_BB)*c_BB*(mass-b_BB)*(mass-b_BB) + (mass>b_BB)*d_BB*(mass-b_BB)*(mass-b_BB) #asymmetric parabola 

   #####scale BE
   a_BE=1.
   b_BE=1388.8
   c_BE=-5.07e-9
   d_BE=2.5e-10
   parameters['scale']['BE']=a_BE + (mass<b_BE)*c_BE*(mass-b_BE)*(mass-b_BE) + (mass>b_BE)*d_BE*(mass-b_BE)*(mass-b_BE) #asymmetric parabola

   #####sigma BB
   s_BB=11.2
   n_BB=0.1
   c_BB=0.86
   l_BB=5.3e-5
   parameters['sigma']['BB']=(sqrt(s_BB*s_BB/mass + n_BB*n_BB/mass/mass + c_BB*c_BB) + l_BB*mass)*0.01 #resolution function with linear term

   #####sigma BE
   s_BE=16.6
   n_BE=10
   c_BE=1.5
   parameters['sigma']['BE']=(sqrt(s_BE*s_BE/mass + n_BE*n_BE/mass/mass + c_BE*c_BE))*0.01 #resolution function w/o linear term


   return parameters



if __name__ == "__main__":
   main(sys.argv[1:]) #argument 0 is the name of the file.py, so let's start from the second one

###################Take the histograms#################
file_mass=ROOT.TFile('../Resolution/histograms_mass_res.root','READ')

if(_t=='resolution'):
    var_type= 'resolution'
    scale_type= 'scale'

if('res' in var_type): #if var_type contains the substring 'res'
   #write all the parameters of the cb (or dCB) you fitted as a function of the mass bins
   file_res_BB = open(str('../Resolution/histograms_mass_'+var_type+'_BB.txt'),'w+')
   file_res_BE = open(str('../Resolution/histograms_mass_'+var_type+'_BE.txt'),'w+')

   file_alphaL_BB = open(str('../Resolution/histograms_mass_alphaL_BB.txt'),'w+')
   file_alphaL_BE = open(str('../Resolution/histograms_mass_alphaL_BE.txt'),'w+')

   file_alphaR_BB = open(str('../Resolution/histograms_mass_alphaR_BB.txt'),'w+')
   file_alphaR_BE = open(str('../Resolution/histograms_mass_alphaR_BE.txt'),'w+')

   file_scale_BB = open('../Resolution/histograms_mass_'+scale_type+'_BB.txt','w+')
   file_scale_BE = open('../Resolution/histograms_mass_'+scale_type+'_BE.txt','w+') 

hBase_mee_mr = file_mass.Get('hBase_mee_mr') #Taken from the file, binning decided in histos_.py

for regions in ['BB','BE']:
     #for i in range(1, hBase_mee_mr.GetNbinsX()+1):# for each mass bin
   for i in range(1, 9):# for each mass bin
        mass_point=hBase_mee_mr.GetXaxis().GetBinCenter(i)
        hist_res   = file_mass.Get(str('h_'+var_type+'_'+regions+'_%d'%i))
        if('res' in var_type): #If substring 'res' is in var_type
           #x=ROOT.RooRealVar("x","(m_{reco}-m_{gen})/m_{gen}",-0.1,+0.06)  #name, title, range: you can use ("x","my x variable",-10,10)
           x=ROOT.RooRealVar("x","(m_{reco}-m_{gen})/m_{gen}",-0.06,+0.03) 
        dh=ROOT.RooDataHist("dh","dh",RooArgList(x), hist_res)  #Without RooArgList it doesn't work
        frame = x.frame(RooFit.Name(""),RooFit.Title(" ")) #Title(" ") takes away "Rooplot of x"
        frame.SetMaximum(2*hist_res.GetMaximum())
        dh.plotOn(frame)  
        
        #Set Cruijff parameters
        alpha=ROOT.RooRealVar("alpha","alpha",getResolution(mass_point)['alphaL'][regions],0.,0.5) 
        alphaR=ROOT.RooRealVar("alphaR","alphaR",getResolution(mass_point)['alphaR'][regions],0.,0.5)
        mean=ROOT.RooRealVar("mean","mean",(getResolution(mass_point)['scale'][regions] -1),0.9, 1.1) #-1
        sigma_extra={}
        sigma_extra['BB']=0.00814
        sigma_extra['BE']=0.01257
        res=getResolution(mass_point)['sigma'][regions]
        sigma=ROOT.RooRealVar("sigma","sigma",sqrt(res*res - sigma_extra[regions]*sigma_extra[regions]),0.,0.05) #difference in quadrature sigma extra

        cball=RooCruijff("cruijff", "cruijff",x,mean,sigma,sigma,alpha, alphaR)
        cball.plotOn(frame, RooFit.LineColor(ROOT.kRed))
        c = ROOT.TCanvas("fit","fit",800,800) #X length, Y length
        c.cd()
        frame.Draw() 

        c.SaveAs(str('~/public_html/Res_scale_Moriond17/Test_fit_results/'+var_type+'_'+regions+'/'+hist_res.GetName()+'.png'))
        c.SaveAs(str('~/public_html/Res_scale_Moriond17/Test_fit_results/'+var_type+'_'+regions+'/'+hist_res.GetName()+'.pdf'))















