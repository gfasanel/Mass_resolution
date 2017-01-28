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

if __name__ == "__main__":
   main(sys.argv[1:]) #argument 0 is the name of the file.py, so let's start from the second one

###################Take the histograms#################
file_mass=ROOT.TFile('../Resolution/histograms_mass_res.root','READ')

if(_t=='resolution'):
    var_type= 'resolution'
    scale_type= 'scale'
if(_t=='res_SC'):
    var_type= 'resolution_supercluster'
    scale_type= 'scale_supercluster'
if(_t=='res_h'):
    var_type= 'resolution_h_recover'
    scale_type= 'scale_h_recover'
if(_t=='res_HoE_cut'):
    var_type= 'resolution_HoE_cut'
    scale_type= 'scale_HoE_cut'

if('res' in var_type): #if var_type contains the substring 'res'
   #write all the parameters of the cb (or dCB) you fitted as a function of the mass bins
   file_res_BB = open(str('../Resolution/histograms_mass_'+var_type+'_BB.txt'),'w+')
   file_res_BE = open(str('../Resolution/histograms_mass_'+var_type+'_BE.txt'),'w+')

   file_sigmaL_BB = open(str('../Resolution/histograms_mass_sigmaL_BB.txt'),'w+')
   file_sigmaL_BE = open(str('../Resolution/histograms_mass_sigmaL_BE.txt'),'w+')

   file_sigmaR_BB = open(str('../Resolution/histograms_mass_sigmaR_BB.txt'),'w+')
   file_sigmaR_BE = open(str('../Resolution/histograms_mass_sigmaR_BE.txt'),'w+')

   file_alphaL_BB = open(str('../Resolution/histograms_mass_alphaL_BB.txt'),'w+')
   file_alphaL_BE = open(str('../Resolution/histograms_mass_alphaL_BE.txt'),'w+')

   file_nL_BB = open(str('../Resolution/histograms_mass_nL_BB.txt'),'w+')
   file_nL_BE = open(str('../Resolution/histograms_mass_nL_BE.txt'),'w+')

   file_alphaR_BB = open(str('../Resolution/histograms_mass_alphaR_BB.txt'),'w+')
   file_alphaR_BE = open(str('../Resolution/histograms_mass_alphaR_BE.txt'),'w+')

   file_nR_BB = open(str('../Resolution/histograms_mass_nR_BB.txt'),'w+')
   file_nR_BE = open(str('../Resolution/histograms_mass_nR_BE.txt'),'w+')

   #The scale can be directly derived from the resolution parameter
   file_scale_BB = open('../Resolution/histograms_mass_'+scale_type+'_BB.txt','w+')
   file_scale_BE = open('../Resolution/histograms_mass_'+scale_type+'_BE.txt','w+') 


hBase_mee_mr = file_mass.Get('hBase_mee_mr') #Taken from the file, binning decided in histos_.py

print "################################### FITTING PROCEDURE ############################################"

#for regions in ['BB','BE','EE']:
#for regions in ['BB','BE']:
#for regions in ['BB']:
for regions in ['BE']:
     for i in range(1, hBase_mee_mr.GetNbinsX()+1):# for each mass bin
        hist_res   = file_mass.Get(str('h_'+var_type+'_'+regions+'_%d'%i))
        if('res' in var_type): #If substring 'res' is in var_type
           #x=ROOT.RooRealVar("x","(m_{reco}-m_{gen})/m_{gen}",-0.1,+0.06)  #name, title, range: you can use ("x","my x variable",-10,10)
           x=ROOT.RooRealVar("x","(m_{reco}-m_{gen})/m_{gen}",-0.06,+0.03) 
        dh=ROOT.RooDataHist("dh","dh",RooArgList(x), hist_res)  #Without RooArgList it doesn't work
        frame = x.frame(RooFit.Name(""),RooFit.Title(" ")) #Title(" ") takes away "Rooplot of x"
        frame.SetMaximum(2*hist_res.GetMaximum())
        dh.plotOn(frame)  

        mean_guessed=hist_res.GetXaxis().GetBinCenter(hist_res.GetMaximumBin())
        sigma_guessed=0.005
        mean=ROOT.RooRealVar("mean","mean",mean_guessed,mean_guessed -1.*sigma_guessed, mean_guessed + 1.*sigma_guessed) #Initial guess, lower bound, upper bound 
        sigma=ROOT.RooRealVar("sigma","sigma",sigma_guessed,0.,0.05)
        sigmaR=ROOT.RooRealVar("sigmaR","sigmaR",sigma_guessed,0.,0.05) #only a cruijff has 2 sigmas
        
        #Perfectly working for BB --> 1 sigma only and 2 alpha fits
#        alpha=ROOT.RooRealVar("alpha","alpha",0.2,0.,0.5) 
#        alphaR=ROOT.RooRealVar("alphaR","alphaR",0.2,0.,0.5)
#        cball=RooCruijff("cruijff", "cruijff",x,mean,sigma,sigma,alpha, alphaR)

        #alpha=ROOT.RooRealVar("alpha","alpha",0.23,0.23,0.23) -->Perfectly working for endcapa
        #alpha=ROOT.RooRealVar("alpha","alpha",0.2,0.2,0.2) -->Perfectly working for endcap
        #alphaR=ROOT.RooRealVar("alphaR","alphaR",0.055,0.054,0.056) -->Perfectly working for endcap

        #Perfectly working for BB --> 1 sigma only and 2 alpha fits
        alpha=ROOT.RooRealVar("alpha","alpha",0.2,0.,1.)
        alphaR=ROOT.RooRealVar("alphaR","alphaR",0.055,0.,0.1) 

        #cball=RooCruijff("cruijff", "cruijff",x,mean,sigma,sigma,alpha, alphaR)
        cball=RooCruijff("cruijff", "cruijff",x,mean,sigma,sigma,alpha, alphaR)
        cball.fitTo(dh)
        res=cball.fitTo(dh,RooFit.Save()) #This is the general way of handling fit results

        mean_fit=res.floatParsFinal().find("mean").getVal()
        mean_fit_error=res.floatParsFinal().find("mean").getError()
        sigma_fit=res.floatParsFinal().find("sigma").getVal()
        sigma_fit_error=res.floatParsFinal().find("sigma").getError()
#        sigmaR_fit_error=res.floatParsFinal().find("sigmaR").getError()
#        sigmaR_fit=res.floatParsFinal().find("sigmaR").getVal()
        sigmaR_fit=0
        sigmaR_fit_error=0
        alpha_fit=res.floatParsFinal().find("alpha").getVal()
        alpha_fit_error=res.floatParsFinal().find("alpha").getError()
        alphaR_fit=res.floatParsFinal().find("alphaR").getVal()
        alphaR_fit_error=res.floatParsFinal().find("alphaR").getError()


        #Plot and save the fit
        cball.plotOn(frame)
        #I want to save the histogram and the fit in a file: how is it done? RooWorkSpace?? Add this later
        c = ROOT.TCanvas("fit","fit",800,800) #X length, Y length
        c.cd()
        mean_label =ROOT.TLatex(0.15,0.85,"mean = %.4f #pm %.4f"%(mean_fit,mean_fit_error))
        mean_label.SetTextSize(0.04)
        mean_label.SetNDC()
        sigma_label =ROOT.TLatex(0.15,0.8,"sigmaL = %.4f #pm %.4f"%(sigma_fit,sigma_fit_error))
        sigma_label.SetNDC()
        sigma_label.SetTextSize(0.04)
        sigmaR_label =ROOT.TLatex(0.15,0.75,"sigmaR = %.4f #pm %.4f"%(sigmaR_fit,sigmaR_fit_error))
        sigmaR_label.SetNDC()
        sigmaR_label.SetTextSize(0.04)
        alpha_label =ROOT.TLatex(0.15,0.7,"alphaL = %.4f #pm %.4f"%(alpha_fit,alpha_fit_error))
        alpha_label.SetNDC()
        alpha_label.SetTextSize(0.04)
        alphaR_label =ROOT.TLatex(0.15,0.65,"alphaR = %.4f #pm %.4f"%(alphaR_fit,alphaR_fit_error))
        alphaR_label.SetNDC()
        alphaR_label.SetTextSize(0.04)

        chi2=frame.chiSquare()
        text= ROOT.TLatex(0.15,0.65,"#chi^{2}_{reduced} = %.2f" %chi2)
        text.SetNDC()
        text.SetTextSize(0.04)
        eff= ROOT.TLatex(0.15,0.55,"#\sigma^{eff} = %.4f" %ROOT.EffSigma(hist_res))
        eff.SetNDC()
        eff.SetTextSize(0.04)

        cms =ROOT.TLatex(0.55,0.97,"CMS Internal")
        cms.SetNDC()
        cms.SetTextSize(0.04)

        frame.Draw() 
        #entry.Draw()
        mean_label.Draw()
        sigma_label.Draw()
        sigmaR_label.Draw()
        alpha_label.Draw()
        alphaR_label.Draw()

        #text.Draw() -->chi2 label
        eff.Draw()
        cms.Draw()

        c.SaveAs(str('~/public_html/Res_scale_Moriond17/fit_results/'+var_type+'_'+regions+'/'+hist_res.GetName()+'.png'))
        c.SaveAs(str('~/public_html/Res_scale_Moriond17/fit_results/'+var_type+'_'+regions+'/'+hist_res.GetName()+'.pdf'))

        #Save Parameters in a txt file
        if('res' in var_type): # if var_type contains 'res'
           if regions=='BB':
              file_res_BB.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i), sigma_fit, sigma_fit_error))
              file_sigmaL_BB.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i), sigma_fit, sigma_fit_error))
              file_sigmaR_BB.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i), sigmaR_fit, sigmaR_fit_error))

              file_alphaL_BB.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i), alpha_fit, alpha_fit_error))
              file_alphaR_BB.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i), alphaR_fit, alphaR_fit_error))
              file_scale_BB.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i), mean_fit + 1., mean_fit_error))

           elif regions=='BE':
              file_res_BE.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i), sigma_fit, sigma_fit_error))
              file_sigmaL_BE.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i), sigma_fit, sigma_fit_error))
              file_sigmaR_BE.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i), sigmaR_fit, sigmaR_fit_error))

              file_alphaL_BE.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i), alpha_fit, alpha_fit_error))
              file_alphaR_BE.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i), alphaR_fit, alphaR_fit_error))
              file_scale_BE.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i), mean_fit + 1., mean_fit_error))














