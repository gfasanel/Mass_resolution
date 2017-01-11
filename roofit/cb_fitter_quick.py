import ROOT
import math
ROOT.gSystem.Load("libRooFit")
ROOT.gSystem.Load("RooDCBShape_cxx.so") #This is the way to handle user defined pdf (generated with RooClassFactory). Compile once and for all in ROOT and then add it as a library
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
file_mass=ROOT.TFile('../Resolution/partial_histos_2016/histograms_mass_res_0_2016.root','READ')

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


hBase_mee_mr = file_mass.Get('hBase_mee_mr') #Taken from the file, binning decided in histos_.py

print "################################### FITTING PROCEDURE ############################################"

for regions in ['BB','BE']:
     #for i in range(1, hBase_mee_mr.GetNbinsX()+1):# for each mass bin
     for i in range(1, 2):# only the first bin
        hist_res   = file_mass.Get(str('h_'+var_type+'_'+regions+'_%d'%i))
        if('res' in var_type): #If substring 'res' is in var_type
           x=ROOT.RooRealVar("x","(m_{reco}-m_{gen})/m_{gen}",-0.1,+0.06)  #name, title, range: you can use ("x","my x variable",-10,10)
        dh=ROOT.RooDataHist("dh","dh",RooArgList(x), hist_res)  #Without RooArgList it doesn't work
        frame = x.frame(RooFit.Name(""),RooFit.Title(" ")) #Title(" ") takes away "Rooplot of x"
        frame.SetMaximum(2*hist_res.GetMaximum())
        dh.plotOn(frame)  

        mean_guessed=hist_res.GetXaxis().GetBinCenter(hist_res.GetMaximumBin())
        sigma_guessed=0.01
        mean=ROOT.RooRealVar("mean","mean",mean_guessed,mean_guessed -1.5*sigma_guessed, mean_guessed + 1.5*sigma_guessed) #Initial guess, lower bound, upper bound 
        sigma=ROOT.RooRealVar("sigma","sigma",sigma_guessed,0.,0.05)
        alpha=ROOT.RooRealVar("alpha","alpha",1,0.,3.) #after alpha*sigma, gaussian connected to power law: alpha>0 => left tail alpha<0 => right tail
        n=ROOT.RooRealVar("n","n",2,0.,100.) #exponent of the power law tail
        alphaR=ROOT.RooRealVar("alphaR","alphaR",3,0.,5)
        nR=ROOT.RooRealVar("nL","nL",100,0.,1000)

        #cball=ROOT.RooCBShape("cball", "crystal ball", x,mean,sigma,alpha,n) 
        cball=ROOT.RooDCBShape("dcball", "double crystal ball", x, mean, sigma, alpha, alphaR, n, nR)
        cball.fitTo(dh)
        res=cball.fitTo(dh,RooFit.Save()) #This is the general way of handling fit results

        sigma_fit=res.floatParsFinal().find("sigma").getVal()
        sigma_fit_error=res.floatParsFinal().find("sigma").getError()
        mean_fit=res.floatParsFinal().find("mean").getVal()
        mean_fit_error=res.floatParsFinal().find("mean").getError()
        alpha_fit=res.floatParsFinal().find("alpha").getVal()
        alpha_fit_error=res.floatParsFinal().find("alpha").getError()
        n_fit=res.floatParsFinal().find("n").getVal()
        n_fit_error=res.floatParsFinal().find("n").getError()

        #Plot and save the fit
        cball.plotOn(frame)
        #I want to save the histogram and the fit in a file: how is it done? RooWorkSpace?? Add this later
        c = ROOT.TCanvas("fit","fit",800,800) #X length, Y length
        c.cd()
        mean_label =ROOT.TLatex(0.15,0.85,"mean = %.4f #pm %.4f"%(mean_fit,mean_fit_error))
        mean_label.SetTextSize(0.04)
        mean_label.SetNDC()
        sigma_label =ROOT.TLatex(0.15,0.8,"sigma = %.4f #pm %.4f"%(sigma_fit,sigma_fit_error))
        sigma_label.SetNDC()
        sigma_label.SetTextSize(0.04)
        alpha_label =ROOT.TLatex(0.15,0.75,"alpha = %.4f #pm %.4f"%(alpha_fit,alpha_fit_error))
        alpha_label.SetNDC()
        alpha_label.SetTextSize(0.04)
        n_label =ROOT.TLatex(0.15,0.7,"n = %.4f #pm %.4f"%(n_fit,n_fit_error))
        n_label.SetNDC()
        n_label.SetTextSize(0.04)
        chi2=frame.chiSquare()
        text= ROOT.TLatex(0.15,0.65,"#chi^{2}_{reduced} = %.2f" %chi2)
        text.SetNDC()
        text.SetTextSize(0.04)
        eff= ROOT.TLatex(0.15,0.55,"#\sigma^{eff} = %.4f" %ROOT.EffSigma(hist_res))
        eff.SetNDC()
        eff.SetTextSize(0.04)
        #entry= ROOT.TLatex(0.12,0.65,"Entries = %d" %hist_res.GetEntries())
        #entry.SetNDC()
        #entry.SetTextSize(0.04)

        cms =ROOT.TLatex(0.55,0.97,"CMS Internal")
        cms.SetNDC()
        cms.SetTextSize(0.04)

        frame.Draw() 
        #entry.Draw()
        mean_label.Draw()
        sigma_label.Draw()
        alpha_label.Draw()
        n_label.Draw()
        text.Draw()
        eff.Draw()
        cms.Draw()

        c.SaveAs(str('~/public_html/Res_scale_16/fit_results/'+var_type+'_'+regions+'/temp/'+hist_res.GetName()+'.png'))
        c.SaveAs(str('~/public_html/Res_scale_16/fit_results/'+var_type+'_'+regions+'/temp/'+hist_res.GetName()+'.pdf'))
        c.SaveAs(str('~/public_html/Res_scale_16/Extra_sigma/temp/'+hist_res.GetName()+'.png'))
        c.SaveAs(str('~/public_html/Res_scale_16/Extra_sigma/temp/'+hist_res.GetName()+'.pdf'))














