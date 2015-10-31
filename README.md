### Mass_resolution
```
cd Mass_resolution_study/ (link simbolico per HEEP/CMSSW_7_2_0_patch1/src/Mass_resolution/)
source setter.sh #(setta root e cmsenv)
```

**1) Sigma extra calculation**

```
python histos_for_sigma_extra.py
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
# in directsubmission/ source submit_all.sh
#python histos_for_resolution -i xxx
```

cd roofit/

python cb_fitter.py -t resolution > fit_results/resolution_results.txt

python cb_fitter.py -t res_SC > fit_results/resolution_supercluster_results.txt

python cb_fitter.py -t res_h > fit_results/resolution_h_results.txt

python cb_fitter.py -t scale > fit_results/scale_results.txt

python cb_fitter.py -t scale_SC > fit_results/scale_supercluster_results.txt

python cb_fitter.py -t scale_h > fit_results/scale_h_results.txt

cd ..

python res_scale_plotter.py -t resolution

python res_scale_plotter.py -t scale

python res_scale_plotter.py -t resolution_supercluster

python res_scale_plotter.py -t scale_supercluster

python res_scale_plotter.py -t resolution_h_recover

python res_scale_plotter.py -t scale_h_recover

python compare_plotter.py -t resolution

python compare_plotter.py -t scale

python HoE.py

python res_scale_plotter.py -t HoverE

python res_scale_plotter.py -t HTotoverETot

dai una occhiata a Leakage.md
__________________________________________________________________________

**********************************************
ISTROGRAMMI
python histos_for_resolution.py
(crea tutti gli istogrammi in bin di massa)
Li puoi vedere qui:
root -l ~gfasanel/public/HEEP/Eff_plots/histograms_mass_res.root 
**********************************************
FIT
cd roofit/
python cb_fitter.py -t resolution (or scale)

(fitta i bin a cb e scrive le sigma su file. Puoi scegliere se fare la massa con l'energia corretta o no)
Al termine avrai dei png in fit_results/ con tutti gli istogrammi fittati e dei .txt con i risultati dei fit


***********PLOT RESOLUTION/SCALE***************
python res_scale_plotter.py -t resolution


***********COMPARE PLOTS**********************
python compare_plotter.py -t resolution

***********HOE check*************************

Plotto la media di HoE (somma) in funzione di mee
python HoE.py (questo crea il file che poi sara' effitavamente plottato))
python res_scale_plotter.py -t HoverE

**********EXTRA*******************************
Posso plottare anche la risoluzione nella categoria BB, chiedendo un taglio su H/E:
cd roofit/
python cb_fitter.py (avendo cura di selezionare scala e risoluzione corretta)
cd ..
python res_scale_plotter.py (avendo cura di selezionare la variabile giusta)
source publisher_res.sh

source publisher_res.sh
