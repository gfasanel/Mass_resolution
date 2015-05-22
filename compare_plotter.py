##########################################################################################m
#                                  PLOTTER RESOLUTION                                    #
##########################################################################################
# Giuseppe Fasanella (ULB)
# Contact: giuseppe.fasanella@cern.ch
##########################################################################################

import math
from array import array

##########################################################################################
#                             Import ROOT and apply settings                             #
##########################################################################################
import ROOT

ROOT.gROOT.SetBatch(ROOT.kTRUE)
#ROOT.gROOT.SetBatch(ROOT.kFALSE)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)
#ROOT.gStyle.SetFillStyle(ROOT.kWhite)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetFrameBorderMode(ROOT.kWhite)
ROOT.gStyle.SetFrameFillColor(ROOT.kWhite)
ROOT.gStyle.SetCanvasBorderMode(ROOT.kWhite)
ROOT.gStyle.SetCanvasColor(ROOT.kWhite)
ROOT.gStyle.SetPadBorderMode(ROOT.kWhite)
ROOT.gStyle.SetPadColor(ROOT.kWhite)
ROOT.gStyle.SetStatColor(ROOT.kWhite)
ROOT.gStyle.SetErrorX(0)


##########################################################################################
#PLOTTING RESOLUTION
##########################################################################################
######################Parsing arguments in python#####################
import sys,getopt #to handle arguments in python

def main(argv):# defining the main function, called later
   try:
      opts, args = getopt.getopt(argv,"ht:",["type="])#getopt takes three args: a list (argv),short options, long options
#short options that requires an argument are followed by :, long options requiring an argument are followed by =
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

#variable_type='resolution'
#variable_type=scale
#variable_type=scale_supercluster
#variable_type='HoverE'

variable_type=_t

mass={}
mass_err={}
res={}
res_err={}#error on the resolution

#Second variable
mass_2={}
mass_err_2={}
res_2={}
res_err_2={}#error on the resolution

for regions in ['BB','BE','EE']:
    mass[regions]=[]
    mass_err[regions]=[]
    res[regions]=[]
    res_err[regions]=[]

    mass_2[regions]=[]
    mass_err_2[regions]=[]
    res_2[regions]=[]
    res_err_2[regions]=[]

Regions=['BB','BE','EE']
#Regions=['BB']

#opern the file and take the numbers
for regions in Regions:
    with open(str('/user/gfasanel/public/HEEP/Eff_plots/histograms_mass_'+variable_type+'_'+regions+'.txt')) as file_res:
        for line in file_res:  #Line is a string       #split the string on whitespace, return a list of numbers
            # (as strings)                                                                               
            numbers_str = line.split()    #convert numbers to floats   
            numbers_float = map(float, line.split())
            ##numbers_float = [float(x) for x in numbers_str]  #map(float,numbers_str) works too
            mass[regions].append(numbers_float[0])
            mass_err[regions].append(0)#for the moment
            res[regions].append(numbers_float[1])
            res_err[regions].append(numbers_float[2])

    with open(str('/user/gfasanel/public/HEEP/Eff_plots/histograms_mass_'+variable_type+'_supercluster_'+regions+'.txt')) as file_res_2:
        for line in file_res_2:
            numbers_str = line.split()    #convert numbers to floats   
            numbers_float = map(float, line.split())
            ##numbers_float = [float(x) for x in numbers_str]  #map(float,numbers_str) works too
            mass_2[regions].append(numbers_float[0])
            mass_err_2[regions].append(0)#for the moment
            res_2[regions].append(numbers_float[1])
            res_err_2[regions].append(numbers_float[2])

#usage of array for TGraph, otherwise it doesn't work
mass_array={}
mass_err_array={}
res_array={}
res_err_array={}
res_graph={}

mass_array_2={}
mass_err_array_2={}
res_array_2={}
res_err_array_2={}
res_graph_2={}

MAX={}
MIN={}

for regions in Regions:
    mass_array[regions] =array("d",mass[regions])
    mass_err_array[regions] =array("d",mass_err[regions])
    res_array[regions] =array("d",res[regions])
    res_err_array[regions] =array("d",res_err[regions])
    res_graph[regions]=ROOT.TGraphErrors(len(mass_array[regions]),mass_array[regions],res_array[regions],mass_err_array[regions],res_err_array[regions])

    mass_array_2[regions] =array("d",mass_2[regions])
    mass_err_array_2[regions] =array("d",mass_err_2[regions])
    res_array_2[regions] =array("d",res_2[regions])
    res_err_array_2[regions] =array("d",res_err_2[regions])
    res_graph_2[regions]=ROOT.TGraphErrors(len(mass_array_2[regions]),mass_array_2[regions],res_array_2[regions],mass_err_array_2[regions],res_err_array_2[regions])

    #Set the maximum
    MAX[regions]=max([max(res[regions]),max(res_2[regions])])
    MIN[regions]=min([min(res[regions]),min(res_2[regions])])
    res_graph[regions].GetYaxis().SetRangeUser(MIN[regions] -0.3*MIN[regions],MAX[regions]+0.3*MAX[regions])
    if(_t=='scale'):
       res_graph[regions].GetYaxis().SetRangeUser(MIN[regions] -0.003*MIN[regions],MAX[regions]+0.01*MAX[regions])

canvas={}
canvas['BB']=ROOT.TCanvas(str(variable_type+"_BB"),str(variable_type+"_BB"))
canvas['BE']=ROOT.TCanvas(str(variable_type+"_BE"),str(variable_type+"_BE"))
canvas['EE']=ROOT.TCanvas(str(variable_type+"_EE"),str(variable_type+"_EE"))

file_out= ROOT.TFile(str("~gfasanel/public/HEEP/Eff_plots/"+variable_type+"_plot_comparison.root"),"RECREATE")

file_out.cd()
for regions in Regions:
    canvas[regions].cd()

    res_graph[regions].SetMarkerSize(1.2)
    res_graph[regions].SetMarkerStyle(20)
    res_graph[regions].GetXaxis().SetTitleSize(0.042)
    res_graph[regions].GetXaxis().SetTitle('m_{gen} [GeV]')
    res_graph[regions].GetYaxis().SetTitleSize(0.052)
    res_graph[regions].GetYaxis().SetTitle('#sigma_{fit}')

    res_graph_2[regions].SetMarkerSize(1.2)
    res_graph_2[regions].SetMarkerStyle(21)
    res_graph_2[regions].SetLineColor(ROOT.kRed)
    res_graph_2[regions].SetMarkerColor(ROOT.kRed)
    res_graph_2[regions].GetXaxis().SetTitleSize(0.042)
    res_graph_2[regions].GetXaxis().SetTitle('m_{gen} [GeV]')
    res_graph_2[regions].GetYaxis().SetTitleSize(0.052)
    res_graph_2[regions].GetYaxis().SetTitle('#sigma_{fit}')

    leg=ROOT.TLegend(0.35,0.7,0.9,0.85)
    leg.SetBorderSize(0)
    leg.SetFillColor(ROOT.kWhite)
    if(_t=='resolution'):
       leg.AddEntry(res_graph[regions],"Resolution with corrected energy","pe")
       leg.AddEntry(res_graph_2[regions],"Resolution with raw SC energy","pe")

    if variable_type=='HoverE':
        res_graph[regions].GetYaxis().SetTitle('HoverE sum')
    if variable_type=='scale':
        res_graph[regions].GetYaxis().SetTitle('mass scale')

    res_graph[regions].Draw("APE")
    res_graph_2[regions].Draw("PE") # This is the way to superimpose graphs
    if(_t=='scale'):
       leg.AddEntry(res_graph[regions],"Scale with corrected energy","pe")
       leg.AddEntry(res_graph_2[regions],"Scale with raw SC energy","pe")
       x1=res_graph[regions].GetXaxis().GetBinLowEdge(res_graph[regions].GetXaxis().GetFirst())
       x2=res_graph[regions].GetXaxis().GetBinUpEdge(res_graph[regions].GetXaxis().GetLast())
       line1 =ROOT.TLine(x1,1,x2,1);
       line1.SetLineWidth(2);
       line1.Draw();
    leg.Draw("same")
    cms =ROOT.TLatex(0.12,0.95,"CMS Internal")
    cms.SetNDC()
    cms.Draw()

    canvas[regions].Write()

    if "scale" in variable_type:
       canvas[regions].Print(str('roofit/fit_results/scale_'+regions+'/'+variable_type+'_'+regions+'_comparison.png'))
       canvas[regions].Print(str('roofit/fit_results/scale_'+regions+'/'+variable_type+'_'+regions+'_comparison.pdf'))
       canvas[regions].Print(str('roofit/fit_results/scale_'+regions+'/'+variable_type+'_'+regions+'_comparison.eps'))
    elif "resolution" in variable_type:
       canvas[regions].Print(str('roofit/fit_results/resolution_'+regions+'/'+variable_type+'_'+regions+'_comparison.png'))
       canvas[regions].Print(str('roofit/fit_results/resolution_'+regions+'/'+variable_type+'_'+regions+'_comparison.pdf'))
       canvas[regions].Print(str('roofit/fit_results/resolution_'+regions+'/'+variable_type+'_'+regions+'_comparison.eps'))


