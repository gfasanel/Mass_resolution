source=/user/gfasanel/public_html/Res_scale_16
dest=gfasanel@lxplus.cern.ch:/afs/cern.ch/user/g/gfasanel/CERN_documents/svnrepo/notes/AN-16-190/trunk/chapters/mass_resolution_figures

scp ${source}/Extra_sigma/*.pdf Extra_sigma/latex_extra_sigma_2016.tex ${source}/fit_results/resolution_*pdf ${source}/fit_results/scale_*.pdf ${source}/fit_results/HoverE/HoverE_*.pdf ${source}/fit_results/HoverE/HTotoverETot_*.pdf ${source}/fit_results/HoverE/eta_distributions.png ${dest}
