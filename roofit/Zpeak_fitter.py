#python Zpeak_fitter.py
import ROOT
import math
import os
ROOT.gSystem.Load("libRooFit")
ROOT.gSystem.Load("RooDCBShape_cxx.so") #This is the way to handle user defined pdf (generated with RooClassFactory). Compile once and for all in ROOT and then add it as a library
ROOT.gSystem.Load("../rootlogon_style_C.so")
ROOT.rootlogon_style()
from ROOT import RooFit, RooRealVar, RooGaussian, RooDataSet, RooArgList, RooTreeData, RooArgSet
ROOT.gROOT.SetBatch(ROOT.kTRUE) 

import sys,getopt

print "################################### FITTING THE Z PEAK ############################################"
for var_type in ['data','MC']:
   for regions in ['BB','BE','EE']:
      if var_type=='MC':
         file_mass=ROOT.TFile('/user/gfasanel/Mass_resolution_study/Extra_sigma/MC_Zpeak.root','READ')
      else:
         file_mass=ROOT.TFile('/user/gfasanel/Mass_resolution_study/Extra_sigma/data_Zpeak.root','READ')
      hist_res   = file_mass.Get(str('h_mee_'+var_type+'_'+regions))
      hist_res.Rebin(3) #1.5 GeV binning
      max=hist_res.GetXaxis().GetBinCenter(hist_res.GetMaximumBin())
      mean_histo=hist_res.GetMean()
      x=ROOT.RooRealVar("x","m_{ee} [GeV]",60,120)
      dh=ROOT.RooDataHist("dh","dh",RooArgList(x), hist_res)

      # Make plot of binned dataset showing Poisson error bars (RooFit default)
      frame = x.frame(RooFit.Name(""),RooFit.Title(" ")) #Title(" ") takes away "Rooplot of x"
      #frame is a RooPlot generated from the RooRealVar x
      #to change x range: RooFit.Range(xmin,xmax)
      frame.SetMaximum(2*hist_res.GetMaximum())
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
      #dCBCutL   = ROOT.RooRealVar("al_{DCB}", "Double CB Cut left", 1., 0.1, 1000.);
      #dCBCutR   = ROOT.RooRealVar("ar_{DCB}", "Double CB Cut right", 1., 0.1, 1000.);
      #dCBPowerL = ROOT.RooRealVar("nl_{DCB}", "Double CB Power left", 2., 0.2, 1000.);
      #dCBPowerR = ROOT.RooRealVar("nr_{DCB}", "Double CB Power right", 2., 0.2, 1000.);
      if regions in ['BB'] and var_type in ['data']:
         mean      = ROOT.RooRealVar("mean", "Double CB Bias", 0.3, -4, 4);
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
      #write fit parameters on file
      file_res = open(str('/user/gfasanel/Mass_resolution_study/Extra_sigma/fit_extra_sigma_'+var_type+'_'+regions+'.dat'),'w+')
      file_res.write("%lf %lf %lf %lf\n"%(mean_fit,mean_fit_error,sigma_fit/bwMean.getVal(),sigma_fit_error/bwMean.getVal()))

      #Plot and save the fit
      if var_type in ['MC']: 
         fit_func.plotOn(frame,RooFit.LineColor(ROOT.kRed))
      else:
         fit_func.plotOn(frame) # default color is kBlue
      #I want to save the histogram and the fit in a file: how is it done? RooWorkSpace?? Add this later
      c = ROOT.TCanvas("fit","fit",800,800) #X length, Y length
      c.cd()
      #c.SetLogy()
      mean_label =ROOT.TLatex(0.14,0.85,"mean = %.4f #pm %.4f"%(mean_fit,mean_fit_error))
      mean_label.SetTextSize(0.04)
      mean_label.SetNDC()
      chi2=frame.chiSquare()
      sigma_label =ROOT.TLatex(0.14,0.8,"sigma = %.4f #pm %.4f"%(sigma_fit,sigma_fit_error))
      sigma_label.SetNDC()
      sigma_label.SetTextSize(0.04)
      chi2=frame.chiSquare()

      text= ROOT.TLatex(0.14,0.75,"#chi^{2}_{reduced} = %.2f" %chi2)
      text.SetNDC()
      text.SetTextSize(0.04)
      entry= ROOT.TLatex(0.14,0.65,"Entries = %d" %hist_res.GetEntries())
      entry.SetNDC()
      entry.SetTextSize(0.04)

      cms =ROOT.TLatex(0.6,0.96,"CMS Internal")
      cms.SetNDC()
      cms.SetTextSize(0.04)
      
      #frame.SetYTitle("test") # change y title
      #frame.SetLabelOffset(0.03,"Y")
      frame.Draw() 
      #text.Draw() #chi2_reduced
      entry.Draw()
      mean_label.Draw()
      sigma_label.Draw()
      cms.Draw()

      c.SaveAs(str('/user/gfasanel/Mass_resolution_study/Extra_sigma/'+hist_res.GetName()+'.png'))
      c.SaveAs(str('/user/gfasanel/Mass_resolution_study/Extra_sigma/'+hist_res.GetName()+'.pdf'))

print "[STATUS] Calling python /user/gfasanel/Mass_resolution_study/Extra_sigma/sigma_extra.py"
os.system("cp /user/gfasanel/Mass_resolution_study/Extra_sigma/*.png ~/public_html/Res_scale_15/Extra_sigma/")
os.system("cp /user/gfasanel/Mass_resolution_study/Extra_sigma/*.pdf ~/public_html/Res_scale_15/Extra_sigma/")
#os.system("source ./roofit/sigma_extra_publisher.sh")#to publish on lxplus
#os.system("python /user/gfasanel/Mass_resolution_study/Extra_sigma/sigma_extra.py") # Ma perche' cazzo non funziona????
print "Now, write your .txt and latex table with:"
print "python ../Extra_sigma/sigma_extra.py"







