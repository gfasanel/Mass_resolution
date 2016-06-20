#python Zpeak_fitter.py
import ROOT
import math
import os
ROOT.gSystem.Load("libRooFit")
ROOT.gSystem.Load("RooDCBShape_cxx.so") #This is the way to handle user defined pdf (generated with RooClassFactory). Compile once and for all in ROOT and then add it as a library
ROOT.gSystem.Load("rootlogon_style_C.so")
ROOT.gSystem.Load("../EffSigma/EffSigma_C.so")
ROOT.rootlogon_style()
from ROOT import RooFit, RooRealVar, RooGaussian, RooDataSet, RooArgList, RooTreeData, RooArgSet
ROOT.gROOT.SetBatch(ROOT.kTRUE) 

import sys,getopt

print "################################### FITTING THE Z PEAK ############################################"
lumi_value=2.6
for var_type in ['data','MC']:
#for var_type in ['data']:
   for regions in ['BB','BE','EE']:
   #for regions in ['BB']:
      if var_type=='MC':
         #file_mass=ROOT.TFile('/user/gfasanel/Mass_resolution_study/Extra_sigma/MC_Zpeak.root','READ')
         file_mass=ROOT.TFile('/user/gfasanel/Mass_resolution_study/Extra_sigma/MC_Zpeak_2016.root','READ')
      else:
         #file_mass=ROOT.TFile('/user/gfasanel/Mass_resolution_study/Extra_sigma/data_Zpeak.root','READ')
         file_mass=ROOT.TFile('/user/gfasanel/Mass_resolution_study/Extra_sigma/data_Zpeak_2016.root','READ')
      hist_res   = file_mass.Get(str('h_mee_'+var_type+'_'+regions))
      hist_res.Rebin(3) #1.5 GeV binning
      max=hist_res.GetXaxis().GetBinCenter(hist_res.GetMaximumBin())
      mean_histo=hist_res.GetMean()
      x=ROOT.RooRealVar("x","m_{ee} [GeV]",60,120)
      dh=ROOT.RooDataHist("dh","dh",RooArgList(x), hist_res)

      frame = x.frame(RooFit.Name(""),RooFit.Title(" ")) 
      frame.SetMaximum(1.5*hist_res.GetMaximum())
      dh.plotOn(frame)  

      #Convolution Fit function (BW + dCB)
      bwMean=ROOT.RooRealVar("m_{Z}","BW Mean", 91.1876, "GeV") 
      bwWidth=ROOT.RooRealVar("#Gamma_{Z}", "BW Width", 2.4952, "GeV") 
      #Keep Breit-Wigner parameters fixed to the PDG values                                                                                                    
      bwMean.setConstant(ROOT.kTRUE); 
      bwWidth.setConstant(ROOT.kTRUE); 
      bw=ROOT.RooBreitWigner("bw", "breit wigner", x, bwMean, bwWidth)

      mean      = ROOT.RooRealVar("mean", "Double CB Bias", -1., -4, 4);
      sigma     = ROOT.RooRealVar("sigma", "Double CB Width", 2., 0.5, 4.);
      dCBCutL   = ROOT.RooRealVar("al_{DCB}", "Double CB Cut left", 1., 0.1, 50.);
      dCBCutR   = ROOT.RooRealVar("ar_{DCB}", "Double CB Cut right", 1., 0.1, 50.);
      dCBPowerL = ROOT.RooRealVar("nl_{DCB}", "Double CB Power left", 2., 0.2, 50.);
      dCBPowerR = ROOT.RooRealVar("nr_{DCB}", "Double CB Power right", 2., 0.2, 50.);

      #ad hoc changes
      if regions in ['BB'] and var_type in ['data']:
         mean      = ROOT.RooRealVar("mean", "Double CB Bias", 0.2, -4, 4);
         sigma     = ROOT.RooRealVar("sigma", "Double CB Width", 3, 0.5, 4.);
         dCBPowerL = ROOT.RooRealVar("nl_{DCB}", "Double CB Power left", 2., 0.2, 1000.);
      dcb       = ROOT.RooDCBShape("dcb", "double crystal ball", x, mean, sigma, dCBCutL, dCBCutR, dCBPowerL, dCBPowerR)

      fit_func = ROOT.RooFFTConvPdf("fit_func","bw (X) dcb",x,bw,dcb)
      fit_func.fitTo(dh)

      res=fit_func.fitTo(dh,RooFit.Save())
      mean_fit=res.floatParsFinal().find("mean").getVal()
      mean_fit_error=res.floatParsFinal().find("mean").getError()
      sigma_fit=res.floatParsFinal().find("sigma").getVal()
      sigma_fit_error=res.floatParsFinal().find("sigma").getError()
      file_res = open(str('/user/gfasanel/Mass_resolution_study/Extra_sigma/fit_extra_sigma_2016_'+var_type+'_'+regions+'.dat'),'w+')
      file_res.write("%lf %lf %lf %lf %lf\n"%(mean_fit,mean_fit_error,sigma_fit/bwMean.getVal(),sigma_fit_error/bwMean.getVal(),ROOT.EffSigma(hist_res)/bwMean.getVal()))

      #Plot and save the fit
      if var_type in ['MC']: 
         fit_func.plotOn(frame,RooFit.LineColor(ROOT.kRed))
      else:
         fit_func.plotOn(frame) # default color is kBlue
      c = ROOT.TCanvas("fit","fit",800,800) #X length, Y length
      c.cd()
      #c.SetLogy()
      mean_label =ROOT.TLatex(0.2,0.85,"mean = %.2f #pm %.2f"%(mean_fit,mean_fit_error))
      mean_label.SetTextSize(0.04)
      mean_label.SetNDC()
      chi2=frame.chiSquare()
      sigma_label =ROOT.TLatex(0.2,0.8,"sigma = %.2f #pm %.2f"%(sigma_fit,sigma_fit_error))
      sigma_label.SetNDC()
      sigma_label.SetTextSize(0.04)
      chi2=frame.chiSquare()

      text= ROOT.TLatex(0.2,0.75,"#chi^{2}_{reduced} = %.2f" %chi2)
      text.SetNDC()
      text.SetTextSize(0.04)
      entry= ROOT.TLatex(0.2,0.65,"Entries = %d" %hist_res.GetEntries())
      entry.SetNDC()
      entry.SetTextSize(0.04)

      cms =ROOT.TLatex(0.6,0.96,"CMS Internal")
      cms.SetNDC()
      cms.SetTextSize(0.04)
      region =ROOT.TLatex(0.6,0.9,str(var_type+'; '+regions))
      region.SetNDC()
      region.SetTextSize(0.04)
      lumi =ROOT.TLatex(0.6,0.85,str('L= '+str(lumi_value)+" /fb"))
      lumi.SetNDC()
      lumi.SetTextSize(0.04)
      
      #frame.SetYTitle("test") # change y title
      #frame.SetLabelOffset(0.03,"Y")
      frame.Draw() 
      #text.Draw() #chi2_reduced
      #entry.Draw()
      mean_label.Draw()
      sigma_label.Draw()
      cms.Draw()
      region.Draw()
      lumi.Draw()

      c.SaveAs(str('/user/gfasanel/Mass_resolution_study/Extra_sigma/'+hist_res.GetName()+'_2016.png'))
      c.SaveAs(str('/user/gfasanel/Mass_resolution_study/Extra_sigma/'+hist_res.GetName()+'_2016.pdf'))

print "[STATUS] Calling python /user/gfasanel/Mass_resolution_study/Extra_sigma/sigma_extra.py"
os.system("mv /user/gfasanel/Mass_resolution_study/Extra_sigma/*.png ~/public_html/Res_scale_16/Extra_sigma/")
os.system("mv /user/gfasanel/Mass_resolution_study/Extra_sigma/*.pdf ~/public_html/Res_scale_16/Extra_sigma/")
print "Plots are moved here ~/public_html/Res_scale_16/Extra_sigma/"
print "Now, write your .txt and latex table with:"
print "python ../Extra_sigma/sigma_extra.py"







