#python Zpeak_fitter.py -t resolution
import ROOT
import math
import os
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
      hist_res.Rebin(3) #1.5 GeV binning
      max=hist_res.GetXaxis().GetBinCenter(hist_res.GetMaximumBin())
      mean_histo=hist_res.GetMean()
      x=ROOT.RooRealVar("x","m_{ee} [GeV]",60,120)
      #x=ROOT.RooRealVar("x","m_{ee} [GeV]",80,100)

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
      #sigma_guessed=hist_res.GetRMS() #only Breit Wigner
      print "SIGMA GUESSED ",sigma_guessed
      mean=ROOT.RooRealVar("mean","mean",mean_guessed,mean_guessed -0.2*sigma_guessed, mean_guessed + 0.2*sigma_guessed)
      sigma=ROOT.RooRealVar("sigma","sigma",sigma_guessed,0.,4) 
      width=ROOT.RooRealVar("width","width",sigma_guessed,0.,4) 
      alpha=ROOT.RooRealVar("alpha","alpha",0.1,0.,1.5) #after alpha*sigma, gaussian connected to power law: alpha>0 => left tail alpha<0 => right tail
      alphaR=ROOT.RooRealVar("alphaR","alphaR",2,0.1,15)#2 was already ~good
      if regions in ['BB']:
         mean=ROOT.RooRealVar("mean","mean",mean_histo,mean_histo -0.2*sigma_guessed, mean_histo + 0.2*sigma_guessed)
         n=ROOT.RooRealVar("nL","nL",2,0.1,15) #exponent of the power law tail
         nR=ROOT.RooRealVar("nR","nR",3,0.1,10)
      elif var_type in ['MC'] and regions in ['EE']:
         mean=ROOT.RooRealVar("mean","mean",mean_histo,mean_histo -0.2*sigma_guessed, mean_histo + 0.2*sigma_guessed)
         n=ROOT.RooRealVar("nL","nL",2,0.1,15) 
         nR=ROOT.RooRealVar("nR","nR",3,0.1,10)
      elif var_type in ['MC'] and regions in ['BE']:
         mean=ROOT.RooRealVar("mean","mean",mean_guessed,mean_guessed -0.2*sigma_guessed, mean_guessed + 0.2*sigma_guessed)
         n=ROOT.RooRealVar("nL","nL",3,0.1,15) 
         nR=ROOT.RooRealVar("nR","nR",3,0.1,10)
      else :
         mean=ROOT.RooRealVar("mean","mean",mean_histo,mean_histo -0.2*sigma_guessed, mean_histo + 0.2*sigma_guessed)
         n=ROOT.RooRealVar("nL","nL",3,0.1,15) 
         nR=ROOT.RooRealVar("nR","nR",4,0.1,10)

      #Simple Fitting Functions
      #fit_func=ROOT.RooCBShape("fit_func", "crystal ball", x,mean,sigma,alpha,n) 
      #fit_func=ROOT.RooDCBShape("fit_func", "double crystal ball", x, mean, sigma, alpha, alphaR, n, nR)##va abbastanza bene
      #fit_func=ROOT.RooGaussian("fit_func","gaussian",x, mean, sigma)
      #fit_func=ROOT.RooBreitWigner("dfit_func", "breit wigner", x, mean, sigma)
      #fit_func=ROOT.RooVoigtian("dfit_func", "voigtian (convolution gauss*breit wigner", x, mean,width, sigma)

      #Convolution Fit function (BW + dCB)
      bwMean=ROOT.RooRealVar("m_{Z}","BW Mean", 91.1876, "GeV") 
      bwWidth=ROOT.RooRealVar("#Gamma_{Z}", "BW Width", 2.4952, "GeV") 
      #Keep Breit-Wigner parameters fixed to the PDG values                                                                                                    
      bwMean.setConstant(ROOT.kTRUE); 
      bwWidth.setConstant(ROOT.kTRUE); 
      bw=ROOT.RooBreitWigner("bw", "breit wigner", x, bwMean, bwWidth)

      #mean   = ROOT.RooRealVar("mean", "Double CB Bias", -.2, -20, 20, "GeV");
      mean      = ROOT.RooRealVar("mean", "Double CB Bias", -1., -4, 4);
      sigma     = ROOT.RooRealVar("sigma", "Double CB Width", 2., 0.5, 4.);
      dCBCutL   = ROOT.RooRealVar("al_{DCB}", "Double CB Cut left", 1., 0.1, 50.);
      dCBCutR   = ROOT.RooRealVar("ar_{DCB}", "Double CB Cut right", 1., 0.1, 50.);
      dCBPowerL = ROOT.RooRealVar("nl_{DCB}", "Double CB Power left", 2., 0.2, 50.);
      dCBPowerR = ROOT.RooRealVar("nr_{DCB}", "Double CB Power right", 2., 0.2, 50.);
      dcb       = ROOT.RooDCBShape("dcb", "double crystal ball", x, mean, sigma, dCBCutL, dCBCutR, dCBPowerL, dCBPowerR)

      fit_func = ROOT.RooFFTConvPdf("fit_func","bw (X) dcb",x,bw,dcb)
      
      fit_func.fitTo(dh)

      res=fit_func.fitTo(dh,RooFit.Save()) #This is the general way of handling fit results
      mean_fit=res.floatParsFinal().find("mean").getVal()
      mean_fit_error=res.floatParsFinal().find("mean").getError()
      sigma_fit=res.floatParsFinal().find("sigma").getVal()
      sigma_fit_error=res.floatParsFinal().find("sigma").getError()
      #write fit parameters on file
      file_res = open(str('../Extra_sigma/fit_extra_sigma_'+var_type+'_'+regions+'.dat'),'w+')
      file_res.write("%lf %lf %lf %lf\n"%(mean_fit,mean_fit_error,sigma_fit/bwMean.getVal(),sigma_fit_error/bwMean.getVal()))

      #Plot and save the fit
      if var_type in ['MC']: 
         fit_func.plotOn(frame,RooFit.LineColor(ROOT.kRed))
      else:
         fit_func.plotOn(frame) # default color is kBlue
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
      
      #frame.SetYTitle("test") # change y title
      frame.Draw() 
      text.Draw()
      entry.Draw()
      mean_label.Draw()
      sigma_label.Draw()
      cms.Draw()

      c.SaveAs(str('../Extra_sigma/'+hist_res.GetName()+'.png'))
      c.SaveAs(str('../Extra_sigma/'+hist_res.GetName()+'.pdf'))

os.system("source ./sigma_extra_publisher.sh")              
print "python ../Extra_sigma/sigma_extra.py"
#os.system("python ../Extra_sigma/sigma_extra.py") # Ma perche' cazzo non funziona????
#os.system("python /user/gfasanel/HEEP/CMSSW_7_2_0_patch1/src/Mass_resolution/Extra_sigma")










