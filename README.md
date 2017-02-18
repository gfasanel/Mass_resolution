### Mass_resolution
```
cd Mass_resolution_study/ (link simbolico per HEEP/CMSSW_7_2_0_patch1/src/Mass_resolution/)
source setter.sh #(setta root e cmsenv)
```

**00) Get the name of the variables**
```
python Dumper.py > tree_content_2016.log
```
**0) Dump the root files names in a .txt**
```
#Scrivi la lista dei file su cui girare
source file_dumper.sh
```


**1) Sigma extra calculation**

```
#E' commentato perche' fare gli istogrammi prende tempo: 
#Impiega 14 minuti circa per 1 milione di eventi (quindi ti puoi fare il conto)

#python histos_for_sigma_extra_newID.py ##->questo usa una funzioncina mia per calcolarsi hasPassedHEEP
#The histograms are saved in Extra_sigma/Histos/

##### TEST JOBS 
# Prima devi capire quanti job sottometter
source job_submission/submit_sigma_extra_B.sh 0 
source job_submission/submit_sigma_extra_C.sh 0
source job_submission/submit_sigma_extra_D.sh 0
source job_submission/submit_sigma_extra_E.sh 0
source job_submission/submit_sigma_extra_F.sh 0
source job_submission/submit_sigma_extra_G.sh 0
source job_submission/submit_sigma_extra_H.sh 0
source job_submission/submit_sigma_extra_MC.sh 0

Guarda l'out per capire quanti job servono e a quel punto:
[gfasanel@m6 Mass_resolution_study]$ emacs job_submission/script_sigma_F_0.stdout 
index max job is 16
A quel punto
##### SEND ALL JOBS
source job_submission/submit_sigma_extra_B.sh 68
source job_submission/submit_sigma_extra_C.sh 22
source job_submission/submit_sigma_extra_D.sh 26
source job_submission/submit_sigma_extra_E.sh 24
source job_submission/submit_sigma_extra_F.sh 16
source job_submission/submit_sigma_extra_G.sh 38
source job_submission/submit_sigma_extra_H.sh 123
source job_submission/submit_sigma_extra_MC.sh 5

##stessa cosa per il MC
#source job_submission/submit_sigma_extra_MC.sh 5

#Controllare lo stato dei job: source job_submission/checker.sh

#Nel caso vuoi killare:
[gfasanel@m6 Mass_resolution_study]$ source job_submission/checker.sh >jobs.dat
[gfasanel@m6 Mass_resolution_study]$ emacs jobs.dat
[gfasanel@m6 Mass_resolution_study]$ python killjobs.py

####HADD ALL ROOT FILES
source hadder.sh
```

### Fatte le ntuple fitta tutto e cucina i numeri
```
cd roofit/
#nota che hai bisogno di caricare qualche libreria per poter utilizzare ROOFit correttamente,
#io lo faccio con un rootlogon messo nella cartella roofit
python Zpeak_fitter.py | tee debug.txt
#Per scrivere tutto su una tabella latex
python ../Extra_sigma/sigma_extra.py
cd ../

Use tex on web to quickly generate your latex table
```
https://tex.mendelu.cz/en/

**2) Risoluzione MC only**

```
#E' commentato perche' fare gli istogrammi prende tempo: 
### TEST JOB (questo per capire quanti job fare): 
#python histos_for_resolution_newID.py -i 0
#Controlla che qualcosa ci sia
h_mee_gen_BB->GetEntries()
h_resolution_BB_1->GetEntries()
#index max job is  3
### SEND ALL JOBS
#lancia questo comando solo se sei veramente sicuro
# in job_submission: source job_submission/submit_resolution.sh 3
#Controllare lo stato dei job: source job_submission/checker.sh

### HADD ALL JOBS
#source resolution_histos_hadder.sh #hadd all jobs together
```

```
cd roofit/
#python cb_fitter.py -t resolution > fit_results/resolution_results.txt
#Oppure, meglio
python cruijff_fitter.py -t resolution > fit_results/resolution_results_cruijf.txt
# with -t resolution you write all the parameters of the cb (or dCB), including the scale file (fitted scale vs mass bins)
cd ..
#Make the plot of the fitted parameters vs mass (the -t parameter specify the name of the dat file to plot)
python res_scale_plotter_generic.py -t resolution
python res_scale_plotter_generic.py -t scale
python res_scale_plotter_generic.py -t alphaL
python res_scale_plotter_generic.py -t alphaR
#python res_scale_plotter.py -t resolution
#python res_scale_plotter_alphaL.py -t alphaL
#python res_scale_plotter_alphaR.py -t alphaR
#python res_scale_plotter_scale.py -t scale

#Test the parametrizations
python plot_cruijiff.py -t resolution
```

```
**2_final) source AN_sender.sh #scp dei plot su afs dove e' la nota
```

**2+) Con e senza SC corrections
```
python cb_fitter.py -t res_SC > fit_results/resolution_results.txt
python compare_plotter.py -t scale

```

**3) H/E check**
```
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
```


