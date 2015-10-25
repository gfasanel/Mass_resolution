source=/user/gfasanel/public_html/Res_scale_15
dest=gfasanel@lxplus.cern.ch:/afs/cern.ch/user/g/gfasanel/CERN_documents/svnrepo/notes/AN-15-222/trunk/Strategy/images/

scp ${source}/Extra_sigma/*.pdf Extra_sigma/latex_extra_sigma.tex ${source}/fit_results/resolution_*pdf ${source}/fit_results/scale_BB/scale_BB.pdf ${source}/fit_results/scale_BE/scale_BE.pdf ${source}/fit_results/scale_EE/scale_EE.pdf ${dest}
#Resolution/fit_results/scale_BB/*.pdf ${dest}