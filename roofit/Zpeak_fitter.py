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
lumi_value=36.46
#for var_type in ['data','MC']:
#for var_type in ['MC']:
for var_type in ['data']:
   #for regions in ['BB','BE','EE']:
   for regions in ['BB','BE']:
   #for regions in ['BE']:
      if var_type=='MC':
         file_mass=ROOT.TFile('/user/gfasanel/Mass_resolution_study/Extra_sigma/Histos/MC_Zpeak_2016_Moriond17.root','READ')
      else:
         file_mass=ROOT.TFile('/user/gfasanel/Mass_resolution_study/Extra_sigma/Histos/data_Zpeak_2016_runB-H_Moriond17.root','READ')
      hist_res   = file_mass.Get(str('h_mee_'+var_type+'_'+regions))
      #hist_res.Rebin(3) #1.5 GeV binning
      #hist_res.Rebin(2) #0.75 GeV binning
      max=hist_res.GetXaxis().GetBinCenter(hist_res.GetMaximumBin())
      mean_histo=hist_res.GetMean()
      #x=ROOT.RooRealVar("x","m_{ee} [GeV]",60,120)
      x=ROOT.RooRealVar("x","m_{ee} [GeV]",80,100)
      #x.setRange("myRange",80,100) ->non funcica
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

      mean      = ROOT.RooRealVar("mean", "Double CB Bias", (max - 91.1876), -1, 1)
      sigma     = ROOT.RooRealVar("sigma", "Double CB Width", 2., 0.5, 4.)
      #sigma     = ROOT.RooRealVar("sigma", "Double CB Width", 2.27, 1.5, 3)
      if (var_type in 'data' and regions in 'BE'): 
         sigma     = ROOT.RooRealVar("sigma", "Double CB Width", 2.27, 2.27, 2.27)
      dCBCutL   = ROOT.RooRealVar("al_{DCB}", "Double CB Cut left", 3., 0.1, 50.)
      dCBCutR   = ROOT.RooRealVar("ar_{DCB}", "Double CB Cut right", 3., 0.1, 50.)
      dCBPowerL = ROOT.RooRealVar("nl_{DCB}", "Double CB Power left", 0.5, 0.1, 50.)
      dCBPowerR = ROOT.RooRealVar("nr_{DCB}", "Double CB Power right", 1., 0.1, 50.)

      #ad hoc changes (if needed)
      #if regions in ['BB'] and var_type in ['data']:
       #  mean      = ROOT.RooRealVar("mean", "Double CB Bias", 0.2, -4, 4);
        # sigma     = ROOT.RooRealVar("sigma", "Double CB Width", 3, 0.5, 4.);

      dcb       = ROOT.RooDCBShape("dcb", "double crystal ball", x, mean, sigma, dCBCutL, dCBCutR, dCBPowerL, dCBPowerR)

      fit_func = ROOT.RooFFTConvPdf("fit_func","bw (X) dcb",x,bw,dcb)

      fit_func.fitTo(dh)

      res=fit_func.fitTo(dh,RooFit.Save())
      mean_fit=res.floatParsFinal().find("mean").getVal()
      mean_fit_error=res.floatParsFinal().find("mean").getError()
      if mean_fit_error==0:
         mean_fit_error=0.01
      sigma_fit=res.floatParsFinal().find("sigma").getVal()
      sigma_fit_error=res.floatParsFinal().find("sigma").getError()
      if sigma_fit_error==0:
         sigma_fit_error=0.01
      alphaL=res.floatParsFinal().find("al_{DCB}").getVal()
      alphaL_error=res.floatParsFinal().find("al_{DCB}").getError()
      alphaR=res.floatParsFinal().find("ar_{DCB}").getVal()
      alphaR_error=res.floatParsFinal().find("ar_{DCB}").getError()
      nL=res.floatParsFinal().find("nl_{DCB}").getError()
      nL_error=res.floatParsFinal().find("nl_{DCB}").getError()
      nR=res.floatParsFinal().find("nr_{DCB}").getError()
      nR_error=res.floatParsFinal().find("nr_{DCB}").getError()

      file_res = open(str('/user/gfasanel/Mass_resolution_study/Extra_sigma/fit_extra_sigma_2016_'+var_type+'_'+regions+'.dat'),'w+')
      file_res.write("%lf %lf %lf %lf %lf\n"%(mean_fit,mean_fit_error,sigma_fit/bwMean.getVal(),sigma_fit_error/bwMean.getVal(),ROOT.EffSigma(hist_res)/bwMean.getVal()))
      #file_res.write("%lf %lf %lf %lf %lf\n"%(mean_fit,mean_fit_error,sigma_fit/(bwMean.getVal() + mean_fit),sigma_fit_error/(bwMean.getVal()+mean_fit),ROOT.EffSigma(hist_res)/(bwMean.getVal()+mean_fit)))

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
      sigma_label =ROOT.TLatex(0.2,0.8,"sigma = %.2f #pm %.2f"%(sigma_fit,sigma_fit_error))
      sigma_label.SetNDC()
      sigma_label.SetTextSize(0.04)
      alphaL_label =ROOT.TLatex(0.2,0.75,"aL = %.2f #pm %.2f"%(alphaL,alphaL_error))
      alphaL_label.SetTextSize(0.04)
      alphaL_label.SetNDC()
      nL_label =ROOT.TLatex(0.2,0.7,"nL = %.2f #pm %.2f"%(nL,nL_error))
      nL_label.SetNDC()
      nL_label.SetTextSize(0.04)
      alphaR_label =ROOT.TLatex(0.2,0.65,"aR = %.2f #pm %.2f"%(alphaR,alphaR_error))
      alphaR_label.SetTextSize(0.04)
      alphaR_label.SetNDC()
      nR_label =ROOT.TLatex(0.2,0.6,"nR = %.2f #pm %.2f"%(nR,nR_error))
      nR_label.SetNDC()
      nR_label.SetTextSize(0.04)

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
      #alphaL_label.Draw()
      #nL_label.Draw()
      #alphaR_label.Draw()
      #nR_label.Draw()

      cms.Draw()
      region.Draw()
      lumi.Draw()

      c.SaveAs(str('/user/gfasanel/Mass_resolution_study/Extra_sigma/'+hist_res.GetName()+'_2016_Moriond17.png'))
      c.SaveAs(str('/user/gfasanel/Mass_resolution_study/Extra_sigma/'+hist_res.GetName()+'_2016_Moriond17.pdf'))

print "[STATUS] Calling python /user/gfasanel/Mass_resolution_study/Extra_sigma/sigma_extra.py"
os.system("mv /user/gfasanel/Mass_resolution_study/Extra_sigma/*.png ~/public_html/Res_scale_Moriond17/Extra_sigma/")
os.system("mv /user/gfasanel/Mass_resolution_study/Extra_sigma/*.pdf ~/public_html/Res_scale_Moriond17/Extra_sigma/")
print "Plots are moved here ~/public_html/Res_scale_16_Moriond17/Extra_sigma/"
print "Now, write your .txt and latex table with:"
print "python ../Extra_sigma/sigma_extra.py"







