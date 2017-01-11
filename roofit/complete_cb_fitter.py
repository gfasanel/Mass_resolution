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
#short options that requires an argument are followed by :, long options requiring an argument are followed by =
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
   file_res_BB = open(str('../Resolution/histograms_mass_'+var_type+'_BB.txt'),'w+')
   file_res_BE = open(str('../Resolution/histograms_mass_'+var_type+'_BE.txt'),'w+')
   file_res_EE = open(str('../Resolution/histograms_mass_'+var_type+'_EE.txt'),'w+')
   file_scale_BB = open('../Resolution/histograms_mass_'+scale_type+'_BB.txt','w+')
   file_scale_BE = open('../Resolution/histograms_mass_'+scale_type+'_BE.txt','w+') 
   file_scale_EE = open('../Resolution/histograms_mass_'+scale_type+'_EE.txt','w+')

hBase_mee_mr = file_mass.Get('hBase_mee_mr') #Taken from the file, binning decided in histos_.py

print "################################### FITTING PROCEDURE ############################################"

for regions in ['BB','BE','EE']:
     for i in range(1, hBase_mee_mr.GetNbinsX()+1):# for each mass bin
     #now you can edit the binning as you wish
     #the last one is 23
     #print "you are fitting",var_type,"in the region",regions
     #binning=[1,2,3,4,5,7,9,11,13,15,17,19,21,23] 
     #if regions=='BB':
     #   binning=[1,2,3,4,5,7,9,11,13,15,17,19,21,23]
     #if regions=='BE':
     #   binning=[1,2,3,4,5,7,9,13,17,23]
     #if regions=='EE':
     #   binning=[1,3,5,9,18,23]
     #for i in binning[0:-1]:#0 is the first entry, -1 is the last one
     #   print "index is",i
     #   print "This will be BIN", binning.index(i)
     #   #if(i<5):
        hist_res   = file_mass.Get(str('h_'+var_type+'_'+regions+'_%d'%i))
        #j=i + 1
        #while j< binning[binning.index(i)+1]:
        #   print "Adding bin ",j
        #   hist_res2    = file_mass.Get(str('h_'+var_type+'_'+regions+'_%d'%j))
        #   hist_res.Add(hist_res2)
        #   j+=1


        #if(regions in ['BE','EE'] and ('scale' in var_type)) : #for scale_BE,EE and scale_supercluster_BE,EE, you need to rebin (otherwise it's overbinned) 
        #   hist_res.Rebin(2)
        #if(regions in ['BE','EE'] and ('scale_supercluster' in var_type)) : #scale supercluster needs rebin(4)
           ##if(binning.index(i)!=0 and binning.index(i)!=1): #Consider not to rebin the first 2 histo
        #   hist_res.Rebin(2)
           
        #hist_res.Rebin(2)

        # Declare observable x
        if('res' in var_type): #If substring 'res' is in var_type
           #x=ROOT.RooRealVar("x","(m_{reco}-m_{gen})/m_{gen}",max-1.5*hist_res.GetRMS(),max+1.5*hist_res.GetRMS())  #name, title, range: you can use ("x","my x variable",-10,10)
           x=ROOT.RooRealVar("x","(m_{reco}-m_{gen})/m_{gen}",-0.1,+0.06)  #name, title, range: you can use ("x","my x variable",-10,10)
           #x=ROOT.RooRealVar("x","(m_{reco}-m_{gen})/m_{gen}",-0.02,+0.02)
           #if(var_type=='resolution_supercluster' and regions=='BE'):
           #   x=ROOT.RooRealVar("x","(m_{reco}-m_{gen})/m_{gen}",max-2*hist_res.GetRMS(),max+1*hist_res.GetRMS())  #name, title, range: you can use ("x","my x variable",-10,10)

        #if('scale' in var_type):
           #x=ROOT.RooRealVar("x","m_{reco}/m_{gen}",hist_res.GetMean()-2*hist_res.GetRMS(),hist_res.GetMean()+2*hist_res.GetRMS())
           #x=ROOT.RooRealVar("x","m_{reco}/m_{gen}",max-2*hist_res.GetRMS(),max+2*hist_res.GetRMS())  #name, title, range: you can use ("x","my x variable",-10,10)
        # Create a binned dataset (RooDataHist) that imports contents of TH1 and associates its contents to observable 'x'

        dh=ROOT.RooDataHist("dh","dh",RooArgList(x), hist_res)  #Without RooArgList it doesn't work

        # P l o t   a n d   f i t   a   R o o D a t a H i s t
        # ---------------------------------------------------

        # Make plot of binned dataset showing Poisson error bars (RooFit default)
        frame = x.frame(RooFit.Name(""),RooFit.Title(" ")) #Title(" ") takes away "Rooplot of x"
        #frame is a RooPlot generated from the RooRealVar x
        #to change x range: RooFit.Range(xmin,xmax)
        #RooFit.Range(max-1.5*hist_res.GetRMS(),max+1.5*hist_res.GetRMS())
        #RooFit.Range("test",-0.02,0.02)
        #x.setRange("test",-0.02,0.02)
        frame.SetMaximum(2*hist_res.GetMaximum())

        dh.plotOn(frame)  

        mean_guessed=hist_res.GetXaxis().GetBinCenter(hist_res.GetMaximumBin())
        #sigma_guessed=min([0.01,hist_res.GetRMS()])
        #sigma_guessed=min([0.003,hist_res.GetRMS()])
        #sigma_guessed=0.003
        sigma_guessed=0.01
        #mean=ROOT.RooRealVar("mean","mean",mean_guessed) #Initial guess, lower bound, upper bound
        #mean.setConstant(ROOT.kTRUE)
        mean=ROOT.RooRealVar("mean","mean",mean_guessed,mean_guessed -1.5*sigma_guessed, mean_guessed + 1.5*sigma_guessed) #Initial guess, lower bound, upper bound 
        #if 'scale' in var_type:##
        #   sigma_guessed=min([0.005,hist_res.GetRMS()])##
        #   mean=ROOT.RooRealVar("mean","mean",mean_guessed,mean_guessed -0.5*sigma_guessed, mean_guessed + 0.5*sigma_guessed) #Initial guess, lower bound, upper bound 

        #Some tuning needed in particular bins
        #if(var_type=='scale' and regions=='BE' and binning.index(i)==3):
        #   mean=ROOT.RooRealVar("mean","mean",mean_guessed,mean_guessed -0.3*sigma_guessed, mean_guessed + 0.3*sigma_guessed) #Initial guess, lower bound, upper bound 

        #if(regions=='BB'):
        #   sigma=ROOT.RooRealVar("sigma","sigma",sigma_guessed,0.,0.023) #Don't touch 0.023, it's dangerous
        #if(regions=='BE'):
        #   sigma=ROOT.RooRealVar("sigma","sigma",sigma_guessed,0.,0.027) #Don't touch 0.027, it's dangerous
        
        #sigma=ROOT.RooRealVar("sigma","sigma",sigma_guessed,0.,0.05)
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

        if("resolution" in var_type):
           c.SaveAs(str('~/public_html/Res_scale_15/fit_results/resolution_'+regions+'/'+hist_res.GetName()+'.png'))
           c.SaveAs(str('~/public_html/Res_scale_15/fit_results/resolution_'+regions+'/'+hist_res.GetName()+'.pdf'))

        #Save Parameters in a txt file
        if('res' in var_type): # if var_type contains 'res'
           if regions=='BB':
              file_res_BB.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i), sigma_fit, sigma_fit_error))
              file_scale_BB.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i), mean_fit + 1., mean_fit_error))
           elif regions=='BE':
              file_res_BE.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i), sigma_fit, sigma_fit_error))
              file_scale_BE.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i), mean_fit + 1., mean_fit_error))
  
           elif regions=='EE':
              file_res_EE.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i), sigma_fit, sigma_fit_error))
              file_scale_EE.write("%lf %lf %lf %lf\n"%(hBase_mee_mr.GetBinCenter(i), hBase_mee_mr.GetBinCenter(i) - hBase_mee_mr.GetBinLowEdge(i), mean_fit + 1., mean_fit_error))













