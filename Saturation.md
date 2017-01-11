```
root -l roofit/rootlogon_style.C Resolution/histograms_mass_res.root
h_resolution_BB_10->Draw()
c1.SaveAs("~/public_html/Res_scale_15/fit_results/resolution_BB/g6TeV.png")
h_resolution_BB_9->Draw()
c1.SaveAs("~/public_html/Res_scale_15/fit_results/resolution_BB/45_6TeV.png")
h_resolution_BE_10->Draw()
c1.SaveAs("~/public_html/Res_scale_15/fit_results/resolution_BE/g6TeV.png")
h_resolution_BE_9->Draw()
c1.SaveAs("~/public_html/Res_scale_15/fit_results/resolution_BE/45_6TeV.png")
.q
```