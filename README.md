### Mass_resolution
```
cd Mass_resolution_study/ (link simbolico per HEEP/CMSSW_7_2_0_patch1/src/Mass_resolution/)
source setter.sh #(setta root e cmsenv)
```

**1) Sigma extra calculation**

```
#E' commentato perche' fare gli istogrammi prende tempo: 
#lancia questo comando solo se sei veramente sicuro
#python histos_for_sigma_extra.py
#The histograms are saved in Extra_sigma/
```

```
cd roofit/
#nota che hai bisogno di caricare qualche libreria per poter utilizzare ROOFit correttamente,
#io lo faccio con un rootlogon messo nella cartella roofit
python Zpeak_fitter.py > debug.txt
#Per scrivere tutto su una tabella latex
python ../Extra_sigma/sigma_extra.py
cd ../
```

**2) Risoluzione MC only**

```
#source resolution_histos_maker.sh
# in ~/directsubmission/ source submit_all.sh
#python histos_for_resolution -i xxx
```

```
cd roofit/
python cb_fitter.py -t resolution > fit_results/resolution_results.txt
python cb_fitter.py -t scale > fit_results/scale_results.txt
cd ..
python res_scale_plotter.py -t resolution
python res_scale_plotter.py -t scale
python HoE.py
python res_scale_plotter.py -t HoverE
python res_scale_plotter.py -t HTotoverETot
#dai una occhiata a Leakage.md
```

Extra
```
python cb_fitter.py -t res_SC > fit_results/resolution_supercluster_results.txt
python cb_fitter.py -t res_h > fit_results/resolution_h_results.txt
python cb_fitter.py -t scale_SC > fit_results/scale_supercluster_results.txt
python cb_fitter.py -t scale_h > fit_results/scale_h_results.txt
python res_scale_plotter.py -t resolution_supercluster
python res_scale_plotter.py -t scale_supercluster
python res_scale_plotter.py -t resolution_h_recover
python res_scale_plotter.py -t scale_h_recover
python compare_plotter.py -t resolution
python compare_plotter.py -t scale
```


