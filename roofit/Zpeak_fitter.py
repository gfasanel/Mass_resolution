#python Zpeak_fitter.py -t resolution
import ROOT
import math
ROOT.gSystem.Load("libRooFit")
ROOT.gSystem.Load("RooDCBShape_cxx.so") #This is the way to handle user defined pdf (generated with RooClassFactory). Compile once and for all in ROOT and then add it as a library
from ROOT import RooFit, RooRealVar, RooGaussian, RooDataSet, RooArgList, RooTreeData, RooArgSet
ROOT.gROOT.SetBatch(ROOT.kTRUE) 

import sys,getopt

print "################################### FITTING THE Z PEAK ############################################"
for var_type in ['data','MC']:
   for regions in ['BB','BE','EE']:
      if var_type=='MC':
         file_mass=ROOT.TFile('../Extra_sigma/MC_Zpeak.root','READ')
         #file_mass=ROOT.TFile('../Extra_sigma/MC_Zpeak_test.root','READ')
      else:
         file_mass=ROOT.TFile('../Extra_sigma/data_Zpeak.root','READ')
         #file_mass=ROOT.TFile('../Extra_sigma/data_Zpeak_test.root','READ')
      hist_res   = file_mass.Get(str('h_mee_'+var_type+'_'+regions))
      max=hist_res.GetXaxis().GetBinCenter(hist_res.GetMaximumBin())
      mean=hist_res.GetMean()
      print "MAX AND MIN, RMS", max, min, hist_res.GetRMS()
      x=ROOT.RooRealVar("x","m_{ee}",max-2*hist_res.GetRMS(),max+2*hist_res.GetRMS())
      # Create a binned dataset (RooDataHist) that imports contents of TH1 and associates its contents to observable 'x'
      dh=ROOT.RooDataHist("dh","dh",RooArgList(x), hist_res)  #Without RooArgList it doesn't work

      # P l o t   a n d   f i t   a   R o o D a t a H i s t
      # ---------------------------------------------------
   
      # Make plot of binned dataset showing Poisson error bars (RooFit default)
      frame = x.frame(RooFit.Name(""),RooFit.Title(" ")) #Title(" ") takes away "Rooplot of x"
      #frame is a RooPlot generated from the RooRealVar x
      #to change x range: RooFit.Range(xmin,xmax)
      frame.SetMaximum(2*hist_res.GetMaximum())
   
      dh.plotOn(frame)  
   
      mean_guessed=hist_res.GetXaxis().GetBinCenter(hist_res.GetMaximumBin())
      sigma_guessed=hist_res.GetRMS()/4.
      print "SIGMA GUESSED ",sigma_guessed
      mean=ROOT.RooRealVar("mean","mean",mean_guessed,mean_guessed -0.1*sigma_guessed, mean_guessed + 0.1*sigma_guessed)
      sigma=ROOT.RooRealVar("sigma","sigma",sigma_guessed,0.,2) 
      alpha=ROOT.RooRealVar("alpha","alpha",0.1,0.,1.5) #after alpha*sigma, gaussian connected to power law: alpha>0 => left tail alpha<0 => right tail
      alphaR=ROOT.RooRealVar("alphaR","alphaR",-0.1,-0.,-1.5) #after alpha*sigma, gaussian connected to power law: alpha>0 => left tail alpha<0 => right tail
      n=ROOT.RooRealVar("nL","nL",3,0.1,15) #exponent of the power law tail
      alphaR=ROOT.RooRealVar("alphaR","alphaR",3,0.1,15)
      nR=ROOT.RooRealVar("nR","nR",3,0.1,10)

      #RooAbsPdf *fit_func = new RooCBShape("fit_func", "crystal ball", x,mean,sigma,alpha,n) #This way works in C++
      #Python version
      #fit_func=ROOT.RooCBShape("fit_func", "crystal ball", x,mean,sigma,alpha,n) 
      fit_func=ROOT.RooDCBShape("dfit_func", "double crystal ball", x, mean, sigma, alpha, alphaR, n, nR)
      #fit_func=ROOT.RooGaussian("fit_func","gaussian",x, mean, sigma)
      fit_func.fitTo(dh)

      res=fit_func.fitTo(dh,RooFit.Save()) #This is the general way of handling fit results
      sigma_fit=res.floatParsFinal().find("sigma").getVal()
      sigma_fit_error=res.floatParsFinal().find("sigma").getError()

      mean_fit=res.floatParsFinal().find("mean").getVal()
      mean_fit_error=res.floatParsFinal().find("mean").getError()

      #Plot and save the fit
      fit_func.plotOn(frame)
      #I want to save the histogram and the fit in a file: how is it done? RooWorkSpace?? Add this later
      c = ROOT.TCanvas("fit","fit",800,800) #X length, Y length
      c.cd()
      mean_label =ROOT.TLatex(0.12,0.85,"mean = %.4f #pm %.4f"%(mean_fit,mean_fit_error))
      mean_label.SetTextSize(0.04)
      mean_label.SetNDC()
      chi2=frame.chiSquare()
      sigma_label =ROOT.TLatex(0.12,0.8,"sigma = %.4f #pm %.4f"%(sigma_fit,sigma_fit_error))
      sigma_label.SetNDC()
      sigma_label.SetTextSize(0.04)
      chi2=frame.chiSquare()

      text= ROOT.TLatex(0.12,0.75,"#chi^{2}_{reduced} = %.2f" %chi2)
      text.SetNDC()
      text.SetTextSize(0.04)
      entry= ROOT.TLatex(0.12,0.65,"Entries = %d" %hist_res.GetEntries())
      entry.SetNDC()
      entry.SetTextSize(0.04)

      cms =ROOT.TLatex(0.12,0.95,"CMS Internal")
      cms.SetNDC()
      cms.SetTextSize(0.04)

      frame.Draw() 
      text.Draw()
      entry.Draw()
      mean_label.Draw()
      sigma_label.Draw()
      cms.Draw()

      c.SaveAs(str('../Extra_sigma/'+hist_res.GetName()+'.png'))
      c.SaveAs(str('../Extra_sigma/'+hist_res.GetName()+'.pdf'))

      #Save Parameters (mean and sigma) in a txt file
      #if regions=='BB':
      #   file_res_BB.write("%lf %lf %lf %lf\n"%( mean_fit, sigma_fit, mean_fit_error, sigma_fit_error))
      #elif regions=='BE':
      #elif regions=='EE':
              











