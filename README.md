### Mass_resolution

**In practice you do this**

remote_dir_mount

sshm6

cd HEEP/CMSSW_7_2_0_patch1/src/

source setter.sh

cd Mass_resolution/

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

cd roofit/

source fit_publisher.sh

cd ../

remote_dir_umount



************SPIEGAZIONE********************************************



***************************************
Montare la cartella remota in locale:
sshfs gfasanel@m6.iihe.ac.be:/user/gfasanel/HEEP/CMSSW_7_2_0_patch1/src/Mass_resolution/roofit/fit_results Scrivania/remote_dir
(per smontare) sudo umount /home/gfasanel/Scrivania/remote_dir
*********************************************

cd HEEP/CMSSW_7_2_0_patch1/src/
source setter.sh
cd Mass_resolution/

NOTA CHE Hai bisogno di caricare qualche libreria per poter utilizzare ROOFit correttamente,
io lo faccio con un rootlogon messo nella cartella roofit
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
source fit_organizer.sh (per organizzare in cartelle)

(fitta i bin a cb e scrive le sigma su file. Puoi scegliere se fare la massa con l'energia corretta o no)
Al termine avrai dei png in fit_results/ con tutti gli istogrammi fittati e dei .txt con i risultati dei fit

source fit_publisher.sh
(questo serve a pubblicare i fit bin per bin in massa)
emacs ~/public/HEEP/Eff_plots/histograms_mass_resolution_BB.txt

cd ..
(esci da roofit)

***********PLOT RESOLUTION/SCALE***************
python res_scale_plotter.py -t resolution

root -l ~/public/HEEP/Eff_plots/resolution_plot.root 
root -l ~/public/HEEP/Eff_plots/scale_plot.root 

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
