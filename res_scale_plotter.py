#! /usr/bin/python
import math
from array import array
import os
import ROOT
import numpy as np

ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetFrameBorderMode(ROOT.kWhite)
ROOT.gStyle.SetFrameFillColor(ROOT.kWhite)
ROOT.gStyle.SetCanvasBorderMode(ROOT.kWhite)
ROOT.gStyle.SetCanvasColor(ROOT.kWhite)
ROOT.gStyle.SetPadBorderMode(ROOT.kWhite)
ROOT.gStyle.SetPadColor(ROOT.kWhite)
ROOT.gStyle.SetStatColor(ROOT.kWhite)
ROOT.gStyle.SetErrorX(0)

import sys,getopt

def main(argv):# defining the main function, called later
   try:
      opts, args = getopt.getopt(argv,"ht:",["type="])#getopt takes three args: a list (argv),short options, long options
   except getopt.GetoptError:
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'python res_scale_plotter.py -t #'
         sys.exit()
      elif opt in ("-t","--type"):
         global _t #defining a global variable _t
         _t=arg

if __name__ == "__main__":
   main(sys.argv[1:]) 

lumi_value=12.4
#variable_type='resolution'
#variable_type='resolution_supercluster'
#variable_type=scale
#variable_type=scale_supercluster
#variable_type='HoverE'
#variable_type='resolution_HoE_cut'
#variable_type='scale_HoE_cut'

variable_type=_t

mass={}
mass_err={}
res={}
res_err={}#error on the resolution
res_noExtra={}
res_noExtra_err={}

for regions in ['BB','BE','EE']:
    mass[regions]=[]
    mass_err[regions]=[]
    res[regions]=[]
    res_err[regions]=[]
    res_noExtra[regions]=[]
    res_noExtra_err[regions]=[]

Regions=['BB','BE']

#opern the file and take the numbers
for regions in Regions:
    with open(str('Resolution/histograms_mass_'+variable_type+'_'+regions+'.txt')) as file_res:
        print str('Resolution/histograms_mass_'+variable_type+'_'+regions+'.txt')
        for line in file_res: 
            numbers_str = line.split()    #convert numbers to floats   
            numbers_float = map(float, line.split())
            mass[regions].append(numbers_float[0])
            mass_err[regions].append(numbers_float[1])
            #mass_err[regions].append(0)
            if variable_type in ['resolution','resolution_supercluster','resolution_h_recover']: # you have the extra sigma to add in quadrature
               print "[STATUS] Adding extra sigma for resolution"
               with open(str('Extra_sigma/final_extra_sigma_2016_'+regions+'.dat')) as file_extra_sigma:
                  for line in file_extra_sigma:
                     # split the string on whitespace, return a list of numbers as strings
                     sigmas_str = line.split()  
                     sigmas_float = map(float, line.split())
                     extra_sigma=sigmas_float[0]
                     extra_sigma_error=sigmas_float[1]

               final_sigma      =ROOT.sqrt(extra_sigma*extra_sigma + numbers_float[2]*numbers_float[2])
               final_sigma_error=ROOT.sqrt(ROOT.pow(extra_sigma*extra_sigma_error/final_sigma,2) + pow(numbers_float[2]*numbers_float[3]/final_sigma,2))
               if regions in ['BB']:#remove it when you are sure
                  print final_sigma, final_sigma_error, extra_sigma, extra_sigma_error, extra_sigma*extra_sigma_error/final_sigma
               res[regions].append(final_sigma*100) # To be in percentage
               res_err[regions].append(final_sigma_error*100)
               res_noExtra[regions].append(numbers_float[2]*100) # MC only
               res_noExtra_err[regions].append(numbers_float[3]*100)
            else:
               res[regions].append(numbers_float[2]) # MC only
               res_err[regions].append(numbers_float[3])

#usage of array for TGraph, otherwise it doesn't work
mass_array={}
mass_err_array={}
res_array={}
res_err_array={}
res_graph={}
res_noExtra_graph={}

for regions in Regions:
    mass_array[regions] =array("d",mass[regions])
    mass_err_array[regions] =array("d",mass_err[regions])
    res_array[regions] =array("d",res[regions])
    res_err_array[regions] =array("d",res_err[regions])
    res_graph[regions]=ROOT.TGraphErrors(len(mass_array[regions]),mass_array[regions],res_array[regions],mass_err_array[regions],res_err_array[regions])

canvas={}
canvas['BB']=ROOT.TCanvas(str(variable_type+"_BB"),str(variable_type+"_BB"))
canvas['BE']=ROOT.TCanvas(str(variable_type+"_BE"),str(variable_type+"_BE"))
#canvas['EE']=ROOT.TCanvas(str(variable_type+"_EE"),str(variable_type+"_EE"))

file_out= ROOT.TFile(str("Resolution/"+variable_type+"_plot_2016.root"),"RECREATE")

file_out.cd()
for regions in Regions:
    canvas[regions].cd()
    canvas[regions].SetLeftMargin(0.13)
    res_graph[regions].SetMarkerSize(0.8)
    res_graph[regions].SetMarkerStyle(20)
    res_graph[regions].GetXaxis().SetTitleSize(0.042)
    res_graph[regions].GetXaxis().SetTitle('m_{gen} [GeV]')
    res_graph[regions].GetYaxis().SetTitleSize(0.052)
    res_graph[regions].GetYaxis().SetTitle('#sqrt{#sigma_{fit}^{2} + #sigma_{extra}^{2}} [%]')
    if variable_type=='HoverE':
        res_graph[regions].GetYaxis().SetTitle('H_{1}/E_{1} + H_{2}/E_{2}')
    if variable_type=='HTotoverETot':
        res_graph[regions].GetYaxis().SetTitle('(H_{1} + H_{2})/(E_{1} + E_{2})')
    if 'scale' in variable_type:
        res_graph[regions].GetYaxis().SetTitle('mass scale')
        res_graph[regions].GetYaxis().SetRangeUser(0.98,1.01)
    ###Fitting resolution and superimpose fit function
    res_graph[regions].Draw("APE")
    res_graph[regions].GetXaxis().SetRangeUser(0.,4500) # Above this SATURATION

    if variable_type == "resolution":
       print "fitting resolution in region ",regions
       res_graph[regions].GetYaxis().SetRangeUser(0.7,4.)
       if regions in ['EE']:
          res_graph[regions].GetYaxis().SetRangeUser(1.,5.5)
       x1=res_graph[regions].GetXaxis().GetBinLowEdge(res_graph[regions].GetXaxis().GetFirst())
       #x2=res_graph[regions].GetXaxis().GetBinUpEdge(res_graph[regions].GetXaxis().GetLast())
       x2=5250
       func=ROOT.TF1("func","sqrt([0]*[0]/x + ([1]*[1])/(x*x) + [2]*[2]) + [3]*x",x1,x2)
       if regions in ['BE','EE']:
          func=ROOT.TF1("func","sqrt([0]*[0]/x + ([1]*[1])/(x*x) + [2]*[2])",x1,x2)
       func.SetParNames("S","N","C","L")
       func.SetParameter("S",0)
       func.SetParLimits(0,0,30)
       func.SetParameter("N",0)
       func.SetParLimits(1,0,10)#N is positive
       func.SetParameter("C",1)
       if regions in ['BB']:
          func.SetParameter("L",0.00001)
          func.SetParLimits(3,0,1)#L is positive

       res_graph[regions].Fit("func","R")
       label_fit =ROOT.TLatex()
       label_fit.SetNDC()
       label_fit.SetTextSize(0.04)
       if regions in ['BB']:
          label_fit.DrawLatex(0.3,0.8,"#sqrt{#frac{S^{2}}{m_{gen}} + #frac{N^{2}}{m_{gen}^{2}} + C^{2}} + Lm_{gen}")
       else:
          label_fit.DrawLatex(0.3,0.8,"#sqrt{#frac{S^{2}}{m_{gen}} + #frac{N^{2}}{m_{gen}^{2}} + C^{2}}")
       #label_fit.DrawLatex(0.3,0.7,"#chi^{2}/ndof=%.2lf"%(func.GetChisquare()/func.GetNDF()))
       label_fit.DrawLatex(0.3,0.65,"S=%.1lf #pm %.1lf"%(func.GetParameter(0),func.GetParError(0)))
       label_fit.DrawLatex(0.3,0.6,"N=%.1lf #pm %.1lf"%(func.GetParameter(1),func.GetParError(1)))
       label_fit.DrawLatex(0.3,0.55,"C=%.2lf #pm %.2lf"%(func.GetParameter(2),func.GetParError(2)))
       if regions in ['BB']:
          label_fit.DrawLatex(0.3,0.5,"L=%.1e #pm %.1e"%(func.GetParameter(3),func.GetParError(3)))
       label_fit.Draw()
       label =ROOT.TLatex(0.12,0.95,str("CMS Internal; L= "+str(lumi_value)+" /fb (13 TeV)"))
       label.SetNDC()
       label.Draw()
       label_region =ROOT.TLatex(0.8,0.8,str(regions))
       label_region.SetNDC()
       label_region.Draw()


    if "resolution" in variable_type:
       res_noExtra_graph[regions]=ROOT.TGraphErrors(len(mass_array[regions]),mass_array[regions],np.asarray(res_noExtra[regions]),mass_err_array[regions],np.asarray(res_noExtra_err[regions]))
       res_noExtra_graph[regions].SetMarkerSize(1.2)
       res_noExtra_graph[regions].SetMarkerStyle(20)
       res_noExtra_graph[regions].GetXaxis().SetTitleSize(0.042)
       res_noExtra_graph[regions].GetXaxis().SetTitle('m_{gen} [GeV]')
       res_noExtra_graph[regions].GetYaxis().SetTitleSize(0.052)
       res_noExtra_graph[regions].GetYaxis().SetTitle('#sigma_{fit} [%]')
       canvas_noExtra=ROOT.TCanvas("noExtra","noExtra");
       res_noExtra_graph[regions].Draw("APE")
       canvas_noExtra.SaveAs(('~/public_html/Res_scale_16/fit_results/resolution_'+regions+'/'+variable_type+'_noExtra_'+regions+'.png'))


    ##This is for scale basically (quick and dirty, I know)
    label_ =ROOT.TLatex(0.12,0.95,str("CMS Internal; L= "+str(lumi_value)+" /fb (13 TeV)"))
    label_.SetNDC()
    label_.Draw()
    label_region_ =ROOT.TLatex(0.3,0.7,str(regions))
    label_region_.SetNDC()
    label_region_.Draw()


    if ("scale" in variable_type) or ("resolution" in variable_type):
       canvas[regions].Print(str('~/public_html/Res_scale_16/fit_results/resolution_'+regions+'/'+variable_type+'_'+regions+'.png'))
       canvas[regions].Print(str('~/public_html/Res_scale_16/fit_results/resolution_'+regions+'/'+variable_type+'_'+regions+'.pdf'))
       canvas[regions].Print(str('~/public_html/Res_scale_16/fit_results/resolution_'+regions+'/'+variable_type+'_'+regions+'.eps'))

       if (variable_type=='resolution') or (variable_type=='scale'):
          canvas[regions].Print(str('~/public_html/Res_scale_16/fit_results/'+variable_type+'_'+regions+'.png'))
          canvas[regions].Print(str('~/public_html/Res_scale_16/fit_results/'+variable_type+'_'+regions+'.pdf'))
          canvas[regions].Print(str('~/public_html/Res_scale_16/fit_results/'+variable_type+'_'+regions+'.eps'))
    elif (("HoverE" in variable_type) or  ("HTotoverETot" in variable_type)):
       canvas[regions].Print(str('~/public_html/Res_scale_16/fit_results/HoverE/'+variable_type+'_'+regions+'.png'))
       canvas[regions].Print(str('~/public_html/Res_scale_16/fit_results/HoverE/'+variable_type+'_'+regions+'.pdf'))
       canvas[regions].Print(str('~/public_html/Res_scale_16/fit_results/HoverE/'+variable_type+'_'+regions+'.eps'))
    else:
       canvas[regions].Print(str('~/public_html/Res_scale_16/fit_results/'+variable_type+'_'+regions+'.png'))
       canvas[regions].Print(str('~/public_html/Res_scale_16/fit_results/'+variable_type+'_'+regions+'.pdf'))
       canvas[regions].Print(str('~/public_html/Res_scale_16/fit_results/'+variable_type+'_'+regions+'.eps'))

