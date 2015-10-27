*Da Mass_resolution_Study*

```
#resolution_histos_maker.sh
#python histos_for_resolution.py -i 0 (Se vuoi fare un test su 100.000 entries)
python HoE.py #scrive su file la media delle distribuzioni di H/E in bin di Mee
python res_scale_plotter.py -t HoverE #questo plotta
python res_scale_plotter.py -t HTotoverETot
python res_scale_plotter.py -t HoverE_lowEta
python res_scale_plotter.py -t HoverE_highEta
python res_scale_plotter.py -t HTotoverETot_lowEta
python res_scale_plotter.py -t HTotoverETot_highEta

root Resolution/histograms_mass_res.root
HoverE_eta.Draw()
c1.SaveAs("~/public_html/Res_scale_15/fit_results/HoverE/2D_HoverE_eta.png")
.q
root roofit/rootlogon_style.C Resolution/histograms_mass_res.root
eta_eleBarrel_BE.getXaxis().SetTitle("electron #eta")
eta_eleBarrel_BE.getYaxis().SetTitle("Normalized events")
eta_eleBarrel_BE.DrawNormalized()
eta_eleBarrel_BB.SetLineColor(kRed)
eta_eleBarrel_BB.SetMarkerColor(kRed)
eta_eleBarrel_BB.DrawNormalized("same")
leg = new TLegend(0.1,0.7,0.48,0.9);
leg->AddEntry(eta_eleBarrel_BB,"electron #eta for BB","ep");
leg->AddEntry(eta_eleBarrel_BE,"electron #eta for BE","ep");
leg->Draw();
root [9] 
```